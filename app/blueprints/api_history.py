import os
from flask import Blueprint, request, jsonify
from pathlib import Path
import json
from datetime import datetime

# Import HistorySearcher for semantic search
try:
    from backend.data.history_searcher import HistorySearcher
    # Initialize searcher (singleton pattern)
    _history_searcher = None
    
    def get_history_searcher():
        global _history_searcher
        if _history_searcher is None:
            _history_searcher = HistorySearcher()
            # Index on first use
            _history_searcher.index_all_meetings(force_reindex=False)
        return _history_searcher
except ImportError:
    HistorySearcher = None
    def get_history_searcher():
        return None

# Import RAGEngine
try:
    from backend.rag.rag_engine import RAGEngine
    _rag_engine = None
    
    def get_rag_engine():
        global _rag_engine
        if _rag_engine is None:
            _rag_engine = RAGEngine()
        return _rag_engine
except ImportError:
    RAGEngine = None
    def get_rag_engine(): return None

history_bp = Blueprint('history', __name__)

@history_bp.route('/search', methods=['POST'])
def search_history():
    """Search for existing analysis by filename.
    
    Returns existing analysis if found, otherwise None.
    """
    try:
        data = request.json
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({'found': False})
        
        # Search in history directory
        history_dir = Path('data/history')
        if not history_dir.exists():
            return jsonify({'found': False})
        
        # Get filename without extension for matching
        file_stem = Path(filename).stem.lower()
        
        # Search through history files
        history_files = sorted(
            history_dir.glob('*.json'),
            key=lambda x: x.stat().st_mtime,
            reverse=True  # Most recent first
        )
        
        for history_file in history_files:
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)
                
                # Check if filename matches
                original_file = analysis.get('original_file', '')
                if file_stem in original_file.lower():
                    # Found matching analysis
                    return jsonify({
                        'found': True,
                        'analysis': {
                            'summary': analysis.get('summary', ''),
                            'topics': analysis.get('topics', []),
                            'actions': analysis.get('action_items', []),
                            'decisions': analysis.get('decisions', []),
                            'transcript': analysis.get('metadata', {}).get('transcript', ''),
                            'timestamp': analysis.get('timestamp', ''),
                            'original_file': original_file
                        }
                    })
            except Exception as e:
                print(f"Error reading history file {history_file}: {e}")
                continue
        
        # No matching analysis found
        return jsonify({'found': False})
        
    except Exception as e:
        print(f"Error searching history: {e}")
        return jsonify({'found': False, 'error': str(e)}), 500


# Simple in-memory cache for history files
# Format: {filename: {'mtime': float, 'data': dict}}
_HISTORY_CACHE = {}

@history_bp.route('/list', methods=['GET'])
def list_history():
    """List all analysis history with filtering and sorting.
    
    Optimized with caching to avoid re-reading all JSON files.
    """
    global _HISTORY_CACHE
    try:
        # Get query parameters
        filter_type = request.args.get('filter_type', 'all')
        sort_by = request.args.get('sort_by', 'newest')
        limit = int(request.args.get('limit', 20))
        
        history_dir = Path('data/history')
        if not history_dir.exists():
            return jsonify({'history': []})
        
        # 1. Update Cache
        # Get current files and mtimes
        current_files = {}
        try:
            for entry in os.scandir(history_dir):
                if entry.name.endswith('.json') and entry.is_file():
                    current_files[entry.name] = entry.stat().st_mtime
        except Exception as e:
            # Fallback if scandir fails
            history_files = list(history_dir.glob('*.json'))
            for f in history_files:
                current_files[f.name] = f.stat().st_mtime
                
        # Remove deleted files from cache
        keys_to_remove = [k for k in _HISTORY_CACHE if k not in current_files]
        for k in keys_to_remove:
            del _HISTORY_CACHE[k]
            
        # Update cache for new/modified files
        for filename, mtime in current_files.items():
            # If not in cache or modified
            if filename not in _HISTORY_CACHE or _HISTORY_CACHE[filename]['mtime'] != mtime:
                try:
                    file_path = history_dir / filename
                    with open(file_path, 'r', encoding='utf-8') as f:
                        analysis = json.load(f)
                    
                    # Extract only needed fields for list view to save memory
                    compact_data = {
                        'id': analysis.get('id', ''),
                        'timestamp': analysis.get('timestamp', ''),
                        'original_file': analysis.get('original_file', ''),
                        'summary_preview': analysis.get('summary', '')[:100] + '...',
                        'meeting_type': analysis.get('metadata', {}).get('meeting_type', 'meeting')
                    }
                    
                    _HISTORY_CACHE[filename] = {
                        'mtime': mtime,
                        'data': compact_data
                    }
                except Exception as e:
                    print(f"Error reading history file {filename}: {e}")
                    continue

        # 2. Filter and Sort using Cache (Memory Speed!)
        history_list = [item['data'] for item in _HISTORY_CACHE.values()]
        
        # Filter by type
        if filter_type != 'all':
            history_list = [h for h in history_list if h.get('meeting_type') == filter_type]
            
        # Sort
        if sort_by == 'newest':
            history_list.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        elif sort_by == 'oldest':
            history_list.sort(key=lambda x: x.get('timestamp', ''))
        elif sort_by == 'name':
            history_list.sort(key=lambda x: x.get('original_file', '').lower())
        
        # Apply limit
        history_list = history_list[:limit]
        
        return jsonify({
            'history': history_list,
            'total': len(history_list),
            'filter_type': filter_type,
            'sort_by': sort_by
        })
        
    except Exception as e:
        print(f"Error listing history: {e}")
        return jsonify({'history': [], 'error': str(e)}), 500


