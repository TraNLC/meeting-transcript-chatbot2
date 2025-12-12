
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.data.history_searcher import HistorySearcher
    print("Starting reindex...")
    searcher = HistorySearcher()
    count = searcher.index_all_meetings(force_reindex=True)
    print(f"DONE: Indexed {count} meetings.")
except Exception as e:
    print(f"Error: {e}")
