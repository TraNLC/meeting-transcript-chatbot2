import pytest
from unittest.mock import patch, mock_open

def test_index_route(client):
    """Test the main page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Meeting Analyzer Pro" in response.data

@patch('app.blueprints.api_recording.load_selected_recording')
def test_load_recording(mock_load, client):
    """Test loading a specific recording"""
    # Mock return: audio_path, transcript, info
    mock_load.return_value = ('path/to/audio', 'Sample Transcript', 'INFO')
    
    response = client.get('/api/recording/load/rec_001')
    assert response.status_code == 200
    data = response.get_json()
    assert data['transcript'] == 'Sample Transcript'

def test_recording_history(client):
    """Test listing recordings (depends on metadata.json existence or mock it)"""
    with patch('builtins.open', mock_open(read_data='{"recordings": [{"id": "1", "category": "recording"}]}')) as mock_file:
        response = client.get('/api/recording/history?category=recording')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['recordings']) == 1
        assert data['recordings'][0]['id'] == '1'

@patch('app.blueprints.api_export.export_to_txt')
@patch('os.path.exists')
def test_export_txt(mock_exists, mock_export, client):
    """Test export functionality"""
    mock_export.return_value = '/tmp/test.txt'
    mock_exists.return_value = True
    
    # We need to mock send_file behavior or just check it calls it. 
    # Flask send_file tries to open the file.
    with patch('app.blueprints.api_export.send_file') as mock_send_file:
        mock_send_file.return_value = 'File Content'
        
        response = client.post('/api/export/txt', json={'content': 'Hello'})
        assert response.status_code == 200