@history_bp.route('/get/<history_id>', methods=['GET'])
def get_history(history_id):
    """Get specific analysis by ID."""
    try:
        history_file = Path('data/history') / f"{history_id}.json"
        
        if not history_file.exists():
            return jsonify({'error': 'History not found'}), 404
        
        with open(history_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        return jsonify({
            'found': True,
            'analysis': {
                'summary': analysis.get('summary', ''),
                'topics': analysis.get('topics', []),
                'actions': analysis.get('action_items', []),
                'decisions': analysis.get('decisions', []),
                'transcript': analysis.get('metadata', {}).get('transcript', ''),
                'timestamp': analysis.get('timestamp', ''),
                'original_file': analysis.get('original_file', '')
            }
        })
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({'error': str(e)}), 500


@history_bp.route('/semantic-search', methods=['POST'])
def semantic_search():
    """Semantic search over meeting history using AI.
    
    Request body:
    {
        "query": "budget planning meetings",
        "top_k": 5,
        "filters": {"meeting_type": "meeting"}  // optional
    }
    
    Response:
    {
        "results": [
            {
                "id": "...",
                "score": 0.85,
                "title": "...",
                "summary": "...",
                "timestamp": "...",
                "meeting_type": "...",
                "matched_text": "..."
            }
        ]
    }
    """
    try:
        # Get HistorySearcher instance
        searcher = get_history_searcher()
        
        if searcher is None:
            return jsonify({
                'error': 'Semantic search not available. ChromaDB not installed.'
            }), 500
        
        # Get request data
        data = request.json
        query = data.get('query', '').strip()
        top_k = data.get('top_k', 5)
        filters = data.get('filters', None)
        
        # Validate
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 50:
            return jsonify({'error': 'top_k must be between 1 and 50'}), 400
        
        # Perform semantic search
        results = searcher.semantic_search(
            query=query,
            top_k=top_k,
            filters=filters
        )
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return jsonify({'error': str(e)}), 500


@history_bp.route('/reindex', methods=['POST'])
def reindex_history():
    """Force re-index all meetings into ChromaDB.
    
    Useful after adding new meetings or if index is corrupted.
    """
    try:
        searcher = get_history_searcher()
        
        if searcher is None:
            return jsonify({'error': 'HistorySearcher not available'}), 500
        
        # Force re-index
        count = searcher.index_all_meetings(force_reindex=True)
        
        return jsonify({
            'success': True,
            'indexed': count,
            'message': f'Successfully re-indexed {count} meetings'
        })
        
    except Exception as e:
        print(f"Error re-indexing: {e}")
        return jsonify({'error': str(e)}), 500


@history_bp.route('/chat', methods=['POST'])
def chat_history():
    """Chat with meeting history using RAG.
    
    Request:
    {
        "message": "What did we decide about the budget?"
    }
    
    Response:
    {
        "answer": "...",
        "sources": [{"id": 1, "name": "...", "text": "..."}]
    }
    """
    try:
        from backend.rag.conversation_manager import get_conversation_manager
        
        engine = get_rag_engine()
        if engine is None:
            return jsonify({'error': 'RAG Engine not available'}), 500
            
        data = request.json
        query = data.get('message', '').strip()
        
        if not query:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create session ID
        session_id = data.get('session_id') or request.cookies.get('chat_session_id')
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
        
        # Get conversation manager
        conv_manager = get_conversation_manager()
        
        # Get conversation history
        history = conv_manager.get_history(session_id)
        
        # Chat with history
        response = engine.chat(query, conversation_history=history)
        
        # Save to conversation history
        conv_manager.add_message(session_id, "user", query)
        conv_manager.add_message(session_id, "assistant", response['answer'])
        
        # Add session_id to response
        response['session_id'] = session_id
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@history_bp.route('/chat-stream', methods=['POST'])
def chat_history_stream():
    """Stream chat with meeting history using RAG.
    
    Request:
    {
        "message": "What did we decide about the budget?",
        "session_id": "optional_session_id"
    }
    
    Response: Server-Sent Events (SSE) stream
    - data: {"chunk": "text chunk"}
    - data: {"sources": [...]}
    - data: {"error": "..."}
    - data: {" done": true}
    """
    from flask import Response, stream_with_context
    from backend.rag.conversation_manager import get_conversation_manager
    import json
    
    def generate():
        try:
            engine = get_rag_engine()
            if engine is None:
                yield f'data: {json.dumps({"error": "RAG Engine not available"})}\n\n'
                return
                
            data = request.json
            query = data.get('message', '').strip()
            
            if not query:
                yield f'data: {json.dumps({"error": "Message is required"})}\n\n'
                return
            
            # Get or create session ID
            session_id = data.get('session_id') or request.cookies.get('chat_session_id')
            if not session_id:
                import uuid
                session_id = str(uuid.uuid4())
            
            # Get conversation manager
            conv_manager = get_conversation_manager()
            
            # Get conversation history
            history = conv_manager.get_history(session_id)
            
            # Stream chat with history
            full_answer = ""
            for event_json in engine.chat_stream(query, conversation_history=history):
                yield f'data: {event_json}\n\n'
                
                # Collect answer for saving
                event = json.loads(event_json)
                if "chunk" in event:
                    full_answer += event["chunk"]
            
            # Save to conversation history
            conv_manager.add_message(session_id, "user", query)
            conv_manager.add_message(session_id, "assistant", full_answer)
            
            # Send session_id and done signal
            yield f'data: {json.dumps({"session_id": session_id, "done": True})}\n\n'
            
        except Exception as e:
            print(f"Error in streaming chat: {e}")
            import traceback
            traceback.print_exc()
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )
