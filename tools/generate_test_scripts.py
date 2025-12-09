"""
Test Script Generator
Generates pytest test scripts from YAML test cases

Usage:
    python tools/generate_test_scripts.py
    python tools/generate_test_scripts.py --input tests/test_cases/upload_api_tests.yaml
"""

import yaml
import argparse
from pathlib import Path
from datetime import datetime


class TestScriptGenerator:
    """Generate pytest scripts from YAML test cases."""
    
    def __init__(self, test_cases_file: Path):
        """Initialize generator with test cases file."""
        self.test_cases_file = test_cases_file
        self.test_data = self._load_test_cases()
    
    def _load_test_cases(self) -> dict:
        """Load test cases from YAML file."""
        with open(self.test_cases_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate_test_script(self) -> str:
        """Generate complete pytest script."""
        test_suite = self.test_data['test_suite']
        test_cases = self.test_data['test_cases']
        
        script = self._generate_header(test_suite)
        script += self._generate_imports()
        script += self._generate_config(test_suite)
        script += self._generate_test_class()
        script += self._generate_fixtures()
        
        # Generate test methods
        for test_case in test_cases:
            script += self._generate_test_method(test_case)
        
        script += self._generate_footer()
        
        return script
    
    def _generate_header(self, test_suite: dict) -> str:
        """Generate file header."""
        return f'''"""
{test_suite['name']}
Auto-generated from: {self.test_cases_file.name}
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Description: {test_suite['description']}
"""

'''
    
    def _generate_imports(self) -> str:
        """Generate import statements."""
        return '''import pytest
import requests
from pathlib import Path
from io import BytesIO
import time
import concurrent.futures


'''
    
    def _generate_config(self, test_suite: dict) -> str:
        """Generate configuration."""
        return f'''# Test Configuration
BASE_URL = "{test_suite['endpoint'].rsplit('/', 1)[0]}"
UPLOAD_ENDPOINT = "{test_suite['endpoint']}"
PROJECT_ROOT = Path(__file__).parent.parent
MOCKS_DIR = PROJECT_ROOT / "mocks"


'''
    
    def _generate_test_class(self) -> str:
        """Generate test class."""
        return '''class TestUploadAPIGenerated:
    """Auto-generated test class from YAML test cases."""
    
'''
    
    def _generate_fixtures(self) -> str:
        """Generate pytest fixtures."""
        return '''    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        # Ensure mocks directory exists
        assert MOCKS_DIR.exists(), f"Mocks directory not found: {MOCKS_DIR}"
        yield
    
'''
    
    def _generate_test_method(self, test_case: dict) -> str:
        """Generate individual test method."""
        test_id = test_case['id']
        name = test_case['name']
        category = test_case['category']
        description = test_case['description']
        input_data = test_case['input']
        expected = test_case['expected']
        
        # Generate method name
        method_name = f"test_{test_id.lower()}_{name.lower().replace(' ', '_').replace('-', '_')}"
        method_name = ''.join(c for c in method_name if c.isalnum() or c == '_')
        
        # Generate method
        method = f'''    def {method_name}(self):
        """
        {test_id}: {name}
        Category: {category}
        Description: {description}
        """
        print(f"\\n=== {test_id}: {name} ===")
        
'''
        
        # Generate test logic based on category
        if category == "success":
            method += self._generate_success_test(input_data, expected)
        elif category == "validation_error":
            method += self._generate_validation_test(input_data, expected)
        elif category == "performance":
            method += self._generate_performance_test(input_data, expected)
        elif category == "edge_case":
            method += self._generate_edge_case_test(input_data, expected)
        
        method += '\n'
        return method
    
    def _generate_success_test(self, input_data: dict, expected: dict) -> str:
        """Generate success test logic."""
        code = ''
        
        # Prepare file
        if 'file' in input_data:
            code += f'''        file_path = MOCKS_DIR / "{input_data['file']}"
        assert file_path.exists(), f"Mock file not found: {{file_path}}"
        
        with open(file_path, 'rb') as f:
            files = {{'text_file': ('{input_data['file']}', f, 'text/plain')}}
            data = {{
                'file_type': '{input_data.get('file_type', 'text')}',
                'meeting_type': '{input_data.get('meeting_type', 'meeting')}',
                'output_lang': '{input_data.get('output_lang', 'vi')}',
                'transcribe_lang': '{input_data.get('transcribe_lang', 'vi')}'
            }}
            
            response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
        
'''
        
        # Assertions
        code += f'''        print(f"Status Code: {{response.status_code}}")
        assert response.status_code == {expected['status_code']}, f"Expected {expected['status_code']}, got {{response.status_code}}"
        
        result = response.json()
'''
        
        if 'response_contains' in expected:
            for field in expected['response_contains']:
                code += f"        assert '{field}' in result, f\"Missing field: {field}\"\n"
        
        if 'validations' in expected:
            code += '\n'
            for validation in expected['validations']:
                code += f"        assert {validation}, f\"Validation failed: {validation}\"\n"
        
        code += '\n        print("✅ Test PASSED")\n'
        return code
    
    def _generate_validation_test(self, input_data: dict, expected: dict) -> str:
        """Generate validation error test logic."""
        code = ''
        
        if 'file' in input_data and 'file_content' in input_data:
            # Create temporary file
            code += f'''        # Create temporary file
        file_content = """{input_data['file_content']}"""
        files = {{'text_file': ('{input_data['file']}', BytesIO(file_content.encode()), 'text/plain')}}
'''
        else:
            code += '''        # No file
        files = {}
'''
        
        code += f'''        data = {{
            'file_type': '{input_data.get('file_type', 'text')}',
            'meeting_type': '{input_data.get('meeting_type', 'meeting')}',
            'output_lang': '{input_data.get('output_lang', 'vi')}'
        }}
        
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=30)
        
        print(f"Status Code: {{response.status_code}}")
        assert response.status_code == {expected['status_code']}, f"Expected {expected['status_code']}, got {{response.status_code}}"
        
        result = response.json()
        assert 'error' in result, "Expected error message"
        print(f"Error: {{result['error']}}")
        print("✅ Test PASSED")
'''
        return code
    
    def _generate_performance_test(self, input_data: dict, expected: dict) -> str:
        """Generate performance test logic."""
        if 'concurrent_requests' in input_data:
            return self._generate_concurrent_test(input_data, expected)
        else:
            return self._generate_success_test(input_data, expected)
    
    def _generate_concurrent_test(self, input_data: dict, expected: dict) -> str:
        """Generate concurrent upload test."""
        return f'''        def upload_file(i):
            file_path = MOCKS_DIR / "{input_data['file']}"
            with open(file_path, 'rb') as f:
                files = {{'text_file': (f'test_{{i}}.txt', f, 'text/plain')}}
                data = {{
                    'file_type': '{input_data.get('file_type', 'text')}',
                    'meeting_type': '{input_data.get('meeting_type', 'meeting')}',
                    'output_lang': '{input_data.get('output_lang', 'vi')}'
                }}
                response = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=60)
                return response.status_code
        
        with concurrent.futures.ThreadPoolExecutor(max_workers={input_data['concurrent_requests']}) as executor:
            futures = [executor.submit(upload_file, i) for i in range({input_data['concurrent_requests']})]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        success_count = sum(1 for r in results if r == 200)
        print(f"Success: {{success_count}}/{input_data['concurrent_requests']}")
        assert success_count >= {expected['min_success_count']}, "Not enough successful uploads"
        print("✅ Test PASSED")
'''
    
    def _generate_edge_case_test(self, input_data: dict, expected: dict) -> str:
        """Generate edge case test logic."""
        return self._generate_validation_test(input_data, expected)
    
    def _generate_footer(self) -> str:
        """Generate file footer."""
        return '''

def run_tests():
    """Run all generated tests."""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_tests()
'''
    
    def save_script(self, output_path: Path):
        """Generate and save test script."""
        script = self.generate_test_script()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"✅ Generated test script: {output_path}")
        print(f"   Test cases: {len(self.test_data['test_cases'])}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate pytest scripts from YAML test cases')
    parser.add_argument('--input', '-i', 
                       default='tests/test_cases/upload_api_tests.yaml',
                       help='Input YAML test cases file')
    parser.add_argument('--output', '-o',
                       default='tests/test_scripts/test_upload_generated.py',
                       help='Output pytest script file')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Error: Test cases file not found: {input_path}")
        return
    
    print(f"📝 Generating test script from: {input_path}")
    
    generator = TestScriptGenerator(input_path)
    generator.save_script(output_path)
    
    print(f"\n🚀 Run tests with: python -m pytest {output_path} -v")


if __name__ == "__main__":
    main()
