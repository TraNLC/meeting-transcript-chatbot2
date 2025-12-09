from flask import Blueprint, request, jsonify, Response, stream_with_context, current_app
from pathlib import Path
import json
import re
import os
from werkzeug.utils import secure_filename
from backend.handlers.meeting_processing import process_upload, process_file
from backend.audio.huggingface_stt import transcribe_audio_huggingface
from backend.audio.speaker_diarization import transcribe_with_speakers

upload_bp = Blueprint('upload', __name__)

# ============================================================================
# Validation & Security Functions
# ============================================================================

def sanitize_filename(filename):
    """Sanitize filename to prevent security issues"""
    if not filename:
        raise ValueError("Filename không được để trống")
    
    # Remove null bytes
    filename = filename.replace('\x00', '')
    
    # Remove path traversal attempts
    filename = filename.replace('..', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    
    # Use werkzeug's secure_filename
    filename = secure_filename(filename)
    
    # Check if filename is empty after sanitization
    if not filename or filename == '':
        raise ValueError("Tên file không hợp lệ sau khi sanitize")
    
    # Check filename length (max 255 characters)
    if len(filename) > 255:
        # Truncate but keep extension
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    # Check for reserved Windows names
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                     'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    name_without_ext = os.path.splitext(filename)[0].upper()
    if name_without_ext in reserved_names:
        filename = f"file_{filename}"
    
    return filename


def validate_file(file, file_type):
    """Validate uploaded file"""
    if not file or file.filename == '':
        raise ValueError(f"Không có file {file_type} được chọn")
    
    # Check file size (0 bytes)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size == 0:
        raise ValueError("File không được để trống (0 bytes)")
    
    # Check maximum file size based on file type
    if file_type == 'audio':
        max_size = 1024 * 1024 * 1024  # 1GB for audio/video
        max_size_str = "1GB"
    else:  # text files
        max_size = 100 * 1024 * 1024  # 100MB for text files
        max_size_str = "100MB"
    
    if file_size > max_size:
        raise ValueError(f"File quá lớn ({file_size / 1024 / 1024:.1f}MB). Tối đa {max_size_str}")
    
    # Validate extension
    filename = file.filename
    if '.' not in filename:
        # Allow files without extension but warn
        pass
    else:
        ext = filename.rsplit('.', 1)[1].lower()
        
        if file_type == 'audio':
            valid_audio_exts = ['wav', 'mp3', 'webm', 'ogg', 'm4a', 'flac']
            if ext not in valid_audio_exts:
                raise ValueError(f"Định dạng audio không hợp lệ: .{ext}. Chấp nhận: {', '.join(valid_audio_exts)}")
        elif file_type == 'text':
            valid_text_exts = ['txt', 'docx', 'pdf', 'json']
            if ext not in valid_text_exts:
                raise ValueError(f"Định dạng text không hợp lệ: .{ext}. Chấp nhận: {', '.join(valid_text_exts)}")
    
    return True


def validate_language(lang):
    """Validate language code"""
    if not lang:
        return 'vi'  # Default
    
    # Normalize to lowercase
    lang = lang.lower().strip()
    
    # Valid language codes
    valid_langs = ['vi', 'en', 'ja', 'ko', 'zh', 'th', 'id', 'ms', 'fr', 'de', 'es']
    
    if lang not in valid_langs:
        raise ValueError(f"Ngôn ngữ không hợp lệ: {lang}. Chấp nhận: {', '.join(valid_langs)}")
    
    return lang


# ============================================================================
# Routes
# ============================================================================

@upload_bp.route('/process', methods=['POST'])
def process_upload_file():
    """Process file upload with comprehensive error handling"""
    try:
        # Handle JSON Request (from Client-side Colab flow)
        if request.is_json:
            data = request.get_json()
            if 'transcript' in data:
                import tempfile
                import os
                
                transcript_text = data['transcript']
                meeting_type = data.get('meeting_type', 'meeting')
                output_lang = data.get('output_lang', 'vi')
                
                # Save to temp file
                fd, temp_path = tempfile.mkstemp(suffix='.txt', text=True)
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(transcript_text)
                    
                try:
                    result = process_upload(
                        file_type='text',
                        text_file=temp_path,
                        meeting_type=meeting_type,
                        output_lang=output_lang
                    )
                    
                    status, transcript, summary, topics, actions, decisions, participants = result
                    
                    # Return JSON
                    return jsonify({
                        'status': status, 'transcript': transcript, 'summary': summary,
                        'topics': topics, 'actions': actions, 'decisions': decisions, 'participants': participants
                    })
                finally:
                    try: os.unlink(temp_path)
                    except: pass

        # Get parameters (Standard Form Data)
        file_type = request.form.get('file_type', 'audio')
        meeting_type = request.form.get('meeting_type', 'meeting')
        output_lang = request.form.get('output_lang', 'vi')
        transcribe_lang = request.form.get('transcribe_lang', 'vi')
        enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
        colab_url = request.form.get('colab_url', '').strip()
        
        # Validate language
        try:
            transcribe_lang = validate_language(transcribe_lang)
            output_lang = validate_language(output_lang)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Validate file type
        if file_type not in ['audio', 'text']:
            return jsonify({'error': f'Loại file không hợp lệ: {file_type}'}), 400
        
        audio_file = None
        text_file = None
        
        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        upload_folder.mkdir(parents=True, exist_ok=True)
        
        # Handle file upload with validation
        try:
            if file_type == 'audio':
                if 'audio_file' not in request.files:
                    return jsonify({'error': 'Không có file audio được tải lên'}), 400
                
                f = request.files['audio_file']
                
                # Validate file
                validate_file(f, 'audio')
                
                # Sanitize filename
                safe_filename = sanitize_filename(f.filename)
                
                # Save file
                path = upload_folder / safe_filename
                f.save(str(path))
                audio_file = str(path)
                
            else:  # text
                if 'text_file' not in request.files:
                    return jsonify({'error': 'Không có file text được tải lên'}), 400
                
                f = request.files['text_file']
                
                # Validate file
                validate_file(f, 'text')
                
                # Sanitize filename
                safe_filename = sanitize_filename(f.filename)
                
                # Save file
                path = upload_folder / safe_filename
                f.save(str(path))
                text_file = str(path)
        
        except ValueError as e:
            # Validation errors
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # File save errors
            return jsonify({'error': f'Lỗi khi lưu file: {str(e)}'}), 400
        
        # Process the file
        try:
            status, transcript, summary, topics, actions, decisions, participants = process_upload(
                file_type=file_type,
                audio_file=audio_file,
                text_file=text_file,
                transcribe_lang=transcribe_lang,
                enable_diarization=enable_diarization,
                meeting_type=meeting_type,
                output_lang=output_lang,
                colab_url=colab_url
            )
            
            # Check if status indicates an error
            if status.startswith('❌') or status.startswith('⚠️'):
                return jsonify({'error': status}), 400
            
            # Return success response

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
            # Processing errors
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return jsonify({'error': '⚠️ Đã vượt quá giới hạn API. Vui lòng đợi vài phút và thử lại.'}), 429
            return jsonify({'error': f'Lỗi khi xử lý file: {error_msg}'}), 500
    
    except Exception as e:
        # Unexpected errors
        return jsonify({'error': f'Lỗi không xác định: {str(e)}'}), 500


@upload_bp.route('/read-file', methods=['POST'])
def read_original_file():
    """Read original file content from uploads directory"""
    try:
        data = request.get_json()
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        # Sanitize filename
        safe_filename = secure_filename(filename)
        
        # Look for file in uploads directory
        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        file_path = upload_folder / safe_filename
        
        if not file_path.exists():
            return jsonify({'error': f'File not found: {safe_filename}'}), 404
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return jsonify({
                'success': True,
                'content': content,
                'filename': safe_filename,
                'size': len(content)
            })
        except Exception as e:
            return jsonify({'error': f'Cannot read file: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/load-original-file', methods=['POST'])
def load_original_file():
    """Load original file content - alias for read-file"""
    return read_original_file()


@upload_bp.route('/check-history', methods=['POST'])
def check_file_history():
    """Check if file was already analyzed"""
    try:
        data = request.get_json()
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        # Check in history folder
        history_dir = Path('data/history')
        history_dir.mkdir(parents=True, exist_ok=True)
        
        # Look for history file
        safe_filename = secure_filename(filename)
        base_name = Path(safe_filename).stem
        
        # Find matching history files
        history_files = list(history_dir.glob(f"*{base_name}*.json"))
        
        if history_files:
            # Load most recent
            latest_file = max(history_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            return jsonify({
                'found': True,
                'history_id': latest_file.stem,
                'timestamp': history_data.get('timestamp'),
                'summary_preview': history_data.get('summary', '')[:200] + '...',
                'data': history_data
            })
        else:
            return jsonify({'found': False})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500