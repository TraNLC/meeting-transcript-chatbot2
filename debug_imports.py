
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")

try:
    import chromadb
    print("SUCCESS: import chromadb")
except ImportError as e:
    print(f"ERROR: import chromadb failed: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("SUCCESS: from sentence_transformers import SentenceTransformer")
except ImportError as e:
    print(f"ERROR: from sentence_transformers import SentenceTransformer failed: {e}")

try:
    import backend.data.history_searcher
    print("SUCCESS: import backend.data.history_searcher")
except ImportError as e:
    print(f"ERROR: import backend.data.history_searcher failed: {e}")
