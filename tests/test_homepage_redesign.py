"""
Test Cases for Homepage Redesign
Tests the new 4-button logic:
1. Ghi âm (record only, save to history)
2. Phân tích ghi âm (upload audio → analyze)
3. Phân tích văn bản (upload txt/docx/PDF → analyze)
4. Lịch sử (history - unchanged)
"""

import unittest
import requests
import json
from pathlib import Path
import time

BASE_URL = "http://localhost:5000"

class TestHomepageRedesign(unittest.TestCase):
    """Test new homepage button logic"""
    
    def setUp(self):
        """Setup test environment"""
        self.base_url = BASE_URL
        self.test_data_dir = Path("tests/test_data")
        self.test_data_dir.mkdir(parents=True, exist_ok=True)
    
    def test_01_homepage_loads(self):
        """Test 1: Homepage loads successfully"""
        print("\n[TEST 1] Testing homepage loads...")
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ghi âm", response.text)
        self.assertIn("Phân tích ghi âm", response.text)
        self.assertIn("Phân tích văn bản", response.text)
        self.assertIn("Lịch sử", response.text)
        print("✅ Homepage loads with 4 buttons")
    
    def test_02_record_page_loads(self):
        """Test 2: Record page loads (Button 1)"""
        print("\n[TEST 2] Testing record page loads...")
        response = requests.get(f"{self.base_url}/record")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ghi âm cuộc họp", response.text)
        self.assertIn("Micro", response.text)
        self.assertIn("Trình duyệt", response.text)
        print("✅ Record page loads with mic + browser tabs")
    
    def test_03_analyze_audio_page_loads(self):
        """Test 3: Analyze audio page loads (Button 2)"""
        print("\n[TEST 3] Testing analyze audio page loads...")
        response = requests.get(f"{self.base_url}/analyze-audio")
        self.assertEqual(response.status_code, 200)
        print("✅ Analyze audio page loads")
    
    def test_04_analyze_text_page_loads(self):
        """Test 4: Analyze text page loads (Button 3)"""
        print("\n[TEST 4] Testing analyze text page loads...")
        response = requests.get(f"{self.base_url}/analyze-text")
        self.assertEqual(response.status_code, 200)
        print("✅ Analyze text page loads")
    
    def test_05_history_page_loads(self):
        """Test 5: History page loads (Button 4)"""
        print("\n[TEST 5] Testing history page loads...")
        response = requests.get(f"{self.base_url}/history")
        self.assertEqual(response.status_code, 200)
        print("✅ History page loads")
    
    def test_06_save_only_api_no_file(self):
        """Test 6: /api/recording/save-only returns error without file"""
        print("\n[TEST 6] Testing save-only API without file...")
        response = requests.post(f"{self.base_url}/api/recording/save-only")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('error', data)
        print("✅ API correctly rejects request without audio file")
    
    def test_07_save_only_api_with_file(self):
        """Test 7: /api/recording/save-only saves audio successfully"""
        print("\n[TEST 7] Testing save-only API with audio file...")
        
        # Create dummy audio file
        audio_data = b'RIFF....WAVE....' # Minimal WAV header
        
        files = {'audio': ('test_recording.webm', audio_data, 'audio/webm')}
        data = {'type': 'mic'}
        
        response = requests.post(
            f"{self.base_url}/api/recording/save-only",
            files=files,
            data=data
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['success'])
        self.assertIn('filename', result)
        self.assertIn('id', result)
        
        # Verify file was saved
        history_dir = Path("data/history")
        saved_file = history_dir / result['filename']
        self.assertTrue(saved_file.exists())
        
        # Verify JSON was created
        json_file = history_dir / f"{result['id']}.json"
        self.assertTrue(json_file.exists())
        
        with open(json_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        self.assertEqual(history_data['id'], result['id'])
        self.assertEqual(history_data['title'], 'Ghi âm mic')
        self.assertEqual(history_data['summary'], 'Ghi âm chưa được phân tích')
        
        print(f"✅ Audio saved successfully: {result['filename']}")
        print(f"   ID: {result['id']}")
        
        # Cleanup
        saved_file.unlink()
        json_file.unlink()
    
    def test_08_history_api_lists_recordings(self):
        """Test 8: /api/history/list shows saved recordings"""
        print("\n[TEST 8] Testing history API lists recordings...")
        response = requests.get(f"{self.base_url}/api/history/list?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('history', data)
        self.assertIsInstance(data['history'], list)
        print(f"✅ History API returns {len(data['history'])} recordings")
    
    def test_09_routes_exist(self):
        """Test 9: All new routes exist and return 200"""
        print("\n[TEST 9] Testing all routes exist...")
        routes = [
            ('/', 'Homepage'),
            ('/record', 'Record page'),
            ('/analyze-audio', 'Analyze audio page'),
            ('/analyze-text', 'Analyze text page'),
            ('/history', 'History page')
        ]
        
        for route, name in routes:
            response = requests.get(f"{self.base_url}{route}")
            self.assertEqual(response.status_code, 200, f"{name} failed")
            print(f"   ✅ {name}: {route}")
    
    def test_10_integration_record_and_view(self):
        """Test 10: Integration test - Record and view in history"""
        print("\n[TEST 10] Integration test: Record → History...")
        
        # Step 1: Save recording
        audio_data = b'RIFF....WAVE....'
        files = {'audio': ('integration_test.webm', audio_data, 'audio/webm')}
        data = {'type': 'browser'}
        
        save_response = requests.post(
            f"{self.base_url}/api/recording/save-only",
            files=files,
            data=data
        )
        self.assertEqual(save_response.status_code, 200)
        save_result = save_response.json()
        recording_id = save_result['id']
        print(f"   Step 1: Saved recording {recording_id}")
        
        # Step 2: Check it appears in history
        time.sleep(0.5)  # Brief delay for file system
        history_response = requests.get(f"{self.base_url}/api/history/list?limit=100")
        self.assertEqual(history_response.status_code, 200)
        history_data = history_response.json()
        
        # Find our recording
        found = False
        for item in history_data['history']:
            if item.get('id') == recording_id:
                found = True
                self.assertEqual(item['title'], 'Ghi âm browser')
                print(f"   Step 2: Found in history ✅")
                break
        
        self.assertTrue(found, "Recording not found in history")
        
        # Cleanup
        history_dir = Path("data/history")
        (history_dir / save_result['filename']).unlink()
        (history_dir / f"{recording_id}.json").unlink()
        
        print("✅ Integration test passed: Record → History workflow works")


def run_tests():
    """Run all tests"""
    print("="*70)
    print("HOMEPAGE REDESIGN TEST SUITE")
    print("="*70)
    print("\nTesting new 4-button logic:")
    print("1. Record audio (save only)")
    print("2. Analyze audio (upload -> analyze)")
    print("3. Analyze text (upload txt/docx/PDF -> analyze)")
    print("4. History (view past analyses)")
    print("="*70)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestHomepageRedesign)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
    
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
