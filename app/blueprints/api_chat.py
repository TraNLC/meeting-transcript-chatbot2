from flask import Blueprint, request, jsonify
from src.handlers.meeting_processing import chat_with_ai, refresh_history, load_history

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.json
    response_text = chat_with_ai(data.get('message'))
    return jsonify({'answer': response_text})

@chat_bp.route('/history/list', methods=['GET'])
def list_history():
    try:
        choices, info = refresh_history()
        return jsonify({'dropdown': choices, 'info': str(info)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/load/<history_id>', methods=['GET'])
def load_history_item(history_id):
    try:
        result = load_history(history_id)
        # Handle unpacking based on tuple size
        if isinstance(result, tuple):
            info = result[0]
            summary = result[1] if len(result) > 1 else ''
            topics = result[2] if len(result) > 2 else ''
        else:
            info, summary, topics = str(result), '', ''
            
        return jsonify({'info': info, 'summary': summary, 'topics': topics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
