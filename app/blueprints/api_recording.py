from flask import Blueprint, request, jsonify
from pathlib import Path
import json
import sys
# Logic Imports
# We can import directly from src as before, assuming sys.path in run.py handles it
# OR we put the sys.path append in app/__init__.py or run.py

from backend.handlers.recording_management import (
    load_selected_recording,
    delete_selected_recording
)
from backend.handlers.meeting_processing import save_recording_and_transcribe

recording_bp = Blueprint('recording', __name__)

@recording_bp.route('/history', methods=['GET'])
def get_recording_history():
    filter_type = request.args.get('filter', 'Tất cả')
    category = request.args.get('category', 'recording')
    
    try:
        # Assuming path relative to CWD (root)
        metadata_file = Path('data/recordings/metadata.json')
        
        if not metadata_file.exists():
            return jsonify({'recordings': []})
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recordings = data.get('recordings', [])
        recordings = [r for r in recordings if r.get('category') == category]
        recordings.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({'recordings': recordings})
        
    except Exception as e:
        return jsonify({'error': str(e), 'recordings': []}), 500

@recording_bp.route('/load/<recording_id>', methods=['GET'])
def load_recording(recording_id):
    audio_path, transcript, info = load_selected_recording(recording_id)
    return jsonify({
        'audio_path': audio_path,
        'transcript': transcript,
        'info': info
    })

@recording_bp.route('/delete/<recording_id>', methods=['DELETE'])
def delete_recording(recording_id):
    status, html = delete_selected_recording(recording_id)
    return jsonify({
        'status': status,
        'html': html
    })

@recording_bp.route('/save', methods=['POST'])
def save_recording():
    """Save recording from browser/mic with audio file upload"""
    try:
        # Check if audio file is in request
        if 'audio' in request.files:
            audio_file = request.files['audio']
            title = request.form.get('title', 'Recording')
            language = request.form.get('language', 'vi')
            
            # Save audio file
            from pathlib import Path
            import time
            
            recordings_dir = Path('data/recordings')
            recordings_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = int(time.time())
            filename = f"recording_{timestamp}.webm"
            audio_path = recordings_dir / filename
            audio_file.save(str(audio_path))
            
            # Process with transcription
            status, rec_id = save_recording_and_transcribe(
                str(audio_path),
                title,
                language,
                None  # transcript will be generated
            )
            
            return jsonify({
                'status': status,
                'recording_id': rec_id
            })
        else:
            # Old JSON format
            data = request.json
            status, rec_id = save_recording_and_transcribe(
                data.get('audio_path'),
                data.get('title'),
                data.get('language'),
                data.get('transcript')
            )
            return jsonify({
                'status': status,
                'recording_id': rec_id
            })
    except Exception as e:
        return jsonify({
            'status': f'Error: {str(e)}',
            'recording_id': None
        }), 500
