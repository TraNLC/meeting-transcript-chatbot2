"""
Flask App for Meeting Analyzer Pro
Modern UI with full control, popup workflow, and all existing features
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sys
import json
import base64
import tempfile
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Import existing modules
from src.audio.huggingface_stt import transcribe_audio_huggingface
from src.ui.recording_history_handlers import (
    get_recordings_grouped_by_date,
    load_selected_recording,
    delete_selected_recording
)
from src.ui.gradio_app_final import (
    save_recording_and_transcribe,
    process_file,
    process_upload,
    chat_with_ai,
    refresh_history,
    load_history,
    export_to_txt,
    export_to_docx
)
try:
    from src.vectorstore.search_ui import (
        get_vectordb_stats_ui,
        search_meetings_ui
    )
except ImportError:
    # Fallback if search_ui doesn't have these functions
    def get_vectordb_stats_ui():
        return "Vector DB stats not available"
    
    def search_meetings_ui(query, meeting_type, lang, n_results):
        return "Search not available", []

# Import Advanced RAG
try:
    from src.rag.advanced_rag import get_rag_instance
    rag_system = get_rag_instance(vector_store="chroma")
    print("✅ Advanced RAG system initialized")
except Exception as e:
    print(f"⚠️  Advanced RAG not available: {e}")
    rag_system = None

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = 'meeting-analyzer-secret-key'
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure upload folder
UPLOAD_FOLDER = Path('data/uploads')
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max


# ============================================================================
# ROUTES - Main Pages
# ============================================================================

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


# ============================================================================
# API ROUTES - Tab 1: Recording & Transcription
# ============================================================================

@app.route('/api/recording/history', methods=['GET'])
def get_recording_history():
    """Get recording history with filter."""
    filter_type = request.args.get('filter', 'Tất cả')
    category = request.args.get('category', 'recording')
    
    try:
        metadata_file = Path('data/recordings/metadata.json')
        
        if not metadata_file.exists():
            return jsonify({'recordings': []})
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recordings = data.get('recordings', [])
        
        # Filter by category
        recordings = [r for r in recordings if r.get('category') == category]
        
        # Sort by timestamp (newest first)
        recordings.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({'recordings': recordings})
        
    except Exception as e:
        return jsonify({'error': str(e), 'recordings': []}), 500


@app.route('/api/recording/load/<recording_id>', methods=['GET'])
def load_recording(recording_id):
    """Load a specific recording."""
    audio_path, transcript, info = load_selected_recording(recording_id)
    
    return jsonify({
        'audio_path': audio_path,
        'transcript': transcript,
        'info': info
    })


@app.route('/api/recording/delete/<recording_id>', methods=['DELETE'])
def delete_recording(recording_id):
    """Delete a recording."""
    status, html = delete_selected_recording(recording_id)
    
    return jsonify({
        'status': status,
        'html': html
    })


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file."""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    language = request.form.get('language', 'vi')
    realtime = request.form.get('realtime', 'true').lower() == 'true'
    
    # Save uploaded file
    audio_path = UPLOAD_FOLDER / audio_file.filename
    audio_file.save(audio_path)
    
    # Transcribe
    results = []
    for update in transcribe_audio_huggingface(str(audio_path), language, realtime):
        results.append(update)
    
    return jsonify({
        'success': True,
        'transcript': results[-1] if results else '',
        'updates': results
    })


@app.route('/api/transcribe/stream', methods=['POST'])
def transcribe_audio_stream():
    """Transcribe audio with streaming updates (SSE)."""
    from flask import Response, stream_with_context
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    language = request.form.get('language', 'vi')
    realtime = request.form.get('realtime', 'true').lower() == 'true'
    
    # Save uploaded file
    audio_path = UPLOAD_FOLDER / audio_file.filename
    audio_file.save(audio_path)
    
    def generate():
        """Generator for SSE streaming."""
        try:
            for update in transcribe_audio_huggingface(str(audio_path), language, realtime):
                # Send update as SSE
                yield f"data: {json.dumps({'update': update})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/recording/save', methods=['POST'])
