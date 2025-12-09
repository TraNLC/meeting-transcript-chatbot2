
import unittest
import sys
import os
import json
from io import BytesIO
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestRecordingFlowMock(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.blueprints.api_upload.process_upload') 
    def test_mock_analysis_flow_success(self, mock_process_upload):
        """
        Detailed Mock Test:
        Simulate the 'Analyze Now' button click sending an audio blob.
        Verify the backend handles it and returns the correct JSON structure for the UI.
        """
        # 1. Setup Mock Return Value (Tuple of 7 items as expected by endpoint)
        mock_process_upload.return_value = (
            '✅ Success', 
            'Mock Transcript', 
            'Mock Summary', 
            ['Topic A'], 
            ['Action B'], 
            ['Decision C'], 
            ['Participant D']
        )

        # 2. Creating a dummy audio file (simulating the Blob from frontend)
        data = {
            'audio_file': (BytesIO(b'fake_audio_content'), 'browser_recording.webm'),
            'transcribe_lang': 'vi',
            'output_lang': 'vi',
            'meeting_type': 'meeting',
            'file_type': 'audio'
        }

        # 3. Trigger the Endpoint
        response = self.client.post('/api/upload/process', data=data, content_type='multipart/form-data')

        # 4. Detailed Assertions
        self.assertEqual(response.status_code, 200, "Backend should acknowledge request")
        
        json_data = response.get_json()
        
        # Verify Keys needed by Frontend 'renderResult' function
        self.assertIn('status', json_data)
        self.assertTrue(json_data['status'].startswith('✅'))
        
        self.assertIn('summary', json_data)
        self.assertEqual(json_data['summary'], 'Mock Summary')
        
        # Verify Mock was called correctly
        mock_process_upload.assert_called_once()
        print("\n[MockTest] Success Flow Verified: Backend correctly bridged Frontend -> Analyzer -> Frontend")

    @patch('app.blueprints.api_upload.process_upload')
    def test_mock_analysis_flow_failure(self, mock_process_upload):
        """
        Detailed Mock Test:
        Simulate a backend processing error.
        Verify frontend receives correct error structure.
        """
        # 1. Setup Mock to Raise Exception
        mock_process_upload.side_effect = Exception("Mocked Processing Error")

        # 2. Dummy Data
        data = {
            'audio_file': (BytesIO(b'fake'), 'error.webm'),
            'file_type': 'audio'
        }

        # 3. Trigger
        response = self.client.post('/api/upload/process', data=data, content_type='multipart/form-data')

        # 4. Assertions
        # Expect 500 because exception raised inside try/except block of route
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Mocked Processing Error', response.data)
             
        print("\n[MockTest] Failure Flow Verified: Exception correctly propagated to UI")

class TestRecordingPages(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_browser_recording_page_loads(self):
        """Test that /browser_recording loads successfully."""
        response = self.client.get('/browser_recording')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Akari AI', response.data)
        # Check for key UI elements
        self.assertIn(b'setupSection', response.data)
        self.assertIn(b'recordingSection', response.data)
        self.assertIn(b'resultSection', response.data)
        self.assertIn(b'colabUrlInput', response.data)

    def test_mic_recording_page_loads(self):
        """Test that /mic_recording loads successfully."""
        response = self.client.get('/mic_recording')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Akari AI', response.data)
        # Check for key UI elements
        self.assertIn(b'setupSection', response.data)
        self.assertIn(b'recordingSection', response.data)
        self.assertIn(b'resultSection', response.data)
        self.assertIn(b'visualizerBars', response.data)

    def test_browser_recording_flow_structure(self):
        """Check flow logic elements in Browser Recording page."""
        response = self.client.get('/browser_recording')
        html = response.data.decode('utf-8')
        
        # Verify Manual Flow Logic existence
        self.assertIn('handleRecordingStopped', html)
        self.assertIn('startAnalysis', html)
        # Verify Backend Endpoint
        self.assertIn('/api/upload/process', html)
        
    def test_mic_recording_flow_structure(self):
        """Check flow logic elements in Mic Recording page."""
        response = self.client.get('/mic_recording')
        html = response.data.decode('utf-8')
        
        # Verify Manual Flow Logic existence
        self.assertIn('handleRecordingStopped', html)
        self.assertIn('startAnalysis', html)
        self.assertIn('/api/upload/process', html)

if __name__ == '__main__':
    unittest.main()
