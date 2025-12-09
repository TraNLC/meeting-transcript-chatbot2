"""
Simple manual test script - test each page individually
Run: python tests/manual_test.py
"""

import requests
from pathlib import Path
import tempfile

BASE_URL = "http://localhost:5000"

def test_pages():
    print("\n" + "="*70)
    print("MANUAL PAGE TESTING")
    print("="*70)
    
    # Test 1: Home page
    print("\n1. Testing Home Page (/)...")
    try:
        r = requests.get(BASE_URL, timeout=5)
        if r.status_code == 200:
            print(f"   [OK] Home page loads (status: {r.status_code})")
        else:
            print(f"   [WARN] Status: {r.status_code}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    # Test 2: Upload page
    print("\n2. Testing Upload Page (/upload)...")
    try:
        r = requests.get(f"{BASE_URL}/upload", timeout=5)
        if r.status_code == 200:
            print(f"   [OK] Upload page loads")
            
            # Check for VERSION 2.0
            if "VERSION 2.0" in r.text:
                print(f"   [OK] VERSION 2.0 detected")
            else:
                print(f"   [WARN] Cannot find VERSION 2.0 marker")
                
            # Check history check disabled
            if "history check disabled" in r.text.lower():
                print(f"   [OK] History check is disabled")
            else:
                print(f"   [WARN] History check may still be active")
        else:
            print(f"   [WARN] Status: {r.status_code}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    # Test 3: Analysis page
    print("\n3. Testing Analysis Page (/analysis)...")
    try:
        r = requests.get(f"{BASE_URL}/analysis", timeout=5)
        if r.status_code == 200:
            print(f"   [OK] Analysis page loads")
            
            # Check for transcript elements
            if "transcriptBody" in r.text:
                print(f"   [OK] Has #transcriptBody element")
            else:
                print(f"   [WARN] Missing #transcriptBody element")
                
            # Check cleanup functions removed
            if "clearTranscriptFromWrongPlaces" in r.text:
                print(f"   [WARN] Old cleanup function still exists!")
            else:
                print(f"   [OK] Old cleanup functions removed")
        else:
            print(f"   [WARN] Status: {r.status_code}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    # Test 4: Export endpoints
    print("\n4. Testing Export Endpoints...")
    try:
        r = requests.get(f"{BASE_URL}/api/export/txt", timeout=5)
        if r.status_code == 404:
            print(f"   [ERROR] /api/export/txt NOT FOUND")
        else:
            print(f"   [OK] /api/export/txt exists (status: {r.status_code})")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        
    try:
        r = requests.get(f"{BASE_URL}/api/export/docx", timeout=5)
        if r.status_code == 404:
            print(f"   [ERROR] /api/export/docx NOT FOUND")
        else:
            print(f"   [OK] /api/export/docx exists (status: {r.status_code})")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    # Test 5: Upload API with BOM file
    print("\n5. Testing File Upload with BOM...")
    content = "Test content with Vietnamese: aeiou"
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig',
                                     suffix='.txt', delete=False) as f:
        f.write(content)
        test_file = f.name
    
    try:
        with open(test_file, 'rb') as f:
            files = {'text_file': ('test.txt', f)}
            data = {
                'file_type': 'text',
                'transcribe_lang': 'vi',
                'meeting_type': 'meeting',
                'output_lang': 'vi'
            }
            
            r = requests.post(
                f"{BASE_URL}/api/upload/process",
                files=files,
                data=data,
                timeout=90
            )
            
            print(f"   Upload status: {r.status_code}")
            
            if r.status_code == 200:
                result = r.json()
                print(f"   [OK] Upload successful")
                print(f"   Transcript length: {len(result.get('transcript', ''))}")
            elif r.status_code == 500:
                error = r.json().get('error', '')
                if 'gbk' in error.lower() or 'codec' in error.lower():
                    print(f"   [ERROR] ENCODING ERROR: {error}")
                else:
                    print(f"   [WARN] Error (not encoding): {error[:100]}")
            else:
                print(f"   [WARN] Status {r.status_code}: {r.json().get('error', '')[:100]}")
                
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    finally:
        Path(test_file).unlink(missing_ok=True)
    
    # Test 6: Check export directory
    print("\n6. Checking Export Directory...")
    export_dir = Path("e:/ChatBot/meeting-transcript-chatbot2/data/exports")
    if export_dir.exists():
        print(f"   [OK] Export directory exists")
    else:
        print(f"   [WARN] Export directory MISSING: {export_dir}")
        print(f"   FIX: Create directory")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_pages()
