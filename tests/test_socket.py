import pytest
from unittest.mock import MagicMock, patch

def test_socket_connection(socket_client):
    """Test WebSocket connection establishment"""
    assert socket_client.is_connected()
    received = socket_client.get_received()
    # Expect 'connected' event
    assert len(received) > 0
    assert received[0]['name'] == 'connected'

@patch('app.services.audio_service.AudioService.transcribe_realtime')
def test_socket_audio_chunk(mock_transcribe, socket_client):
    """Test sending audio chunk and receiving transcript update"""
    # Mock segment return
    Segment = MagicMock()
    Segment.text = "Hello world"
    Segment.start = 0.0
    Segment.end = 1.0
    mock_transcribe.return_value = [Segment]
    
    # Send base64 dummy audio
    socket_client.emit('audio_chunk', {'audio': 'AAA=', 'language': 'en'})
    
    received = socket_client.get_received()
    # Filter for transcript_update
    updates = [e for e in received if e['name'] == 'transcript_update']
    assert len(updates) > 0
    data = updates[0]['args'][0]
    assert 'segments' in data
    assert data['segments'][0]['text'] == "Hello world"
