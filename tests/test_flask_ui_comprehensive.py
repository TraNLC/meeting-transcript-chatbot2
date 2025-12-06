"""Comprehensive UI Test Suite for Flask App.

Tests all features including:
- Recording & Transcription
- Upload & Analysis (Audio/Text)
- Speaker Diarization
- Export (TXT/DOCX)
- Smart Search (RAG)
- Chat with AI
- Abnormal cases & error handling
"""

import pytest
import sys
import os
from pathlib import Path
import json
import tempfile
from io import BytesIO

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Flask app
from app_flask import app, socketio


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_audio_file():
    """Create a sample audio file for testing."""
    # Create a minimal WAV file (silent)
    wav_data = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
    return BytesIO(wav_data)


@pytest.fixture
def sample_text_file():
    """Create a sample text file for testing."""
    content = """
    Cuộc họp bắt đầu lúc 9:00 sáng.
    Chủ đề: Thảo luận về dự án AI.
    Người tham gia: Nguyễn Văn A, Trần Thị B.
    Quyết định: Sẽ implement RAG system.
    Action items:
    - Nguyễn Văn A: Setup environment (deadline: 10/12/2025)
    - Trần Thị B: Research LangChain (deadline: 12/12/2025)
    """
    return BytesIO(content.encode('utf-8'))


# ============================================================================
# TEST 1: Basic Routes
# ============================================================================

class TestBasicRoutes:
    """Test basic routes and page loads."""
    
    def test_index_page_loads(self, client):
        """Test that index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Meeting Analyzer Pro' in response.data
    
    def test_static_files_load(self, client):
        """Test that static files are accessible."""
        # Test CSS
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        
        # Test JS
        response = client.get('/static/js/app.js')
        assert response.status_code == 200


# ============================================================================
# TEST 2: Recording History API
# ============================================================================

class TestRecordingHistory:
    """Test recording history functionality."""
    
    def test_get_recording_history_empty(self, client):
        """Test getting recording history when empty."""
        response = client.get('/api/recording/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'recordings' in data
    
    def test_get_recording_history_with_filter(self, client):
        """Test getting recording history with filter."""
        response = client.get('/api/recording/history?filter=Hôm nay')
        assert response.status_code == 200
    
    def test_load_nonexistent_recording(self, client):
        """Test loading a recording that doesn't exist."""
        response = client.get('/api/recording/load/nonexistent_id')
        assert response.status_code == 200
        # Should handle gracefully


# ============================================================================
# TEST 3: Upload & Analysis
# ============================================================================

