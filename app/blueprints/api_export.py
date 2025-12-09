from flask import Blueprint, request, send_file, jsonify
from backend.handlers.meeting_processing import export_to_txt, export_to_docx
import os

export_bp = Blueprint('export', __name__)

@export_bp.route('/<format>', methods=['GET', 'POST'])
def export_file(format):
    content = None
    if request.method == 'POST':
        data = request.json
        content = data.get('content')
    
    # If GET or no content in POST, content remains None
    # export functions in meeting_processing.py handle None by using global state
    
    # if not content and request.method == 'POST':
    #    return jsonify({'error': 'No content provided'}), 400
        
    try:
        path = None
        if format == 'txt':
            path = export_to_txt(content)
        elif format == 'docx':
            path = export_to_docx(content)
            
        if path and os.path.exists(path):
            return send_file(path, as_attachment=True)
        else:
            return jsonify({'error': 'Export failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
