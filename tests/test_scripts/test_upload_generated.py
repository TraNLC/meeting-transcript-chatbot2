"""
Upload API Test Suite
Auto-generated from: upload_api_tests.yaml
Generated at: 2025-12-07 23:51:53

Description: Test cases for file upload and analysis API
"""

import pytest
import requests
from pathlib import Path
from io import BytesIO
import time
import concurrent.futures


# Test Configuration
BASE_URL = "http://localhost:5000/api/upload"
UPLOAD_ENDPOINT = "http://localhost:5000/api/upload/process"
PROJECT_ROOT = Path(__file__).parent.parent
MOCKS_DIR = PROJECT_ROOT / "mocks"


class TestUploadAPIGenerated:
    """Auto-generated test class from YAML test cases."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        # Ensure mocks directory exists
        assert MOCKS_DIR.exists(), f"Mocks directory not found: {MOCKS_DIR}"
        yield
    
    def test_tc001_upload_text_file___meeting_type(self):
        """
        TC001: Upload text file - Meeting type
        Category: success
        Description: Upload a meeting transcript and verify analysis results
        """
        print(f"\n=== TC001: Upload text file - Meeting type ===")
        
        file_path = MOCKS_DIR / "mocks/meeting_sample.txt"
        assert file_path.exists(), f"Mock file not found: {file_path}"
        
        with open(file_path, 'rb') as f:
            files = {'text_file': ('mocks/meeting_sample.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'summary' in result, f"Missing field: summary"
        assert 'topics' in result, f"Missing field: topics"
        assert 'actions' in result, f"Missing field: actions"
        assert 'decisions' in result, f"Missing field: decisions"

        assert len(response['summary']) > 50, f"Validation failed: len(response['summary']) > 50"
        assert len(response['topics']) > 0, f"Validation failed: len(response['topics']) > 0"
        assert 'status' in response, f"Validation failed: 'status' in response"

        print("✅ Test PASSED")

    def test_tc002_upload_text_file___interview_type(self):
        """
        TC002: Upload text file - Interview type
        Category: success
        Description: Upload an interview transcript
        """
        print(f"\n=== TC002: Upload text file - Interview type ===")
        
        file_path = MOCKS_DIR / "mocks/interview_sample.txt"
        assert file_path.exists(), f"Mock file not found: {file_path}"
        
        with open(file_path, 'rb') as f:
            files = {'text_file': ('mocks/interview_sample.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'interview',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'summary' in result, f"Missing field: summary"
        assert 'topics' in result, f"Missing field: topics"

        print("✅ Test PASSED")

    def test_tc003_upload_text_file___brainstorm_type(self):
        """
        TC003: Upload text file - Brainstorm type
        Category: success
        Description: Upload a brainstorming session transcript
        """
        print(f"\n=== TC003: Upload text file - Brainstorm type ===")
        
        file_path = MOCKS_DIR / "mocks/brainstorm_sample.txt"
        assert file_path.exists(), f"Mock file not found: {file_path}"
        
        with open(file_path, 'rb') as f:
            files = {'text_file': ('mocks/brainstorm_sample.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'brainstorm',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'summary' in result, f"Missing field: summary"
        assert 'topics' in result, f"Missing field: topics"

        print("✅ Test PASSED")

    def test_tc004_upload_text_file___english_language(self):
        """
        TC004: Upload text file - English language
        Category: success
        Description: Upload and analyze in English
        """
        print(f"\n=== TC004: Upload text file - English language ===")
        
        file_path = MOCKS_DIR / "mocks/meeting_sample.txt"
        assert file_path.exists(), f"Mock file not found: {file_path}"
        
        with open(file_path, 'rb') as f:
            files = {'text_file': ('mocks/meeting_sample.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'en',
                'transcribe_lang': 'en'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'summary' in result, f"Missing field: summary"

        print("✅ Test PASSED")

    def test_tc101_no_file_uploaded(self):
        """
        TC101: No file uploaded
        Category: validation_error
        Description: Attempt to upload without selecting a file
        """
        print(f"\n=== TC101: No file uploaded ===")
        
        # No file
        files = {}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc102_empty_file(self):
        """
        TC102: Empty file
        Category: validation_error
        Description: Upload an empty file (0 bytes)
        """
        print(f"\n=== TC102: Empty file ===")
        
        # Create temporary file
        file_content = """"""
        files = {'text_file': ('empty.txt', BytesIO(file_content.encode()), 'text/plain')}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc103_invalid_file_type(self):
        """
        TC103: Invalid file type
        Category: validation_error
        Description: Upload unsupported file format (.exe)
        """
        print(f"\n=== TC103: Invalid file type ===")
        
        # Create temporary file
        file_content = """fake executable"""
        files = {'text_file': ('test.exe', BytesIO(file_content.encode()), 'text/plain')}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc104_invalid_language_code(self):
        """
        TC104: Invalid language code
        Category: validation_error
        Description: Use unsupported language code
        """
        print(f"\n=== TC104: Invalid language code ===")
        
        # No file
        files = {}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'invalid_lang'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc105_special_characters_in_filename(self):
        """
        TC105: Special characters in filename
        Category: validation_error
        Description: Upload file with special characters in name
        """
        print(f"\n=== TC105: Special characters in filename ===")
        
        # Create temporary file
        file_content = """Test content"""
        files = {'text_file': ('test file (2024-12-07) #1.txt', BytesIO(file_content.encode()), 'text/plain')}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == [200, 400], f"Expected [200, 400], got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc201_large_file_upload(self):
        """
        TC201: Large file upload
        Category: performance
        Description: Upload large text file (~10KB)
        """
        print(f"\n=== TC201: Large file upload ===")
        
        file_path = MOCKS_DIR / "large_meeting.txt"
        assert file_path.exists(), f"Mock file not found: {file_path}"
        
        with open(file_path, 'rb') as f:
            files = {'text_file': ('large_meeting.txt', f, 'text/plain')}
            data = {
                'file_type': 'text',
                'meeting_type': 'meeting',
                'output_lang': 'vi',
                'transcribe_lang': 'vi'
            }
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()

        print("✅ Test PASSED")

    def test_tc202_concurrent_uploads(self):
        """
        TC202: Concurrent uploads
        Category: performance
        Description: Multiple simultaneous uploads
        """
        print(f"\n=== TC202: Concurrent uploads ===")
        
        def upload_file(i):
            file_path = MOCKS_DIR / "mocks/meeting_sample.txt"
            with open(file_path, 'rb') as f:
                files = {'text_file': (f'test_{i}.txt', f, 'text/plain')}
                data = {
                    'file_type': 'text',
                    'meeting_type': 'meeting',
                    'output_lang': 'vi'
                }
                response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=60)
                return response.status_code
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(upload_file, i) for i in range(3)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        success_count = sum(1 for r in results if r == 200)
        print(f"Success: {success_count}/3")
        assert success_count >= 1, "Not enough successful uploads"
        print("✅ Test PASSED")

    def test_tc301_very_short_content(self):
        """
        TC301: Very short content
        Category: edge_case
        Description: Upload file with minimal content
        """
        print(f"\n=== TC301: Very short content ===")
        
        # Create temporary file
        file_content = """Hello"""
        files = {'text_file': ('short.txt', BytesIO(file_content.encode()), 'text/plain')}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == [200, 400], f"Expected [200, 400], got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")

    def test_tc302_unicode_characters(self):
        """
        TC302: Unicode characters
        Category: edge_case
        Description: Upload file with special Unicode characters
        """
        print(f"\n=== TC302: Unicode characters ===")
        
        # Create temporary file
        file_content = """Cuộc họp 🎉 với emoji và ký tự đặc biệt: ñ, ü, ç"""
        files = {'text_file': ('unicode.txt', BytesIO(file_content.encode()), 'text/plain')}
        data = {
            'file_type': 'text',
            'meeting_type': 'meeting',
            'output_lang': 'vi'
        }
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {result['error']}")
        print("✅ Test PASSED")



def run_tests():
    """Run all generated tests."""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_tests()