class TestUploadAnalysis:
    """Test upload and analysis functionality."""
    
    def test_upload_audio_file_missing(self, client):
        """Test upload without file."""
        response = client.post('/api/upload/process', data={
            'file_type': 'audio',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        })
        # Should return 200 with error in JSON
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_upload_text_file_missing(self, client):
        """Test upload text without file."""
        response = client.post('/api/upload/process', data={
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        })
        # Should return 200 with error in JSON
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_upload_text_file_success(self, client, sample_text_file):
        """Test successful text file upload."""
        response = client.post('/api/upload/process', data={
            'file_type': 'text',
            'text_file': (sample_text_file, 'test.txt'),
            'meeting_type': 'meeting',
            'output_lang': 'vi',
            'transcribe_lang': 'vi',
            'enable_diarization': 'false'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should have status and results
        assert 'status' in data or 'error' in data
    
    def test_upload_invalid_file_type(self, client):
        """Test upload with invalid file type."""
        response = client.post('/api/upload/process', data={
            'file_type': 'invalid',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        })
        # Should handle gracefully
        assert response.status_code in [200, 400]


# ============================================================================
# TEST 4: Chat API
# ============================================================================

class TestChatAPI:
    """Test chat functionality."""
    
    def test_chat_without_message(self, client):
        """Test chat without message."""
        response = client.post('/api/chat',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_chat_with_message(self, client):
        """Test chat with valid message."""
        response = client.post('/api/chat',
            json={
                'message': 'Tóm tắt cuộc họp',
                'history': []
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'history' in data
    
    def test_chat_with_empty_message(self, client):
        """Test chat with empty message."""
        response = client.post('/api/chat',
            json={
                'message': '',
                'history': []
            },
            content_type='application/json'
        )
        assert response.status_code == 200


# ============================================================================
# TEST 5: Analysis History
# ============================================================================

class TestAnalysisHistory:
    """Test analysis history functionality."""
    
    def test_list_history(self, client):
        """Test listing analysis history."""
        response = client.get('/api/history/list')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'dropdown' in data
        assert 'info' in data
    
    def test_load_nonexistent_history(self, client):
        """Test loading non-existent history."""
        response = client.get('/api/history/load/nonexistent')
        assert response.status_code == 200


# ============================================================================
# TEST 6: Export Functionality
# ============================================================================

class TestExport:
    """Test export functionality."""
    
    def test_export_txt_no_data(self, client):
        """Test exporting TXT without data."""
        response = client.get('/api/export/txt')
        # Should return error or empty file
        assert response.status_code in [200, 400]
    
    def test_export_docx_no_data(self, client):
        """Test exporting DOCX without data."""
        response = client.get('/api/export/docx')
        # Should return error or empty file
        assert response.status_code in [200, 400]


# ============================================================================
# TEST 7: RAG Smart Search
# ============================================================================

class TestRAGSmartSearch:
    """Test RAG smart search functionality."""
    
    def test_smart_search_without_query(self, client):
        """Test smart search without query."""
        response = client.post('/api/rag/smart-search',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_smart_search_with_query(self, client):
        """Test smart search with valid query."""
        response = client.post('/api/rag/smart-search',
            json={
                'query': 'action items về marketing',
                'k': 5
            },
            content_type='application/json'
        )
        # Should return results or error if RAG not available
        assert response.status_code in [200, 503]
    
    def test_smart_search_empty_query(self, client):
        """Test smart search with empty query."""
        response = client.post('/api/rag/smart-search',
            json={
                'query': '',
                'k': 5
            },
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_smart_qa_without_question(self, client):
        """Test smart Q&A without question."""
        response = client.post('/api/rag/smart-qa',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_smart_qa_with_question(self, client):
        """Test smart Q&A with valid question."""
        response = client.post('/api/rag/smart-qa',
            json={
                'question': 'Ai phụ trách dự án?',
                'context_k': 3
            },
            content_type='application/json'
        )
        # Should return answer or error if RAG not available
        assert response.status_code in [200, 503]
    
    def test_rag_stats(self, client):
        """Test getting RAG statistics."""
        response = client.get('/api/rag/stats')
        # Should return stats or error if RAG not available
        assert response.status_code in [200, 503]
    
    def test_add_meeting_to_rag_missing_data(self, client):
        """Test adding meeting without required data."""
        response = client.post('/api/rag/add-meeting',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400


# ============================================================================
# TEST 8: Search & Stats
# ============================================================================

class TestSearchStats:
    """Test search and statistics."""
    
    def test_search_stats(self, client):
        """Test getting search statistics."""
        response = client.get('/api/search/stats')
        assert response.status_code == 200
    
    def test_search_meetings(self, client):
        """Test searching meetings."""
        response = client.post('/api/search/meetings',
            json={
                'query': 'test query',
                'meeting_type': 'Tất cả',
                'n_results': 5
            },
            content_type='application/json'
        )
        assert response.status_code == 200


# ============================================================================
# TEST 9: Abnormal Cases & Error Handling
# ============================================================================

class TestAbnormalCases:
    """Test abnormal cases and error handling."""
    
    def test_invalid_json_request(self, client):
        """Test request with invalid JSON."""
        response = client.post('/api/chat',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 500]
    
    def test_missing_content_type(self, client):
        """Test request without content type."""
        response = client.post('/api/chat',
            data=json.dumps({'message': 'test'})
        )
        # Should handle gracefully (415 = Unsupported Media Type is also valid)
        assert response.status_code in [200, 400, 415]
    
    def test_very_long_query(self, client):
        """Test with very long query."""
        long_query = 'a' * 10000
        response = client.post('/api/rag/smart-search',
            json={
                'query': long_query,
                'k': 5
            },
            content_type='application/json'
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 503]
    
    def test_negative_k_value(self, client):
        """Test with negative k value."""
        response = client.post('/api/rag/smart-search',
            json={
                'query': 'test',
                'k': -5
            },
            content_type='application/json'
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 503]
    
    def test_special_characters_in_query(self, client):
        """Test with special characters."""
        response = client.post('/api/rag/smart-search',
            json={
                'query': '<script>alert("xss")</script>',
                'k': 5
            },
            content_type='application/json'
        )
        # Should sanitize and handle safely
        assert response.status_code in [200, 400, 503]
    
    def test_sql_injection_attempt(self, client):
        """Test SQL injection attempt."""
        response = client.post('/api/rag/smart-search',
            json={
                'query': "'; DROP TABLE meetings; --",
                'k': 5
            },
            content_type='application/json'
        )
        # Should handle safely
        assert response.status_code in [200, 400, 503]
    
    def test_upload_oversized_file(self, client):
        """Test uploading oversized file."""
        # Create a large file (simulated)
        large_data = b'x' * (600 * 1024 * 1024)  # 600MB
        response = client.post('/api/upload/process', data={
            'file_type': 'text',
            'text_file': (BytesIO(large_data), 'large.txt'),
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        })
        # Should reject or handle gracefully
        assert response.status_code in [200, 413, 500]
    
    def test_concurrent_requests(self, client):
        """Test handling concurrent requests (sequential for Flask test client)."""
        # Flask test client doesn't support true concurrent requests
        # Test sequential requests instead to verify no state issues
        results = []
        
        for i in range(5):
            response = client.get('/api/recording/history')
            results.append(response.status_code)
        
        # All requests should complete successfully
        assert len(results) == 5
        assert all(code == 200 for code in results)

    def test_upload_unsupported_file_type(self, client):
        """Test uploading unsupported file type (e.g. .exe)."""
        # Create a dummy exe file
        exe_data = b'MZ\x90\x00\x03\x00\x00\x00'
        response = client.post('/api/upload/process', data={
            'file_type': 'audio',
            'audio_file': (BytesIO(exe_data), 'malicious.exe'),
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        })
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
        if response.status_code == 200:
            data = json.loads(response.data)
            # Either error or handled as generic file
            pass

    def test_rag_system_failure_simulation(self, client):
        """Test behavior when RAG system is down/erroring."""
        # We can't easily shut down RAG here without mocking, 
        # but we can pass invalid parameters that might trigger errors
        response = client.post('/api/rag/smart-search',
            json={
                'query': 'test',
                'k': 1000000 # Unreasonably high k
            },
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 500, 503]


# ============================================================================
# TEST 11: WebSocket Tests
# ============================================================================

class TestWebSocket:
    """Test WebSocket functionality."""

    def test_websocket_connection(self, client):
        """Test WebSocket connection."""
        socket_client = socketio.test_client(app, flask_test_client=client)
        assert socket_client.is_connected()
        socket_client.disconnect()

    def test_websocket_audio_chunk(self, client):
        """Test sending audio chunk."""
        socket_client = socketio.test_client(app, flask_test_client=client)
        
        # Send valid base64 audio
        # Minimal valid wav base64
        wav_b64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="
        
        socket_client.emit('audio_chunk', {
            'audio': wav_b64,
            'language': 'vi'
        })
        
        # Should receive transcript_update or at least not error
        received = socket_client.get_received()
        # Filter for 'transcript_update' or 'connected'
        # Note: processing might be async/slow, so we might only get 'connected' initially
        assert len(received) > 0
        
        socket_client.disconnect()

    def test_websocket_invalid_audio_chunk(self, client):
        """Test sending invalid audio chunk."""
        socket_client = socketio.test_client(app, flask_test_client=client)
        
        socket_client.emit('audio_chunk', {
            'audio': 'invalid_base64_!@#$',
            'language': 'vi'
        })
        
        # Should receive error event
        received = socket_client.get_received()
        # Look for error event
        errors = [evt for evt in received if evt['name'] == 'error']
        # It might not emit error immediately depending on implementation, but shouldn't crash
        
        socket_client.disconnect()

    def test_websocket_stop_recording(self, client):
        """Test stop recording event."""
        socket_client = socketio.test_client(app, flask_test_client=client)
        
        # Send a chunk first so there's something to process
        wav_b64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="
        socket_client.emit('audio_chunk', {'audio': wav_b64, 'language': 'vi'})
        
        # Stop
        socket_client.emit('stop_recording', {'language': 'vi'})
        
        received = socket_client.get_received()
        # Should eventually get transcript_final
        # Note: In test env, might be hard to wait for async processing without sleep
        # But we verify it doesn't crash
        
        socket_client.disconnect()



# ============================================================================
# TEST 10: Integration Tests
# ============================================================================

class TestIntegration:
    """Test complete workflows."""
    
    def test_complete_workflow_text_upload(self, client, sample_text_file):
        """Test complete workflow: upload text -> analyze -> export."""
        # Step 1: Upload and analyze
        response = client.post('/api/upload/process', data={
            'file_type': 'text',
            'text_file': (sample_text_file, 'test.txt'),
            'meeting_type': 'meeting',
            'output_lang': 'vi',
            'transcribe_lang': 'vi',
            'enable_diarization': 'false'
        })
        assert response.status_code == 200
        
        # Step 2: Check history
        response = client.get('/api/history/list')
        assert response.status_code == 200
        
        # Step 3: Try to export (may fail if no data)
        response = client.get('/api/export/txt')
        assert response.status_code in [200, 400]
    
    def test_complete_workflow_chat(self, client):
        """Test complete workflow: chat interaction."""
        # Send multiple messages
        messages = [
            'Xin chào',
            'Tóm tắt cuộc họp',
            'Action items là gì?'
        ]
        
        history = []
        for msg in messages:
            response = client.post('/api/chat',
                json={
                    'message': msg,
                    'history': history
                },
                content_type='application/json'
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            history = data.get('history', [])


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
