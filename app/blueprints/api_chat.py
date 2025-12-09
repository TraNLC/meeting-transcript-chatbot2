from flask import Blueprint, request, jsonify
from backend.handlers.meeting_processing import chat_with_ai, refresh_history, load_history

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
    
    # Get context from request
    context = data.get('context', {})
    
    # Validate: Must have context (scoped to meeting)
    if not context or not any([context.get('summary'), context.get('transcript')]):
        return jsonify({'error': 'Context is required. Please reload the page.'}), 400
    
    # Build scoped prompt
    system_prompt = """Bạn là AI assistant chuyên phân tích meeting. 
    
QUAN TRỌNG:
- CHỈ trả lời câu hỏi về meeting này
- KHÔNG trả lời câu hỏi chung hoặc ngoài phạm vi meeting
- Trả lời ngắn gọn, súc tích (2-3 câu)
- Dựa trên context được cung cấp
- Nếu không tìm thấy thông tin → Nói rõ "Không tìm thấy trong meeting"

Context của meeting:"""
    
    context_parts = []
    if context.get('summary'):
        context_parts.append(f"Tóm tắt: {context['summary'][:800]}")
    if context.get('topics'):
        topics_str = str(context['topics'])[:500]
        context_parts.append(f"Chủ đề: {topics_str}")
    if context.get('actions'):
        actions_str = str(context['actions'])[:500]
        context_parts.append(f"Hành động: {actions_str}")
    if context.get('decisions'):
        decisions_str = str(context['decisions'])[:500]
        context_parts.append(f"Quyết định: {decisions_str}")
    if context.get('transcript'):
        # Add transcript for full context (limit to 2000 chars to avoid token limit)
        transcript_str = str(context['transcript'])[:2000]
        context_parts.append(f"Transcript: {transcript_str}")
    
    full_prompt = f"{system_prompt}\n\n{chr(10).join(context_parts)}\n\nCâu hỏi: {message}"
    
    # Simple response for now
    try:
        # Mock response based on message
        if "deadline" in message.lower():
            response_text = "Dựa trên meeting này, các deadline quan trọng cần theo dõi."
        elif "ai" in message.lower() or "trách nhiệm" in message.lower():
            response_text = "Các action items đã được phân công cho từng thành viên trong team."
        elif "tóm tắt" in message.lower():
            response_text = "Meeting tập trung vào việc thảo luận kế hoạch phát triển và phân công nhiệm vụ."
        else:
            response_text = f"Tôi hiểu câu hỏi của bạn về '{message}'. Dựa trên nội dung meeting, đây là thông tin liên quan."
        
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
