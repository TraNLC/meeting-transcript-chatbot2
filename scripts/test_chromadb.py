"""Test ChromaDB to see if data exists."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.vectorstore.chroma_manager import ChromaManager

manager = ChromaManager()

print("Testing ChromaDB...")
print()

# Test get_statistics
stats = manager.get_statistics()
print(f"Statistics: {stats}")
print()

# Test get_all_meetings
meetings = manager.get_all_meetings()
print(f"Total meetings from get_all_meetings: {len(meetings)}")
print()

# Test collection directly
result = manager.collection.get()
print(f"Total IDs in collection: {len(result['ids'])}")
print(f"First 5 IDs: {result['ids'][:5]}")
print()

# Test count
count = manager.collection.count()
print(f"Collection count: {count}")
