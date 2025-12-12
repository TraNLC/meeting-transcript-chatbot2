"""
History Semantic Searcher using ChromaDB.

Smart ChromaDB usage:
- Separate collection for meeting history
- Metadata filtering for efficient queries
- Batch operations for indexing
- Incremental updates
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import threading

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class HistorySearcher:
    """Semantic search over meeting history using ChromaDB."""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HistorySearcher, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self, history_dir: str = "data/history", collection_name: str = "meeting_history"):
        """Initialize History Searcher."""
        if self.initialized:
            return

        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        if chromadb is None:
            raise ImportError("chromadb not installed. Run: pip install chromadb")
        
        # Create persistent ChromaDB client
        chroma_dir = Path("data/chroma_history")
        chroma_dir.mkdir(parents=True, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=str(chroma_dir))
        
        # Get or create collection for meeting history
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Meeting history for semantic search", "hnsw:space": "cosine"}
        )
        
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers not installed")
        
        # Model lazy loading/preloading
        self.model = None
        self.model_lock = threading.Lock()
        self.initialized = True
        
        # Start preloading in background
        print(f"[HistorySearcher] Starting background model load...")
        threading.Thread(target=self._preload_model, daemon=True).start()
        
        print(f"[OK] HistorySearcher initialized")
        print(f"     Collection: {self.collection_name}")
        try:
            print(f"     Existing documents: {self.collection.count()}")
        except:
            pass

    def _preload_model(self):
        """Load model into memory in background."""
        try:
            with self.model_lock:
                if self.model is None:
                    print("[HistorySearcher] Preloading AI model (all-MiniLM-L6-v2)...")
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                    print("[HistorySearcher] AI Model loaded successfully!")
        except Exception as e:
            print(f"[HistorySearcher] Model load failed: {e}")

    def _get_model(self):
        """Get model, loading if likely not yet ready (fallback)."""
        with self.model_lock:
            if self.model is None:
                print("[HistorySearcher] Model not ready/preloaded. Loading now (blocking)...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model
    
    def _create_search_document(self, meeting_data: Dict) -> str:
        """Create searchable document from meeting data."""
        parts = []
        if meeting_data.get('summary'): parts.append(f"Summary: {meeting_data['summary']}")
        
        # Topics: handle both list of strings and list of dicts
        if meeting_data.get('topics'):
            topics = meeting_data['topics']
            if isinstance(topics, list) and topics:
                if isinstance(topics[0], str):
                    # List of strings
                    topics_text = ", ".join(topics)
                else:
                    # List of dicts
                    topics_text = ", ".join([f"{t.get('topic', '')} - {t.get('description', '')}" for t in topics])
                parts.append(f"Topics: {topics_text}")
        
        # Action items: handle both formats
        if meeting_data.get('action_items'):
            actions = meeting_data['action_items']
            if isinstance(actions, list) and actions:
                if isinstance(actions[0], str):
                    actions_text = ", ".join(actions)
                else:
                    actions_text = ", ".join([f"{a.get('task', '')} ({a.get('assignee', '')})" for a in actions])
                parts.append(f"Actions: {actions_text}")
        
        # Decisions: handle both formats
        if meeting_data.get('decisions'):
            decisions = meeting_data['decisions']
            if isinstance(decisions, list) and decisions:
                if isinstance(decisions[0], str):
                    decisions_text = ", ".join(decisions)
                else:
                    decisions_text = ", ".join([f"{d.get('decision', '')} - {d.get('context', '')}" for d in decisions])
                parts.append(f"Decisions: {decisions_text}")
        
        return " ".join(parts)
    
    def _extract_metadata(self, meeting_data: Dict) -> Dict:
        """Extract metadata for ChromaDB filtering."""
        metadata = {
            "meeting_id": meeting_data.get('id', ''),
            "original_file": meeting_data.get('original_file', ''),
            "timestamp": meeting_data.get('timestamp', ''),
            "meeting_type": meeting_data.get('metadata', {}).get('meeting_type', 'meeting')
        }
        if meeting_data.get('metadata', {}).get('language'):
            metadata['language'] = meeting_data['metadata']['language']
        return metadata
    
    def index_single_meeting(self, meeting_id: str, meeting_data: Dict) -> bool:
        """Index a single meeting into ChromaDB."""
        try:
            doc_text = self._create_search_document(meeting_data)
            if not doc_text.strip(): return False
            
            metadata = self._extract_metadata(meeting_data)
            embedding = self._get_model().encode(doc_text).tolist()
            
            self.collection.upsert(
                ids=[meeting_id],
                embeddings=[embedding],
                documents=[doc_text],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            print(f"[ERROR] Failed to index {meeting_id}: {e}")
            return False
    
    def index_all_meetings(self, force_reindex: bool = False) -> int:
        """Index all meetings from history directory."""
        print(f"\n[INFO] Indexing meetings from {self.history_dir}")
        history_files = list(self.history_dir.glob("*.json"))
        if not history_files: return 0
        
        ids_batch, embeddings_batch, documents_batch, metadatas_batch = [], [], [], []
        indexed_count = 0
        
        for history_file in history_files:
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    meeting_data = json.load(f)
                
                meeting_id = meeting_data.get('id', history_file.stem)
                
                if not force_reindex:
                    existing = self.collection.get(ids=[meeting_id])
                    if existing['ids']: continue
                
                doc_text = self._create_search_document(meeting_data)
                if not doc_text.strip(): continue
                
                metadata = self._extract_metadata(meeting_data)
                embedding = self._get_model().encode(doc_text).tolist()
                
                ids_batch.append(meeting_id)
                embeddings_batch.append(embedding)
                documents_batch.append(doc_text)
                metadatas_batch.append(metadata)
                
                if len(ids_batch) >= 100:
                    self.collection.upsert(
                        ids=ids_batch,
                        embeddings=embeddings_batch,
                        documents=documents_batch,
                        metadatas=metadatas_batch
                    )
                    indexed_count += len(ids_batch)
                    print(f"[OK] Indexed batch: {indexed_count} meetings")
                    ids_batch, embeddings_batch, documents_batch, metadatas_batch = [], [], [], []
                
            except Exception as e:
                print(f"[ERROR] Failed to process {history_file}: {e}")
                continue
        
        if ids_batch:
            self.collection.upsert(
                ids=ids_batch,
                embeddings=embeddings_batch,
                documents=documents_batch,
                metadatas=metadatas_batch
            )
            indexed_count += len(ids_batch)
        
        print(f"   Indexed: {indexed_count} meetings")
        return indexed_count

    def semantic_search(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """Perform semantic search."""
        try:
            if not query.strip(): return []
            
            embedding = self._get_model().encode(query).tolist()
            
            search_args = {
                "query_embeddings": [embedding],
                "n_results": top_k
            }
            if filters: search_args["where"] = filters
            
            results = self.collection.query(**search_args)
            
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'score': 1 - results['distances'][0][i] if 'distances' in results else 0,
                        'matched_text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"[ERROR] Semantic search failed: {e}")
            return []
