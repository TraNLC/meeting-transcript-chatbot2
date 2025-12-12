
import sys
import json
from pathlib import Path

# Ensure backend imports work
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.rag.rag_engine import RAGEngine
    
    print("Testing RAGEngine...")
    engine = RAGEngine()
    
    # Test queries
    queries = [
        "What key decisions were made about recruitment?",
        "Is there any discussion about AWS vs Google Cloud?",
        "Summarize the marketing strategy launch."
    ]
    
    for q in queries:
        print(f"\nQUERY: {q}")
        response = engine.chat(q)
        print(f"ANSWER:\n{response['answer']}")
        print(f"SOURCES: {len(response['sources'])}")
        for s in response['sources']:
            print(f"  - {s['name']} (Score: {s['score']:.2f})")
            
except Exception as e:
    print(f"Error: {e}")