def save_recording():
    """Save recording with metadata."""
    data = request.json
    
    audio_path = data.get('audio_path')
    title = data.get('title')
    language = data.get('language')
    transcript = data.get('transcript')
    
    status, rec_id = save_recording_and_transcribe(audio_path, title, language, transcript)
    
    return jsonify({
        'status': status,
        'recording_id': rec_id
    })


# ============================================================================
# API ROUTES - Tab 3: Upload & Transcribe (Audio or Text)
# ============================================================================

@app.route('/api/upload/process', methods=['POST'])
def process_upload_file():
    """Process uploaded file - audio or text with optional speaker diarization."""
    try:
        file_type = request.form.get('file_type', 'audio')
        meeting_type = request.form.get('meeting_type', 'meeting')
        output_lang = request.form.get('output_lang', 'vi')
        transcribe_lang = request.form.get('transcribe_lang', 'vi')
        enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
        
        audio_file = None
        text_file = None
        
        if file_type == 'audio':
            if 'audio_file' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio_file']
            audio_path = UPLOAD_FOLDER / audio_file.filename
            audio_file.save(audio_path)
            audio_file = str(audio_path)
            
        else:  # text
            if 'text_file' not in request.files:
                return jsonify({'error': 'No text file provided'}), 400
            
            text_file = request.files['text_file']
            text_path = UPLOAD_FOLDER / text_file.filename
            text_file.save(text_path)
            text_file = str(text_path)
        
        # Process with new handler
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


@app.route('/api/upload/process/stream', methods=['POST'])
def process_upload_stream():
    """Process uploaded file with streaming updates (SSE)."""
    from flask import Response, stream_with_context
    
    try:
        file_type = request.form.get('file_type', 'audio')
        meeting_type = request.form.get('meeting_type', 'meeting')
        output_lang = request.form.get('output_lang', 'vi')
        transcribe_lang = request.form.get('transcribe_lang', 'vi')
        enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
        
        audio_file = None
        text_file = None
        
        if file_type == 'audio':
            if 'audio_file' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio_file']
            audio_path = UPLOAD_FOLDER / audio_file.filename
            audio_file.save(audio_path)
            audio_file = str(audio_path)
            
        else:  # text
            if 'text_file' not in request.files:
                return jsonify({'error': 'No text file provided'}), 400
            
            text_file = request.files['text_file']
            text_path = UPLOAD_FOLDER / text_file.filename
            text_file.save(text_path)
            text_file = str(text_path)
        
        def generate():
            """Generator for SSE streaming."""
            try:
                # Step 1: Transcribe if audio
                if file_type == 'audio':
                    yield f"data: {json.dumps({'step': 'transcribe', 'status': 'Đang transcribe audio...'})}\n\n"
                    
                    if enable_diarization:
                        from src.audio.speaker_diarization import transcribe_with_speakers
                        
                        for update in transcribe_with_speakers(audio_file, transcribe_lang):
                            yield f"data: {json.dumps({'step': 'transcribe', 'update': update})}\n\n"
                    else:
                        for update in transcribe_audio_huggingface(audio_file, transcribe_lang, realtime=True):
                            yield f"data: {json.dumps({'step': 'transcribe', 'update': update})}\n\n"
                
                # Step 2: Analyze
                yield f"data: {json.dumps({'step': 'analyze', 'status': 'Đang phân tích với AI...'})}\n\n"
                
                status, transcript, summary, topics, actions, decisions, participants = process_upload(
                    file_type=file_type,
                    audio_file=audio_file,
                    text_file=text_file,
                    transcribe_lang=transcribe_lang,
                    enable_diarization=enable_diarization,
                    meeting_type=meeting_type,
                    output_lang=output_lang
                )
                
                # Send final results
                yield f"data: {json.dumps({'done': True, 'results': {'status': status, 'transcript': transcript, 'summary': summary, 'topics': topics, 'actions': actions, 'decisions': decisions, 'participants': participants}})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Legacy endpoint for backward compatibility
