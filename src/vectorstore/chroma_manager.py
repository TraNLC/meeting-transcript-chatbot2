"""ChromaDB manager for semantic search and meeting storage."""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class ChromaManager:
    """Manages ChromaDB vector storage for meetings and workshops."""
    
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="meetings",
            metadata={"description": "Meeting transcripts and analysis"}
        )
        
        # Initialize sentence transformer for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def store_meeting(
        self,
        meeting_id: str,
        transcript: str,
        analysis: Dict[str, Any],
        meeting_type: str = "meeting",
        language: str = "en"
    ) -> bool:
        """Store meeting transcript and analysis with vector embeddings.
        
        Args:
            meeting_id: Unique identifier for the meeting
            transcript: Full meeting transcript
            analysis: Analysis results from universal_executor
            meeting_type: Type of meeting (meeting, workshop, brainstorming)
            language: Language code (en, vi, ja, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate embedding from transcript
            embedding = self.encoder.encode(transcript).tolist()
            
            # Prepare metadata
            metadata = {
                "meeting_type": meeting_type,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "transcript_length": len(transcript),
                "has_participants": bool(analysis.get("participants")),
                "has_action_items": bool(analysis.get("action_items")),
                "has_decisions": bool(analysis.get("decisions"))
            }
            
            # Add workshop-specific metadata
            if meeting_type == "workshop":
                metadata.update({
                    "has_key_learnings": bool(analysis.get("key_learnings")),
                    "has_exercises": bool(analysis.get("exercises")),
                    "has_qa_pairs": bool(analysis.get("qa_pairs"))
                })
            
            # Store in ChromaDB
            self.collection.add(
                ids=[meeting_id],
                embeddings=[embedding],
                documents=[transcript],
                metadatas=[metadata]
            )
            
            # Store full analysis separately (ChromaDB metadata has size limits)
            self._store_analysis(meeting_id, analysis)
            
            return True
            
        except Exception as e:
            print(f"Error storing meeting: {e}")
            return False
    
    def _store_analysis(self, meeting_id: str, analysis: Dict[str, Any]):
        """Store full analysis in JSON file (ChromaDB metadata has size limits)."""
        analysis_dir = os.path.join(self.persist_directory, "analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        analysis_path = os.path.join(analysis_dir, f"{meeting_id}.json")
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    def _load_analysis(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """Load full analysis from JSON file."""
        analysis_path = os.path.join(self.persist_directory, "analysis", f"{meeting_id}.json")
        if os.path.exists(analysis_path):
            with open(analysis_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def semantic_search(
        self,
        query: str,
        n_results: int = 5,
        meeting_type: Optional[str] = None,
        language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Perform semantic search on stored meetings.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            meeting_type: Filter by meeting type (optional)
            language: Filter by language (optional)
            
        Returns:
            List of matching meetings with metadata and analysis
        """
        try:
            # Generate query embedding
            query_embedding = self.encoder.encode(query).tolist()
            
            # Build where filter
            where_filter = {}
            if meeting_type:
                where_filter["meeting_type"] = meeting_type
            if language:
                where_filter["language"] = language
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter if where_filter else None
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i, meeting_id in enumerate(results['ids'][0]):
                    result = {
                        "meeting_id": meeting_id,
                        "transcript": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None,
                        "analysis": self._load_analysis(meeting_id)
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
    
    def find_similar_meetings(
        self,
        meeting_id: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Find meetings similar to a given meeting.
        
        Args:
            meeting_id: ID of the reference meeting
            n_results: Number of similar meetings to return
            
        Returns:
            List of similar meetings
        """
        try:
            # Get the reference meeting
            result = self.collection.get(ids=[meeting_id])
            if not result['documents']:
                return []
            
            transcript = result['documents'][0]
            
            # Use the transcript as query
            return self.semantic_search(transcript, n_results=n_results + 1)[1:]  # Exclude self
            
        except Exception as e:
            print(f"Error finding similar meetings: {e}")
            return []
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific meeting by ID.
        
        Args:
            meeting_id: Meeting identifier
            
        Returns:
            Meeting data with transcript, metadata, and analysis
        """
        try:
            result = self.collection.get(ids=[meeting_id])
            if result['ids']:
                return {
                    "meeting_id": meeting_id,
                    "transcript": result['documents'][0],
                    "metadata": result['metadatas'][0],
                    "analysis": self._load_analysis(meeting_id)
                }
            return None
        except Exception as e:
            print(f"Error getting meeting: {e}")
            return None
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting from the vector store.
        
        Args:
            meeting_id: Meeting identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[meeting_id])
            
            # Delete analysis file
            analysis_path = os.path.join(self.persist_directory, "analysis", f"{meeting_id}.json")
            if os.path.exists(analysis_path):
                os.remove(analysis_path)
            
            return True
        except Exception as e:
            print(f"Error deleting meeting: {e}")
            return False
    
    def get_all_meetings(self) -> List[Dict[str, Any]]:
        """Get all stored meetings.
        
        Returns:
            List of all meetings with metadata
        """
        try:
            result = self.collection.get()
            meetings = []
            for i, meeting_id in enumerate(result['ids']):
                meetings.append({
                    "meeting_id": meeting_id,
                    "metadata": result['metadatas'][i],
                    "transcript_preview": result['documents'][i][:200] + "..."
                })
            return meetings
        except Exception as e:
            print(f"Error getting all meetings: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored meetings.
        
        Returns:
            Dictionary with statistics
        """
        try:
            all_meetings = self.collection.get()
            total = len(all_meetings['ids'])
            
            # Count by type
            type_counts = {}
            language_counts = {}
            
            for metadata in all_meetings['metadatas']:
                meeting_type = metadata.get('meeting_type', 'unknown')
                language = metadata.get('language', 'unknown')
                
                type_counts[meeting_type] = type_counts.get(meeting_type, 0) + 1
                language_counts[language] = language_counts.get(language, 0) + 1
            
            return {
                "total_meetings": total,
                "by_type": type_counts,
                "by_language": language_counts
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {"total_meetings": 0, "by_type": {}, "by_language": {}}
