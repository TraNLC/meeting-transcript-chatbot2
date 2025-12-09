from flask import Blueprint, request, jsonify

search_bp = Blueprint('search', __name__)

try:
    from backend.handlers.search_handlers import get_vectordb_stats_ui, search_meetings_ui
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

@search_bp.route('/stats', methods=['GET'])
def search_stats():
    if not SEARCH_AVAILABLE:
        return jsonify({'stats': 'Vector DB not available'})
    return jsonify({'stats': get_vectordb_stats_ui()})

@search_bp.route('/meetings', methods=['POST'])
def search_meetings():
    if not SEARCH_AVAILABLE:
        return jsonify({'status': 'Error', 'results': []})
        
    data = request.json
    status, results = search_meetings_ui(
        data.get('query'), 
        data.get('meeting_type', 'Tất cả'),
        "Tất cả",
        data.get('n_results', 5)
    )
    return jsonify({'status': status, 'results': results})
