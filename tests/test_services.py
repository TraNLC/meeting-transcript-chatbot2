import pytest
from unittest.mock import MagicMock, patch
from app.services.audio_service import AudioService

@patch('faster_whisper.WhisperModel')
def test_audio_service_loading(mock_whisper_cls):
    """Test that model loads strictly once"""
    service = AudioService()
    # Reset singleton/instance for test if possible or checks state
    # Since it's a singleton, it might be already loaded if other tests ran.
    # We can force reset:
    service._whisper_model = None
    
    model = service.whisper_model
    assert model is not None
    mock_whisper_cls.assert_called_once()
    
    # Second access should not init again
    model2 = service.whisper_model
    mock_whisper_cls.assert_called_once() # Count remains 1

@patch('app.services.audio_service.SpeakerDiarizer')
def test_diarizer_loading(mock_diarizer_cls):
    service = AudioService()
    service._diarizer = None
    
    d = service.diarizer
    mock_diarizer_cls.assert_called_once()

@patch('faster_whisper.WhisperModel')
def test_transcribe_realtime(mock_whisper_cls):
    service = AudioService()
    service._whisper_model = MagicMock() # Mock the instance
    
    service._whisper_model.transcribe.return_value = (['seg1'], 'info')
    
    res = service.transcribe_realtime("dummy.wav")
    assert res == ['seg1']
