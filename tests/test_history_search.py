"""
Test suite for History Semantic Search functionality.

Tests ChromaDB-based semantic search over meeting history.
Run: pytest tests/test_history_search.py -v -s
"""

import pytest
import json
import tempfile
import shutil
import time
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure project root is in path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try importing backend classes strictly
try:
    from backend.data.history_searcher import HistorySearcher
except ImportError as e:
    print(f"!!! CRITICAL IMPORT ERROR: {e}")
    # Retrying with debug prints
    import traceback
    traceback.print_exc()
    raise e

@pytest.fixture
def temp_dirs():
    """Create temporary directories for history and chroma."""
    base_dir = tempfile.mkdtemp()
    history_dir = Path(base_dir) / "data" / "history"
    chroma_dir = Path(base_dir) / "data" / "chroma_history"
    
    history_dir.mkdir(parents=True)
    
    yield str(history_dir), str(chroma_dir)
    
    shutil.rmtree(base_dir)

@pytest.fixture
def sample_meetings():
    """Create sample meeting data for testing."""
    meetings = [
        {
            "id": "20251201_meeting1",
            "timestamp": "2025-12-01T10:00:00",
            "original_file": "budget_planning.txt",
            "meeting_type": "meeting",
            "summary": "Discussed Q4 budget planning and resource allocation for next year.",
            "topics": [
                {"topic": "Budget Planning", "description": "Reviewed budget for Q4"},
                {"topic": "Resource Allocation", "description": "Assigned team members to projects"}
            ],
            "action_items": [
                {"task": "Submit budget proposal", "assignee": "John", "deadline": "2025-12-15"}
            ],
            "decisions": [
                {"decision": "Increase marketing budget by 15%", "context": "Based on ROI analysis"}
            ]
        },
        {
            "id": "20251202_interview1",
            "timestamp": "2025-12-02T14:00:00",
            "original_file": "candidate_interview.txt",
            "meeting_type": "interview",
            "summary": "Interview with senior developer candidate. Strong backend skills, good cultural fit.",
            "topics": [
                {"topic": "Technical Skills", "description": "Discussed Python and system design"},
                {"topic": "Team Fit", "description": "Evaluated communication and collaboration"}
            ],
            "action_items": [
                {"task": "Send offer letter", "assignee": "HR", "deadline": "2025-12-05"}
            ],
            "decisions": [
                {"decision": "Move to final round", "context": "Passed technical assessment"}
            ]
        },
        {
            "id": "20251203_meeting2",
            "timestamp": "2025-12-03T09:00:00",
            "original_file": "sprint_planning.txt",
            "meeting_type": "meeting",
            "summary": "Sprint planning for December. Prioritized features and assigned tasks.",
            "topics": [
                {"topic": "Sprint Goals", "description": "Defined sprint objectives"},
                {"topic": "Task Assignment", "description": "Distributed work among team"}
            ],
            "action_items": [
                {"task": "Implement user authentication", "assignee": "Alice", "deadline": "2025-12-10"},
                {"task": "Design database schema", "assignee": "Bob", "deadline": "2025-12-08"}
            ],
            "decisions": [
                {"decision": "Use JWT for authentication", "context": "Security requirements"}
            ]
        }
    ]
    return meetings

@pytest.fixture
def reset_singleton():
    """Reset HistorySearcher singleton."""
    HistorySearcher._instance = None
    yield
    HistorySearcher._instance = None

class TestHistorySearcher:
    """Test HistorySearcher functionality."""

    def test_initialization(self, temp_dirs, reset_singleton):
        """Test HistorySearcher initialization."""
        history_dir, chroma_dir = temp_dirs
        
        with patch("chromadb.PersistentClient") as mock_client_cls:
            searcher = HistorySearcher(history_dir=history_dir, collection_name="test_collection")
            
            assert searcher.history_dir == Path(history_dir)
            assert searcher.collection_name == "test_collection"
            mock_client_cls.assert_called_once()
            searcher.chroma_client.get_or_create_collection.assert_called_with(
                name="test_collection",
                metadata={"description": "Meeting history for semantic search", "hnsw:space": "cosine"}
            )

    @patch("chromadb.PersistentClient")
    def test_index_single_meeting(self, mock_client_cls, temp_dirs, sample_meetings, reset_singleton):
        """Test indexing a single meeting."""
        history_dir, _ = temp_dirs
        
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_client_cls.return_value = mock_client
        
        searcher = HistorySearcher(history_dir=history_dir)
        searcher.model = MagicMock()
        searcher.model.encode.return_value.tolist.return_value = [0.1, 0.2, 0.3]
        
        meeting = sample_meetings[0]
        success = searcher.index_single_meeting(meeting['id'], meeting)
        
        assert success is True
        mock_collection.upsert.assert_called_once()
        
        call_args = mock_collection.upsert.call_args[1]
        assert call_args['ids'] == [meeting['id']]
        assert len(call_args['embeddings'][0]) == 3

    @patch("chromadb.PersistentClient")
    def test_index_all_meetings(self, mock_client_cls, temp_dirs, sample_meetings, reset_singleton):
        """Test batch indexing all meetings."""
        history_dir_path, _ = temp_dirs
        history_dir = Path(history_dir_path)
        
        for m in sample_meetings:
            with open(history_dir / f"{m['id']}.json", 'w') as f:
                json.dump(m, f)
        
        mock_collection = MagicMock()
        mock_collection.get.return_value = {'ids': []} 
        
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_client_cls.return_value = mock_client
        
        searcher = HistorySearcher(history_dir=history_dir_path)
        searcher.model = MagicMock()
        searcher.model.encode.return_value.tolist.return_value = [0.1]*384
        
        count = searcher.index_all_meetings(force_reindex=True)
        
        assert count == 3
        assert mock_collection.upsert.called

    @patch("chromadb.PersistentClient")
    def test_semantic_search_logic(self, mock_client_cls, temp_dirs, reset_singleton):
        """Test semantic search query construction and result parsing."""
        history_dir, _ = temp_dirs
        
        mock_results = {
            'ids': [['meet1', 'meet2']],
            'distances': [[0.2, 0.5]],
            'documents': [['Doc 1', 'Doc 2']],
            'metadatas': [[{'type': 'meeting'}, {'type': 'interview'}]]
        }
        
        mock_collection = MagicMock()
        mock_collection.query.return_value = mock_results
        
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_client_cls.return_value = mock_client
        
        searcher = HistorySearcher(history_dir=history_dir)
        searcher.model = MagicMock()
        searcher.model.encode.return_value.tolist.return_value = [0.1]*384
        
        results = searcher.semantic_search("test query", top_k=2)
        
        assert len(results) == 2
        assert results[0]['id'] == 'meet1'
        assert results[0]['score'] == 0.8 # 1 - 0.2
        
        mock_collection.query.assert_called_once()

    @patch("chromadb.PersistentClient")
    def test_metadata_filtering(self, mock_client_cls, temp_dirs, reset_singleton):
        """Test filtering logic passed to ChromaDB."""
        history_dir, _ = temp_dirs
        
        mock_collection = MagicMock()
        mock_collection.query.return_value = {'ids': [], 'distances': [], 'documents': [], 'metadatas': []}
        
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_client_cls.return_value = mock_client
        
        searcher = HistorySearcher(history_dir=history_dir)
        searcher.model = MagicMock()
        searcher.model.encode.return_value.tolist.return_value = [0.1]*384
        
        filters = {"meeting_type": "interview"}
        searcher.semantic_search("query", filters=filters)
        
        call_kwargs = mock_collection.query.call_args[1]
        assert call_kwargs['where'] == filters

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
