from flask import Blueprint, request, jsonify

rag_bp = Blueprint('rag', __name__)

try:
    from backend.handlers.rag_handlers import query_rag_system
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

@rag_bp.route('/query', methods=['POST'])
def rag_query():
    if not RAG_AVAILABLE:
        return jsonify({'error': 'RAG system not available'}), 503
        
    data = request.json
    answer = query_rag_system(
        data.get('query'),
        data.get('meeting_type'),
        data.get('k', 5)
    )
    return jsonify({'answer': answer})