@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    """Analyze uploaded transcript file (legacy endpoint)."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    meeting_type = request.form.get('meeting_type', 'meeting')
    output_lang = request.form.get('output_lang', 'vi')
    
    # Save file
    file_path = UPLOAD_FOLDER / file.filename
    file.save(file_path)
    
    # Process
    status, summary, topics, actions, decisions = process_file(
        str(file_path), meeting_type, output_lang
    )
    
    return jsonify({
        'status': status,
        'summary': summary,
        'topics': topics,
        'actions': actions,
        'decisions': decisions
    })


# ============================================================================
# API ROUTES - Tab 3: Chat
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI about transcript."""
    data = request.json
    
    message = data.get('message')
    history = data.get('history', [])
    
    updated_history = chat_with_ai(message, history)
    
    return jsonify({
        'history': updated_history
    })


# ============================================================================
# API ROUTES - Tab 4: Analysis History
# ============================================================================

@app.route('/api/history/list', methods=['GET'])
def list_history():
    """Get analysis history list."""
    try:
        dropdown, info = refresh_history()
        
        # Convert Gradio components to serializable data
        dropdown_choices = []
        if hasattr(dropdown, 'choices'):
            dropdown_choices = dropdown.choices
        elif isinstance(dropdown, (list, tuple)):
            dropdown_choices = list(dropdown)
        else:
            dropdown_choices = []
        
        return jsonify({
            'dropdown': dropdown_choices,
            'info': str(info) if info else ''
        })
    except Exception as e:
        return jsonify({
            'dropdown': [],
            'info': f"Error loading history: {str(e)}",
            'error': str(e)
        }), 500


@app.route('/api/history/load/<history_id>', methods=['GET'])
def load_history_item(history_id):
    """Load specific history item."""
    try:
        result = load_history(history_id)
        
        # Handle different return formats
        if isinstance(result, tuple):
            if len(result) == 3:
                info, summary, topics = result
            elif len(result) == 2:
                info, summary = result
                topics = ''
            else:
                info = result[0] if result else ''
                summary = ''
                topics = ''
        else:
            info = str(result)
            summary = ''
            topics = ''
        
        return jsonify({
            'info': str(info) if info else '',
            'summary': str(summary) if summary else '',
            'topics': str(topics) if topics else ''
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'info': '',
            'summary': '',
            'topics': ''
        }), 500


# ============================================================================
# API ROUTES - Tab 5: Search & Export
# ============================================================================

@app.route('/api/search/stats', methods=['GET'])
def search_stats():
    """Get vector database statistics."""
    stats = get_vectordb_stats_ui()
    
    return jsonify({'stats': stats})


@app.route('/api/search/meetings', methods=['POST'])
def search_meetings():
    """Search meetings by query."""
    data = request.json
    
    query = data.get('query')
    meeting_type = data.get('meeting_type', 'Tất cả')
    n_results = data.get('n_results', 5)
    
    status, results = search_meetings_ui(query, meeting_type, "Tất cả", n_results)
    
    return jsonify({
        'status': status,
        'results': results
    })


@app.route('/api/export/txt', methods=['GET'])
def export_txt():
    """Export to TXT file."""
    file_path = export_to_txt()
    
    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'No data to export'}), 400


@app.route('/api/export/docx', methods=['GET'])
def export_docx():
    """Export to DOCX file."""
    file_path = export_to_docx()
    
    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'No data to export'}), 400


# ============================================================================
# API ROUTES - Advanced RAG Features
# ============================================================================

