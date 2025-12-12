
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.data.history_searcher import HistorySearcher
    searcher = HistorySearcher()
    
    query = "budget planning"
    print(f"Searching for: '{query}'")
    results = searcher.semantic_search(query, top_k=3)
    
    print(f"Found {len(results)} results:")
    for r in results:
        print(f"- {r['metadata'].get('original_file')} (Score: {r['score']:.2f})")
        
except Exception as e:
    print(f"Error: {e}")
