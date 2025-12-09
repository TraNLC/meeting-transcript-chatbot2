"""
Test Generator - Generate pytest test cases from YAML files
Generates test functions for TXT, PDF, and Audio upload tests
"""

import yaml
from pathlib import Path
from datetime import datetime


class TestGenerator:
    """Generate pytest test cases from YAML test definitions."""
    
    def __init__(self, yaml_file: Path):
        self.yaml_file = yaml_file
        with open(yaml_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        self.test_suite = self.data.get('test_suite', {})
        self.test_cases = self.data.get('test_cases', [])
    
    def generate_test_function(self, test_case: dict) -> str:
        """Generate a single test function from test case definition."""
        test_id = test_case['id']
        test_name = test_case['name']
        category = test_case.get('category', 'general')
        priority = test_case.get('priority', 'medium')
        
        input_data = test_case.get('input', {})
        expected = test_case.get('expected', {})
        
        # Build function name
        func_name = f"test_{test_id.lower()}_{test_name.replace(' ', '_').replace('-', '_')}"
        func_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in func_name)
        
        # Build docstring
        docstring = f'''"""
        {test_id}: {test_name}
        Category: {category}
        Priority: {priority}
        """'''
        
        # Build test body
        lines = []
        lines.append(f'    def {func_name}(self):')
        lines.append(f'        {docstring}')
        lines.append(f'        print(f"\\n=== {test_id}: {test_name} ===")')
        lines.append('')
        
        # Handle file input
        file_path = input_data.get('file', '')
        file_content = input_data.get('file_content')
        
        if file_content:
            # Create temporary file
            lines.append('        # Create temporary file')
            lines.append(f'        file_content = """{file_content}"""')
            lines.append(f'        files = {{"text_file": ("{file_path}", BytesIO(file_content.encode()), "text/plain")}}')
        elif file_path:
            # Use existing file
            lines.append(f'        file_path = MOCKS_DIR / "{file_path}"')
            lines.append('        assert file_path.exists(), f"Mock file not found: {file_path}"')
            lines.append('')
            lines.append('        with open(file_path, "rb") as f:')
            
            # Determine file field name based on file type
            file_type = input_data.get('file_type', 'text')
            if file_type == 'audio':
                field_name = 'audio_file'
            else:
                field_name = 'text_file'
            
            lines.append(f'            files = {{"{field_name}": ("{file_path}", f, "application/octet-stream")}}')
        else:
            lines.append('        # No file')
            lines.append('        files = {}')
        
        # Build data payload
        lines.append('        data = {')
        for key, value in input_data.items():
            if key not in ['file', 'file_content']:
                if isinstance(value, str):
                    lines.append(f'            "{key}": "{value}",')
                else:
                    lines.append(f'            "{key}": {value},')
        lines.append('        }')
        lines.append('')
        
        # Make request
        timeout = expected.get('max_response_time', 120)
        if file_content:
            lines.append(f'        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout={timeout})')
        else:
            lines.append(f'            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout={timeout})')
        lines.append('')
        
        # Check status code
        lines.append('        print(f"Status Code: {response.status_code}")')
        expected_status = expected.get('status_code', 200)
        if isinstance(expected_status, list):
            lines.append(f'        assert response.status_code in {expected_status}, f"Expected {expected_status}, got {{response.status_code}}"')
        else:
            lines.append(f'        assert response.status_code == {expected_status}, f"Expected {expected_status}, got {{response.status_code}}"')
        lines.append('')
        
        # Parse response
        if expected_status == 200 or (isinstance(expected_status, list) and 200 in expected_status):
            lines.append('        result = response.json()')
            lines.append('')
            
            # AI validations
            ai_validations = expected.get('ai_validations', [])
            if ai_validations:
                lines.append('        # AI validations')
                for validation in ai_validations:
                    # Replace response with result
                    validation_code = validation.replace('response', 'result')
                    lines.append(f'        assert {validation_code}, f"AI validation failed: {validation}"')
                lines.append('')
        
        # Check error message if expected
        error_contains = expected.get('error_contains')
        if error_contains:
            lines.append('        result = response.json()')
            lines.append('        assert "error" in result, "Expected error message"')
            lines.append(f'        assert "{error_contains}" in result["error"].lower(), f"Expected error to contain \\"{error_contains}\\""')
            lines.append('        print(f"Error: {result[\'error\']}")')
        
        lines.append('        print("✅ Test PASSED")')
        lines.append('')
        
        return '\n'.join(lines)
    
    def generate_test_class(self) -> str:
        """Generate complete test class with all test functions."""
        lines = []
        
        # Header
        lines.append('"""')
        lines.append(f'{self.test_suite.get("name", "Test Suite")}')
        lines.append(f'Auto-generated from: {self.yaml_file.name}')
        lines.append(f'Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append('')
        lines.append(f'Description: {self.test_suite.get("description", "")}')
        lines.append('"""')
        lines.append('')
        lines.append('import pytest')
        lines.append('import requests')
        lines.append('from pathlib import Path')
        lines.append('from io import BytesIO')
        lines.append('import time')
        lines.append('')
        lines.append('')
        lines.append('# Test Configuration')
        lines.append(f'BASE_URL = "{self.test_suite.get("endpoint", "http://localhost:5000/api/upload")}"')
        lines.append('UPLOAD_ENDPOINT = BASE_URL')
        lines.append('PROJECT_ROOT = Path(__file__).parent.parent.parent')
        lines.append('MOCKS_DIR = PROJECT_ROOT / "mocks"')
        lines.append('')
        lines.append('')
        
        # Test class
        class_name = self.yaml_file.stem.replace('_', ' ').title().replace(' ', '')
        lines.append(f'class Test{class_name}:')
        lines.append('    """Auto-generated test class from YAML test cases."""')
        lines.append('')
        lines.append('    @pytest.fixture(autouse=True)')
        lines.append('    def setup(self):')
        lines.append('        """Setup test environment."""')
        lines.append('        # Ensure mocks directory exists')
        lines.append('        assert MOCKS_DIR.exists(), f"Mocks directory not found: {MOCKS_DIR}"')
        lines.append('        yield')
        lines.append('')
        
        # Generate test functions
        for test_case in self.test_cases:
            lines.append(self.generate_test_function(test_case))
        
        # Footer
        lines.append('')
        lines.append('def run_tests():')
        lines.append('    """Run all generated tests."""')
        lines.append('    pytest.main([__file__, "-v", "--tb=short"])')
        lines.append('')
        lines.append('')
        lines.append('if __name__ == "__main__":')
        lines.append('    run_tests()')
        lines.append('')
        
        return '\n'.join(lines)


def generate_all_tests():
    """Generate test files for all YAML test cases."""
    test_cases_dir = Path(__file__).parent / "test_cases"
    test_scripts_dir = Path(__file__).parent / "test_scripts"
    
    yaml_files = [
        # Text files (TXT, DOCX, PDF)
        ("upload_txt_tests.yaml", "test_txt_upload.py"),
        ("upload_pdf_tests.yaml", "test_pdf_upload.py"),
        ("upload_docx_tests.yaml", "test_docx_upload.py"),
        # Audio/Video files (WAV, MP3, MP4, WebM)
        ("upload_mp3_tests.yaml", "test_mp3_upload.py"),
        ("upload_wav_tests.yaml", "test_wav_upload.py"),
        ("upload_webm_tests.yaml", "test_webm_upload.py"),
        ("upload_mp4_tests.yaml", "test_mp4_upload.py"),
    ]
    
    for yaml_file, output_file in yaml_files:
        yaml_path = test_cases_dir / yaml_file
        if not yaml_path.exists():
            print(f"⚠️  YAML file not found: {yaml_path}")
            continue
        
        print(f"📝 Generating tests from {yaml_file}...")
        generator = TestGenerator(yaml_path)
        test_code = generator.generate_test_class()
        
        output_path = test_scripts_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        print(f"✅ Generated: {output_path}")
    
    print("\n🎉 All test files generated successfully!")


if __name__ == "__main__":
    generate_all_tests()
