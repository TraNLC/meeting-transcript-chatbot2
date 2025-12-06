import requests
import json
import os
import time

BASE_URL = "http://localhost:5000"
SAMPLE_FILE_PATH = r"C:\Users\Admin\.gemini\antigravity\brain\68e3b5f5-b31b-469c-89d1-d43cac149e1c\sample.txt"

def print_status(message, status):
    icon = "[PASS]" if status == "PASS" else "[FAIL]"
    print(f"{icon} [{status}] {message}")

def verify_app_launch():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print_status("Server is reachable", "PASS")
            return True
        else:
            print_status(f"Server returned status code {response.status_code}", "FAIL")
            return False
    except Exception as e:
        print_status(f"Could not connect to server: {e}", "FAIL")
        return False

def verify_upload():
    if not os.path.exists(SAMPLE_FILE_PATH):
        print_status(f"Sample file not found at {SAMPLE_FILE_PATH}", "FAIL")
        return False

    url = f"{BASE_URL}/api/upload/process"
    files = {
        'text_file': ('sample.txt', open(SAMPLE_FILE_PATH, 'rb'), 'text/plain')
    }
    data = {
        'file_type': 'text',
        'meeting_type': 'project',
        'output_lang': 'vi',
        'transcribe_lang': 'vi'
    }

    try:
        print("\n--- Testing Upload... ---")
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            res_json = response.json()
            if "summary" in res_json:
                print_status("Upload and analysis successful", "PASS")
                return True
            else:
                print_status(f"Upload response missing summary: {res_json}", "FAIL")
                return False
        else:
            print_status(f"Upload failed with {response.status_code}: {response.text}", "FAIL")
            return False
    except Exception as e:
        print_status(f"Upload exception: {e}", "FAIL")
        return False

def verify_chat():
    url = f"{BASE_URL}/api/chat"
    payload = {
        "message": "Tóm tắt lại cuộc họp này",
        "history": [] # Simplified API expects history but we found it might not need it for simple Q&A now
    }
    
    try:
        print("\n--- Testing Chat... ---")
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            res_json = response.json()
            if "answer" in res_json:
                print_status("Chat response received", "PASS")
                # print(f"   AI Answer: {res_json['answer'][:100]}...")
                try:
                   print(f"   AI Answer: {res_json['answer'][:50]}...")
                except:
                   print("   AI Answer: (unicode content hidden)")
                return True
            else:
                print_status(f"Chat response missing answer: {res_json}", "FAIL")
                return False
        else:
            print_status(f"Chat failed with {response.status_code}: {response.text}", "FAIL")
            return False
    except Exception as e:
        print_status(f"Chat exception: {e}", "FAIL")
        return False

def verify_history():
    url = f"{BASE_URL}/api/chat/history/list"
    try:
        print("\n--- Testing History... ---")
        response = requests.get(url)
        if response.status_code == 200:
            res_json = response.json()
            if "dropdown" in res_json and isinstance(res_json["dropdown"], list):
                print_status(f"History list retrieved ({len(res_json['dropdown'])} items)", "PASS")
                return True
            else:
                print_status(f"Invalid history format: {res_json}", "FAIL")
                return False
        else:
            print_status(f"History failed with {response.status_code}", "FAIL")
            return False
    except Exception as e:
        print_status(f"History exception: {e}", "FAIL")
        return False

def verify_export():
    try:
        print("\n--- Testing Export... ---")
        # Test TXT Export
        url_txt = f"{BASE_URL}/api/export/txt"
        response_txt = requests.get(url_txt)
        if response_txt.status_code == 200:
            print_status("Export TXT successful", "PASS")
        else:
            print_status(f"Export TXT failed: {response_txt.status_code} - {response_txt.text}", "FAIL")

        # Test DOCX Export
        url_docx = f"{BASE_URL}/api/export/docx"
        response_docx = requests.get(url_docx)
        if response_docx.status_code == 200:
            print_status("Export DOCX successful", "PASS")
        else:
            print_status(f"Export DOCX failed: {response_docx.status_code} - {response_docx.text}", "FAIL")
            
        return True
    except Exception as e:
         print_status(f"Export exception: {e}", "FAIL")
         return False

if __name__ == "__main__":
    print("[START] Starting E2E API Verification...")
    
    if verify_app_launch():
        verify_upload()
        verify_chat()
        verify_history()
        verify_export()
    
    print("\n[DONE] Verification Complete.")
