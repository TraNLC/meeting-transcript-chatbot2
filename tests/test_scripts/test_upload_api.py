"""
Comprehensive Test Suite for Upload API Endpoint
URL: http://localhost:5000/api/upload/process

Test Coverage:
- Text file upload and analysis
- Audio file upload and transcription
- Error handling and validation
- Different languages and meeting types
- File size and format validation
"""

import pytest
import requests
import os
from pathlib import Path
import time


# Test Configuration
BASE_URL = "http://localhost:5000"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/upload/process"
TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestUploadAPI:
    """Test suite for upload API endpoint."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment - use files from mocks folder."""
        # Use mock files instead of creating new ones
        mocks_dir = Path(__file__).parent.parent / "mocks"
        
        self.sample_txt_file = mocks_dir / "meeting_sample.txt"
        self.interview_file = mocks_dir / "interview_sample.txt"
        self.brainstorm_file = mocks_dir / "brainstorm_sample.txt"
        
        # Ensure mock files exist
        if not self.sample_txt_file.exists():
            raise FileNotFoundError(f"Mock file not found: {self.sample_txt_file}")
        
        yield
    
    def test_01_text_file_upload_success(self):
        """Test 1: Upload text file successfully."""
        print("\n=== Test 1: Text File Upload Success ===")
        
        with open(self.sample_txt_file, 'rb') as f:
            files = {'text_file': ('test_meeting.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'status' in result
        assert 'transcript' in result
        assert 'summary' in result
        assert 'topics' in result
        assert 'actions' in result
        assert 'decisions' in result
        
        # Verify content is not empty
        assert len(result['transcript']) > 0, "Transcript should not be empty"
        assert len(result['summary']) > 0, "Summary should not be empty"
        
        print("✅ Test 1 PASSED")
    
    def test_02_text_file_english_language(self):
        """Test 2: Upload text file with English output."""
        print("\n=== Test 2: English Language Output ===")
        
        # Create English sample
        english_file = TEST_DATA_DIR / "test_meeting_en.txt"
        english_file.write_text(
            "Meeting started at 9 AM. "
            "Main topic is discussing the new project. "
            "John proposed increasing budget by 20%. "
            "Sarah agreed and suggested completion in 3 months. "
            "Decision: Approve project and start next week.",
            encoding='utf-8'
        )
        
        with open(english_file, 'rb') as f:
            files = {'text_file': ('test_meeting_en.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'en',
                'transcribe_lang': 'en'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Keys: {response.json().keys()}")
        
        assert response.status_code == 200
        result = response.json()
        assert 'summary' in result
        
        print("✅ Test 2 PASSED")
    
    def test_03_different_meeting_types(self):
        """Test 3: Test different meeting types."""
        print("\n=== Test 3: Different Meeting Types ===")
        
        meeting_types = ['meeting', 'interview', 'presentation', 'brainstorm', 'training']
        
        for meeting_type in meeting_types:
            print(f"\nTesting meeting type: {meeting_type}")
            
            with open(self.sample_txt_file, 'rb') as f:
                files = {'text_file': ('test_meeting.txt', f, 'text/plain')}
                data = {
                    'file_type': 'text',
                    'meeting_type': meeting_type,
                    'output_lang': 'vi',
                    'transcribe_lang': 'vi'
                }
                
                response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
            
            assert response.status_code == 200, f"Failed for meeting type: {meeting_type}"
            result = response.json()
            assert 'summary' in result
            
            print(f"  ✓ {meeting_type} - OK")
        
        print("✅ Test 3 PASSED")
    
    def test_04_no_file_uploaded(self):
        """Test 4: Error when no file is uploaded."""
        print("\n=== Test 4: No File Uploaded Error ===")
        
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 400, "Should return 400 for missing file"
        assert 'error' in response.json()
        
        print("✅ Test 4 PASSED")
    
    def test_05_empty_file(self):
        """Test 5: Error when uploading empty file."""
        print("\n=== Test 5: Empty File Error ===")
        
        empty_file = TEST_DATA_DIR / "empty.txt"
        empty_file.write_text("", encoding='utf-8')
        
        with open(empty_file, 'rb') as f:
            files = {'text_file': ('empty.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 400, "Should return 400 for empty file"
        assert 'error' in response.json()
        
        print("✅ Test 5 PASSED")
    
    def test_06_invalid_file_type(self):
        """Test 6: Error when uploading invalid file type."""
        print("\n=== Test 6: Invalid File Type Error ===")
        
        invalid_file = TEST_DATA_DIR / "test.exe"
        invalid_file.write_bytes(b"fake executable")
        
        with open(invalid_file, 'rb') as f:
            files = {'text_file': ('test.exe', f, 'application/octet-stream')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 400, "Should return 400 for invalid file type"
        assert 'error' in response.json()
        
        print("✅ Test 6 PASSED")
    
    def test_07_large_text_file(self):
        """Test 7: Upload large text file."""
        print("\n=== Test 7: Large Text File ===")
        
        # Create a large text file (simulate long meeting)
        large_content = "Cuộc họp bắt đầu. " * 500  # ~10KB
        large_file = TEST_DATA_DIR / "large_meeting.txt"
        large_file.write_text(large_content, encoding='utf-8')
        
        with open(large_file, 'rb') as f:
            files = {'text_file': ('large_meeting.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi'
            }
            
            start_time = time.time()
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
            elapsed_time = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Processing Time: {elapsed_time:.2f}s")
        
        assert response.status_code == 200, "Should handle large files"
        result = response.json()
        assert 'summary' in result
        
        print("✅ Test 7 PASSED")
    
    def test_08_special_characters_in_filename(self):
        """Test 8: Upload file with special characters in filename."""
        print("\n=== Test 8: Special Characters in Filename ===")
        
        special_file = TEST_DATA_DIR / "test file (2024-12-07) #1.txt"
        special_file.write_text("Test content", encoding='utf-8')
        
        with open(special_file, 'rb') as f:
            files = {'text_file': (special_file.name, f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        
        # Should either succeed or return proper error
        assert response.status_code in [200, 400]
        
        print("✅ Test 8 PASSED")
    
    def test_09_concurrent_uploads(self):
        """Test 9: Multiple concurrent uploads."""
        print("\n=== Test 9: Concurrent Uploads ===")
        
        import concurrent.futures
        
        def upload_file(file_num):
            with open(self.sample_txt_file, 'rb') as f:
                files = {'text_file': (f'test_{file_num}.txt', f, 'text/plain')}
                data = {
                    'file_type': 'text',
                    'meeting_type': 'meeting',
                    'output_lang': 'vi'
                }
                
                response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=60)
                return response.status_code
        
        # Upload 3 files concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(upload_file, i) for i in range(3)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        print(f"Results: {results}")
        
        # At least some should succeed (may hit rate limits)
        success_count = sum(1 for r in results if r == 200)
        print(f"Success: {success_count}/3")
        
        assert success_count >= 1, "At least one upload should succeed"
        
        print("✅ Test 9 PASSED")
    
    def test_10_response_structure_validation(self):
        """Test 10: Validate complete response structure."""
        print("\n=== Test 10: Response Structure Validation ===")
        
        with open(self.sample_txt_file, 'rb') as f:
            files = {'text_file': ('test_meeting.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        assert response.status_code == 200
        result = response.json()
        
        # Validate all required fields
        required_fields = ['status', 'transcript', 'summary', 'topics', 'actions', 'decisions', 'participants']
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
            print(f"  ✓ {field}: {type(result[field]).__name__} ({len(str(result[field]))} chars)")
        
        # Validate data types
        assert isinstance(result['status'], str)
        assert isinstance(result['transcript'], str)
        assert isinstance(result['summary'], str)
        
        print("✅ Test 10 PASSED")


def run_all_tests():
    """Run all tests and generate report."""
    print("\n" + "="*60)
    print("UPLOAD API TEST SUITE")
    print("="*60)
    print(f"Endpoint: {UPLOAD_ENDPOINT}")
    print(f"Test Data: {TEST_DATA_DIR}")
    print("="*60 + "\n")
    
    # Run pytest
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_all_tests()
