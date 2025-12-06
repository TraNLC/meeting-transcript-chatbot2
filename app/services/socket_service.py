import base64
import tempfile
import json
from flask import request
from flask_socketio import emit
from pathlib import Path
from .audio_service import audio_service

# Store audio chunks per session
audio_buffers = {}

def init_socket_events(socketio):
    
    @socketio.on('connect')
    def handle_connect():
        print(f"Client connected: {request.sid}")
        # Initialize buffer structure
        audio_buffers[request.sid] = {
            'raw_audio': [],
            'segments': [], 
            'temp_file': tempfile.NamedTemporaryFile(suffix='.webm', delete=False).name,
            'diarization_segments': []
        }
        emit('connected', {'status': 'ready'})

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client disconnected: {request.sid}")
        if request.sid in audio_buffers:
            # Cleanup
            try:
                temp_file = audio_buffers[request.sid].get('temp_file')
                if temp_file and Path(temp_file).exists():
                    Path(temp_file).unlink()
            except Exception as e:
                print(f"Error cleaning up temp file: {e}")
            del audio_buffers[request.sid]

    @socketio.on('audio_chunk')
    def handle_audio_chunk(data):
        try:
            session_id = request.sid
            if session_id not in audio_buffers:
                return # Should not happen if connect handled

            audio_data = base64.b64decode(data['audio'])
            language = data.get('language', 'vi')
            
            session_data = audio_buffers[session_id]
            session_data['raw_audio'].append(audio_data)
            
            with open(session_data['temp_file'], 'ab') as f:
                f.write(audio_data)
            
            chunk_num = len(session_data['raw_audio'])
            print(f"Received chunk #{chunk_num} from {session_id}")

            # Transcribe
            try:
                segments = audio_service.transcribe_realtime(session_data['temp_file'], language)
                
                # Diarization (Periodic)
                if chunk_num % 5 == 0:
                     new_segments = audio_service.diarize(session_data['temp_file'])
                     if new_segments:
                         session_data['diarization_segments'] = new_segments
                         print(f"[OK] Diarization updated: {len(new_segments)} speakers")

                # Map Speakers
                diarization_segments = session_data.get('diarization_segments', [])
                current_transcript = []
                
                if not diarization_segments:
                     full_text = " ".join([s.text.strip() for s in segments])
                     if full_text.strip():
                        current_transcript = [{
                            'speaker': 'Guest-1',
                            'text': full_text,
                            'start': segments[0].start if segments else 0,
                            'end': segments[-1].end if segments else 0
                        }]
                else:
                    for seg in segments:
                        text = seg.text.strip()
                        if not text: continue
                        
                        seg_mid = (seg.start + seg.end) / 2
                        best_speaker = "Guest-1"
                        for d_seg in diarization_segments:
                            if d_seg['start'] <= seg_mid <= d_seg['end']:
                                best_speaker = d_seg['speaker']
                                break
                        
                        if current_transcript and current_transcript[-1]['speaker'] == best_speaker:
                             current_transcript[-1]['text'] += " " + text
                             current_transcript[-1]['end'] = seg.end
                        else:
                            current_transcript.append({
                                'speaker': best_speaker,
                                'text': text,
                                'start': seg.start,
                                'end': seg.end
                            })

                session_data['segments'] = current_transcript
                
                emit('transcript_update', {
                    'segments': current_transcript,
                    'is_final': False,
                    'chunk': chunk_num
                })
                
            except Exception as e:
                print(f"Transcription error: {e}")
                emit('error', {'message': str(e)})

        except Exception as e:
            print(f"Error handling chunk: {e}")
            emit('error', {'message': str(e)})

    @socketio.on('stop_recording')
    def handle_stop_recording(data):
        try:
            session_id = request.sid
            if session_id in audio_buffers:
                session_data = audio_buffers[session_id]
                
                final_text = ""
                if 'segments' in session_data:
                    final_text = "\n".join([f"[{s['speaker']}] {s['text']}" for s in session_data['segments']])
                
                emit('transcript_final', {'text': final_text})
                
                # Cleanup
                try:
                    temp_file = session_data.get('temp_file')
                    if temp_file and Path(temp_file).exists():
                        Path(temp_file).unlink()
                except:
                    pass
                del audio_buffers[session_id]
                
        except Exception as e:
            print(f"Error stopping: {e}")
