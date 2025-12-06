from flask import Blueprint, request, jsonify, Response, stream_with_context, current_app
from pathlib import Path
import json
from src.handlers.meeting_processing import process_upload, process_file
from src.audio.huggingface_stt import transcribe_audio_huggingface
from src.audio.speaker_diarization import transcribe_with_speakers

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/process', methods=['POST'])
def process_upload_file():
    try:
        file_type = request.form.get('file_type', 'audio')
        meeting_type = request.form.get('meeting_type', 'meeting')
        output_lang = request.form.get('output_lang', 'vi')
        transcribe_lang = request.form.get('transcribe_lang', 'vi')
        enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
        
        audio_file = None
        text_file = None
        
        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        
        if file_type == 'audio':
            if 'audio_file' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            f = request.files['audio_file']
            path = upload_folder / f.filename
            f.save(path)
            audio_file = str(path)
        else:
            if 'text_file' not in request.files:
                return jsonify({'error': 'No text file provided'}), 400
            f = request.files['text_file']
            path = upload_folder / f.filename
            f.save(path)
            text_file = str(path)
            
        status, transcript, summary, topics, actions, decisions, participants = process_upload(
            file_type=file_type,
            audio_file=audio_file,
            text_file=text_file,
            transcribe_lang=transcribe_lang,
            enable_diarization=enable_diarization,
            meeting_type=meeting_type,
            output_lang=output_lang
        )
        
        return jsonify({
            'status': status,
            'transcript': transcript,
            'summary': summary,
            'topics': topics,
            'actions': actions,
            'decisions': decisions,
            'participants': participants
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/process/stream', methods=['POST'])
def process_upload_stream():
    try:
        file_type = request.form.get('file_type', 'audio')
        meeting_type = request.form.get('meeting_type', 'meeting')
        output_lang = request.form.get('output_lang', 'vi')
        transcribe_lang = request.form.get('transcribe_lang', 'vi')
        enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
        
        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        audio_file, text_file = None, None
        
        if file_type == 'audio':
            f = request.files.get('audio_file')
            if f:
                path = upload_folder / f.filename
                f.save(path)
                audio_file = str(path)
        else:
            f = request.files.get('text_file')
            if f:
                path = upload_folder / f.filename
                f.save(path)
                text_file = str(path)

        def generate():
            try:
                if file_type == 'audio' and audio_file:
                    yield f"data: {json.dumps({'step': 'transcribe', 'status': 'Transcribing...'})}\n\n"
                    if enable_diarization:
                        for update in transcribe_with_speakers(audio_file, transcribe_lang):
                            yield f"data: {json.dumps({'step': 'transcribe', 'update': update})}\n\n"
                    else:
                        for update in transcribe_audio_huggingface(audio_file, transcribe_lang, realtime=True):
                            yield f"data: {json.dumps({'step': 'transcribe', 'update': update})}\n\n"
                
                yield f"data: {json.dumps({'step': 'analyze', 'status': 'Analyzing...'})}\n\n"
                
                results = process_upload(
                    file_type, audio_file, text_file, transcribe_lang, 
                    enable_diarization, meeting_type, output_lang
                )
                
                # Unpack tuple
                status, transcript, summary, topics, actions, decisions, participants = results
                
                payload = {
                    'done': True,
                    'results': {
                        'status': status, 'transcript': transcript, 'summary': summary,
                        'topics': topics, 'actions': actions, 'decisions': decisions,
                        'participants': participants
                    }
                }
                yield f"data: {json.dumps(payload)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(stream_with_context(generate()), mimetype='text/event-stream')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
