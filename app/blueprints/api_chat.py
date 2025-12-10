from flask import Blueprint, request, jsonify
from backend.handlers.meeting_processing import chat_with_ai, refresh_history, load_history
from backend.rag.chroma_manager import ChromaManager

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
@chat_bp.route('/ask', methods=['POST'])
def chat():
    """Chat with AI about the meeting - SCOPED to meeting context only"""
    from backend.utils.rate_limiter import get_rate_limiter
    
    # Check for valid content-type
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json(silent=True)
    if data is None:
         return jsonify({'error': 'Invalid JSON'}), 400
         
    message = data.get('message', '').strip()
    if not message:
         return jsonify({'error': 'Message is required'}), 400
    
    # Rate limiting: 10 questions per minute
    rate_limiter = get_rate_limiter('chat', max_calls=10, time_window=60)
    if not rate_limiter.wait_if_needed(key='ask_ai', max_wait=5):
        return jsonify({'error': '⚠️ Quá nhiều câu hỏi. Vui lòng đợi 1 phút.'}), 429
    
    try:
        chroma_manager = ChromaManager()
        response_text = chroma_manager.retrieve(message)
        
        return jsonify({'response': response_text, 'answer': response_text})
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

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
