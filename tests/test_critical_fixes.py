import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestCriticalFixes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_upload_page_render(self):
        """Verify upload.html no longer has TemplateSyntaxError"""
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200, "Upload page should render 200 OK")
        self.assertIn(b'Upload', response.data)

    def test_recording_redirects(self):
        """Verify legacy routes redirect correctly"""
        # Browser redirect
        response = self.client.get('/recording/browser')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/browser_recording'))

        # Mic redirect
        response = self.client.get('/recording/mic')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/mic_recording'))

if __name__ == '__main__':
    unittest.main()