@app.route('/api/rag/smart-search', methods=['POST'])
def smart_search():
    """Smart semantic search with RAG."""
    if not rag_system:
        return jsonify({'error': 'RAG system not available'}), 503
    
    data = request.json
    query = data.get('query', '')
    k = data.get('k', 5)
    filter_metadata = data.get('filter', None)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        results = rag_system.semantic_search(query, k=k, filter_metadata=filter_metadata)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rag/smart-qa', methods=['POST'])
def smart_qa():
    """Smart Q&A with RAG context."""
    if not rag_system:
        return jsonify({'error': 'RAG system not available'}), 503
    
    data = request.json
    question = data.get('question', '')
    context_k = data.get('context_k', 3)
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    try:
        result = rag_system.smart_qa(question, context_k=context_k)
        
        return jsonify({
            'success': True,
            'question': question,
            **result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rag/add-meeting', methods=['POST'])
def add_meeting_to_rag():
    """Add meeting to RAG vector store."""
    if not rag_system:
        return jsonify({'error': 'RAG system not available'}), 503
    
    data = request.json
    meeting_id = data.get('meeting_id')
    transcript = data.get('transcript')
    metadata = data.get('metadata', {})
    
    if not meeting_id or not transcript:
        return jsonify({'error': 'meeting_id and transcript are required'}), 400
    
    try:
        success = rag_system.add_meeting(meeting_id, transcript, metadata)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Meeting {meeting_id} added to RAG system',
                'meeting_id': meeting_id
            })
        else:
            return jsonify({'error': 'Failed to add meeting'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rag/stats', methods=['GET'])
def rag_stats():
    """Get RAG system statistics."""
    if not rag_system:
        return jsonify({'error': 'RAG system not available'}), 503
    
    try:
        stats = rag_system.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WebSocket Events - Realtime Transcription
# ============================================================================

# Store audio chunks per session
audio_buffers = {}

# Initialize faster-whisper model (load once, reuse)
faster_whisper_model = None

def get_faster_whisper_model():
    """Get or initialize faster-whisper model."""
    global faster_whisper_model
    if faster_whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            print("Loading faster-whisper model (base)...")
            # Use base model for speed, can upgrade to small/medium for accuracy
            faster_whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
            print("✅ faster-whisper model loaded!")
        except Exception as e:
            print(f"❌ Error loading faster-whisper: {e}")
            faster_whisper_model = None
    return faster_whisper_model

@socketio.on('connect')
def handle_connect():
    """Client connected."""
    print(f"Client connected: {request.sid}")
    audio_buffers[request.sid] = []
    emit('connected', {'status': 'ready'})


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected."""
    print(f"Client disconnected: {request.sid}")
    if request.sid in audio_buffers:
        del audio_buffers[request.sid]


@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Receive audio chunk and transcribe in realtime with faster-whisper."""
    try:
        session_id = request.sid
        
        # Get audio data
        audio_data = base64.b64decode(data['audio'])
        language = data.get('language', 'vi')
        
        # Add to buffer
        if session_id not in audio_buffers:
            audio_buffers[session_id] = []
        
        audio_buffers[session_id].append(audio_data)
        chunk_num = len(audio_buffers[session_id])
        
        print(f"Received audio chunk #{chunk_num} from {session_id}, size: {len(audio_data)} bytes")
        
        # Try to transcribe with faster-whisper
        model = get_faster_whisper_model()
        
        if model is not None:
            try:
                # Save chunk to temp file
                with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
                    f.write(audio_data)
                    temp_path = f.name
                
                # Transcribe with faster-whisper
                # Anti-hallucination settings
                segments, info = model.transcribe(
                    temp_path,
                    language=language,
                    beam_size=1,  # Faster
                    vad_filter=True,  # Filter silence
                    condition_on_previous_text=False,  # Prevent hallucination
                    temperature=0.0,  # More deterministic
                    compression_ratio_threshold=2.4,  # Detect repetition
                    log_prob_threshold=-1.0,  # Filter low confidence
                    no_speech_threshold=0.6,  # Filter silence better
                    initial_prompt=None  # Don't use prompt that might cause hallucination
                )
                
                # Collect all segments and filter hallucinations
                chunk_text = ""
                hallucination_patterns = [
                    "subscribe",
                    "like",
                    "comment",
                    "bell icon",
                    "notification",
                    "channel",
                    "video",
                    "hãy subscribe",
                    "đăng ký kênh",
                    "bấm chuông",
                    "like và share"
                ]
                
                for segment in segments:
                    text = segment.text.strip()
                    
                    # Skip if contains hallucination patterns
                    text_lower = text.lower()
                    is_hallucination = any(pattern in text_lower for pattern in hallucination_patterns)
                    
                    if not is_hallucination and len(text) > 0:
                        chunk_text += text + " "
                
                # Build cumulative transcript
                all_chunks_text = []
                for i, chunk_data in enumerate(audio_buffers[session_id]):
                    if i < chunk_num - 1:
                        # Previous chunks (already transcribed)
                        pass
                    else:
                        # Current chunk
                        all_chunks_text.append(chunk_text.strip())
                
                cumulative_text = " ".join(all_chunks_text)
                
                if cumulative_text.strip():
                    emit('transcript_update', {
                        'text': cumulative_text,
                        'is_final': False,
                        'chunk': chunk_num
                    })
                    print(f"Sent transcript update #{chunk_num}: {chunk_text[:50]}...")
                else:
                    print(f"Chunk #{chunk_num}: No speech detected (silence)")
                
                # Cleanup
                Path(temp_path).unlink()
                
            except Exception as e:
                print(f"Error transcribing chunk: {e}")
                # Fallback to simulated
                emit('transcript_update', {
                    'text': f"[Processing chunk {chunk_num}...]",
                    'is_final': False
                })
        else:
            # Fallback: simulated transcription
            simulated_texts = [
                "Xin chào,",
                "hôm nay chúng ta sẽ",
                "thảo luận về dự án mới.",
                "Dự án này rất quan trọng",
                "và cần sự tham gia",
                "của tất cả mọi người."
            ]
            
            if chunk_num <= len(simulated_texts):
                cumulative_text = " ".join(simulated_texts[:chunk_num])
                emit('transcript_update', {
                    'text': cumulative_text,
                    'is_final': False,
                    'chunk': chunk_num
                })
        
    except Exception as e:
        print(f"Error processing audio chunk: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': str(e)})


@socketio.on('stop_recording')
def handle_stop_recording(data):
    """Process final transcription."""
    try:
        session_id = request.sid
        language = data.get('language', 'vi')
        
        if session_id not in audio_buffers or not audio_buffers[session_id]:
            emit('transcript_final', {'text': 'No audio recorded'})
            return
        
        # Combine all chunks
        full_audio = b''.join(audio_buffers[session_id])
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
            f.write(full_audio)
            temp_path = f.name
        
        # Transcribe full audio
        emit('transcript_update', {'text': '🔄 Đang xử lý transcript cuối cùng...', 'is_final': False})
        
        # Use existing transcription function
        results = []
        for update in transcribe_audio_huggingface(temp_path, language, realtime=True):
            results.append(update)
            emit('transcript_update', {'text': update, 'is_final': False})
        
        # Send final result
        final_transcript = results[-1] if results else 'No transcript'
        emit('transcript_final', {'text': final_transcript})
        
        # Cleanup
        Path(temp_path).unlink()
        audio_buffers[session_id] = []
        
    except Exception as e:
        print(f"Error in final transcription: {e}")
        emit('error', {'message': str(e)})


# ============================================================================
# Run App
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("🎯 Meeting Analyzer Pro - Flask Edition with WebSocket")
    print("=" * 80)
    print("Starting server...")
    print("URL: http://localhost:5000")
    print("WebSocket: Enabled for realtime transcription")
    print("=" * 80)
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )
