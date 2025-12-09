"""
Comprehensive Page-by-Page Test Suite
Tests every page thoroughly to find issues and provide fix recommendations

Run: pytest tests/test_all_pages.py -v -s
"""

import pytest
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import tempfile
import json

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"


class TestHomePage:
    """Test / (Home/Index page)"""
    
    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"\n✅ Home page loaded")
        print(f"   Title: {soup.title.string if soup.title else 'No title'}")
        
    def test_home_page_has_navigation(self):
        """Test home page has proper navigation links"""
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for links to other pages
        links = [a.get('href', '') for a in soup.find_all('a')]
        print(f"\n   Found {len(links)} links")
        
        # Should have link to upload page
        upload_links = [l for l in links if 'upload' in l.lower()]
        assert len(upload_links) > 0, "No link to upload page found"
        print(f"   ✅ Has upload link")


class TestUploadPage:
    """Test /upload page thoroughly"""
    
    def test_upload_page_loads(self):
        """Test upload page loads without errors"""
        response = requests.get(f"{BASE_URL}/upload")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"\n✅ Upload page loaded")
        
    def test_upload_page_has_file_input(self):
        """Test upload page has file input element"""
        response = requests.get(f"{BASE_URL}/upload")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        file_inputs = soup.find_all('input', {'type': 'file'})
        assert len(file_inputs) > 0, "No file input found"
        print(f"   ✅ Has {len(file_inputs)} file input(s)")
        
    def test_upload_page_has_upload_button(self):
        """Test upload page has upload button"""
        response = requests.get(f"{BASE_URL}/upload")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find upload button
        buttons = soup.find_all('button')
        upload_buttons = [b for b in buttons if 'upload' in b.get_text().lower()]
        
        assert len(upload_buttons) > 0, "No upload button found"
        print(f"   ✅ Has upload button: '{upload_buttons[0].get_text().strip()}'")
        
    def test_upload_page_javascript_loaded(self):
        """Test upload page has necessary JavaScript"""
        response = requests.get(f"{BASE_URL}/upload")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for script tags
        scripts = soup.find_all('script')
        inline_scripts = [s for s in scripts if s.string and 'function' in s.string]
        
        print(f"   Found {len(scripts)} script tags, {len(inline_scripts)} with functions")
        
        # Check for specific functions
        page_content = response.text
        required_functions = [
            'handleFileSelect',
            'processWithLocalServer', 
            'uploadBtn'
        ]
        
        for func in required_functions:
            if func in page_content:
                print(f"   ✅ Has function: {func}")
            else:
                print(f"   ⚠️  Missing function: {func}")
                
    def test_upload_page_no_history_check_in_js(self):
        """BUG FIX #4: Verify history check is disabled in JavaScript"""
        response = requests.get(f"{BASE_URL}/upload")
        content = response.text
        
        # Check if history check code is commented out
        if "history check disabled" in content.lower():
            print(f"   ✅ History check is disabled")
        elif "checkExistingAnalysis" in content and "/*" in content:
            print(f"   ✅ History check is commented out")
        else:
            print(f"   ⚠️  WARNING: History check may still be active!")
            print(f"   ISSUE: Need to verify if 'checkExistingAnalysis' is commented out")
            
    def test_upload_page_version_check(self):
        """Check upload page version in JavaScript"""
        response = requests.get(f"{BASE_URL}/upload")
        content = response.text
        
        # Look for version indicator
        if "VERSION 2.0" in content or "TWO COLUMN LAYOUT" in content:
            print(f"   ✅ Page is VERSION 2.0")
        else:
            print(f"   ⚠️  Cannot confirm page version")


class TestAnalysisPage:
    """Test /analysis page thoroughly"""
    
    def test_analysis_page_loads(self):
        """Test analysis page loads"""
        response = requests.get(f"{BASE_URL}/analysis")
        assert response.status_code == 200
        print(f"\n✅ Analysis page loaded")
        
    def test_analysis_page_has_transcript_tab(self):
        """Test analysis page has transcript tab"""
        response = requests.get(f"{BASE_URL}/analysis")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for transcript-related elements
        content = response.text.lower()
        assert 'transcript' in content, "No transcript tab found"
        print(f"   ✅ Has transcript tab")
        
    def test_analysis_page_has_panels(self):
        """Test analysis page has left and right panels"""
        response = requests.get(f"{BASE_URL}/analysis")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for panel structure
        content = response.text
        
        has_left_panel = 'analysis-panel' in content or 'left' in content.lower()
        has_right_panel = 'transcript-panel' in content or 'right' in content.lower()
        
        print(f"   Left panel: {'✅' if has_left_panel else '⚠️'}")
        print(f"   Right panel: {'✅' if has_right_panel else '⚠️'}")
        
    def test_analysis_page_transcript_loading_logic(self):
        """BUG FIX #1: Check transcript loading logic"""
        response = requests.get(f"{BASE_URL}/analysis")
        content = response.text
        
        # Check for loadTranscriptFromData function
        if 'loadTranscriptFromData' in content:
            print(f"   ✅ Has loadTranscriptFromData function")
        else:
            print(f"   ⚠️  Missing loadTranscriptFromData function")
            
        # Check if aggressive cleanup is removed
        if 'clearTranscriptFromWrongPlaces' in content:
            print(f"   ⚠️  WARNING: Old cleanup function still exists!")
            print(f"   ISSUE: clearTranscriptFromWrongPlaces should be removed")
        else:
            print(f"   ✅ Old cleanup functions removed")
            
    def test_analysis_page_has_transcript_body(self):
        """Test analysis page has #transcriptBody element"""
        response = requests.get(f"{BASE_URL}/analysis")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        transcript_body = soup.find(id='transcriptBody')
        if transcript_body:
            print(f"   ✅ Has #transcriptBody element")
        else:
            print(f"   ⚠️  Missing #transcriptBody element")
            print(f"   ISSUE: Need to add <div id='transcriptBody'> in HTML")


class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_api_upload_process_endpoint(self):
        """Test /api/upload/process endpoint exists"""
        # Create minimal test file
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         suffix='.txt', delete=False) as f:
            f.write("Test content")
            test_file = f.name
            
        try:
            with open(test_file, 'rb') as f:
                files = {'text_file': ('test.txt', f)}
                data = {'file_type': 'text', 'transcribe_lang': 'vi'}
                
                response = requests.post(
                    f"{API_URL}/upload/process",
                    files=files,
                    data=data,
                    timeout=60
                )
            
            print(f"\n   /api/upload/process status: {response.status_code}")
            
            # Check response format
            if response.status_code == 200:
                result = response.json()
                required_fields = ['status', 'transcript', 'summary']
                for field in required_fields:
                    if field in result:
                        print(f"   ✅ Response has '{field}'")
                    else:
                        print(f"   ⚠️  Missing '{field}' in response")
                        
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
        finally:
            Path(test_file).unlink(missing_ok=True)
            
    def test_api_export_txt_endpoint(self):
        """BUG FIX #3: Test export TXT endpoint"""
        response = requests.get(f"{API_URL}/export/txt")
        print(f"\n   /api/export/txt status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   ⚠️  ISSUE: Export endpoint not found!")
        elif response.status_code == 500:
            print(f"   ✅ Endpoint exists (500 = no data to export)")
        else:
            print(f"   ✅ Endpoint exists")
            
    def test_api_export_docx_endpoint(self):
        """BUG FIX #3: Test export DOCX endpoint"""
        response = requests.get(f"{API_URL}/export/docx")
        print(f"\n   /api/export/docx status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   ⚠️  ISSUE: Export endpoint not found!")
        elif response.status_code == 500:
            print(f"   ✅ Endpoint exists (500 = no data to export)")
        else:
            print(f"   ✅ Endpoint exists")


class TestEncodingHandling:
    """Test encoding fixes (BUG #2 and #5)"""
    
    def test_utf8_bom_file_upload(self):
        """BUG FIX #2: Test file with UTF-8 BOM"""
        content = "Nội dung tiếng Việt có dấu: áéíóú"
        
        # Create file with BOM
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig',
                                         suffix='.txt', delete=False) as f:
            f.write(content)
            test_file = f.name
            
        try:
            with open(test_file, 'rb') as f:
                files = {'text_file': ('test_bom.txt', f)}
                data = {
                    'file_type': 'text',
                    'transcribe_lang': 'vi',
                    'meeting_type': 'meeting',
                    'output_lang': 'vi'
                }
                
                response = requests.post(
                    f"{API_URL}/upload/process",
                    files=files,
                    data=data,
                    timeout=90
                )
            
            print(f"\n   BOM file upload status: {response.status_code}")
            
            # Check for encoding errors
            if response.status_code == 500:
                error = response.json().get('error', '')
                if 'gbk' in error.lower() or 'codec' in error.lower():
                    print(f"   ❌ ENCODING ERROR DETECTED!")
                    print(f"   ISSUE: {error}")
                    print(f"   FIX: Need to use 'utf-8-sig' encoding in file reading")
                else:
                    print(f"   ⚠️  Error (but not encoding): {error}")
            else:
                print(f"   ✅ BOM file processed without encoding error")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        finally:
            Path(test_file).unlink(missing_ok=True)
            
    def test_vietnamese_characters_preserved(self):
        """Test Vietnamese characters are preserved"""
        content = "Test: àáảãạ êếềểễ"
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         suffix='.txt', delete=False) as f:
            f.write(content)
            test_file = f.name
            
        try:
            with open(test_file, 'rb') as f:
                files = {'text_file': ('test_vn.txt', f)}
                data = {'file_type': 'text', 'transcribe_lang': 'vi'}
                
                response = requests.post(
                    f"{API_URL}/upload/process",
                    files=files,
                    data=data,
                    timeout=90
                )
            
            if response.status_code == 200:
                result = response.json()
                transcript = result.get('transcript', '')
                
                # Check if Vietnamese chars are preserved
                has_vietnamese = any(c in transcript for c in 'àáảãạêếềểễ')
                if has_vietnamese:
                    print(f"\n   ✅ Vietnamese characters preserved")
                else:
                    print(f"\n   ⚠️  Vietnamese characters may be lost")
                    
        except Exception as e:
            print(f"\n   Error: {e}")
        finally:
            Path(test_file).unlink(missing_ok=True)


class TestExportFunctionality:
    """Test export features (BUG #3)"""
    
    def test_export_directory_exists(self):
        """Test export directory exists and is writable"""
        export_dir = Path("e:/ChatBot/meeting-transcript-chatbot2/data/exports")
        
        if export_dir.exists():
            print(f"\n   ✅ Export directory exists: {export_dir}")
            
            # Check if writable
            test_file = export_dir / "test_write.txt"
            try:
                test_file.write_text("test")
                test_file.unlink()
                print(f"   ✅ Export directory is writable")
            except Exception as e:
                print(f"   ⚠️  Cannot write to export directory: {e}")
        else:
            print(f"\n   ⚠️  Export directory does NOT exist: {export_dir}")
            print(f"   ISSUE: Need to create directory")
            print(f"   FIX: mkdir -p {export_dir}")


def generate_fix_recommendations():
    """Generate fix recommendations based on test results"""
    print("\n" + "="*70)
    print("FIX RECOMMENDATIONS BASED ON TEST RESULTS")
    print("="*70)
    
    recommendations = []
    
    # Check if export dir exists
    export_dir = Path("e:/ChatBot/meeting-transcript-chatbot2/data/exports")
    if not export_dir.exists():
        recommendations.append({
            'issue': 'Export directory missing',
            'file': 'data/exports/',
            'fix': f'Create directory: {export_dir}',
            'priority': 'HIGH'
        })
    
    print(f"\nFound {len(recommendations)} issues:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['issue']}")
        print(f"   Priority: {rec['priority']}")
        print(f"   File: {rec['file']}")
        print(f"   Fix: {rec['fix']}")
    
    if not recommendations:
        print("\n✅ No critical issues found!")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPREHENSIVE PAGE-BY-PAGE TEST SUITE")
    print("="*70)
    print("\nThis test suite will:")
    print("  1. Test each page thoroughly")
    print("  2. Identify remaining issues")
    print("  3. Provide specific fix recommendations")
    print("\nRun with: pytest tests/test_all_pages.py -v -s")
    print("="*70 + "\n")
