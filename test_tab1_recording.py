"""
Comprehensive Test Suite for Tab 1 - Mic Recording
Tests all aspects of the recording functionality with detailed failure reporting
"""

import sys
import io

# Configure UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import json
import time
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import traceback

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"
COLAB_URL = os.getenv('COLAB_WHISPERX_URL')

# Test Results Storage
test_results = []
failed_tests = []

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_test_start(test_name):
    print(f"\n{Colors.BOLD}> Testing: {test_name}{Colors.ENDC}")

def print_success(text, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{Colors.OKGREEN}[PASS] {text}{Colors.ENDC}")

def print_error(text, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{Colors.FAIL}[FAIL] {text}{Colors.ENDC}")

def print_info(text, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")

def print_warning(text, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{Colors.WARNING}[WARN] {text}{Colors.ENDC}")

def record_test_result(test_name, passed, error_msg=None, details=None):
    """Record test result for final summary"""
    result = {
        'name': test_name,
        'passed': passed,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if error_msg:
        result['error'] = error_msg
    if details:
        result['details'] = details
    
    test_results.append(result)
    
    if not passed:
        failed_tests.append(result)

class Tab1RecordingTester:
    """Comprehensive tester for Tab 1 Mic Recording functionality"""
    
    def __init__(self):
        self.driver = None
        self.test_audio_file = None
        
    def setup_browser(self):
        """Setup Selenium WebDriver with fake media stream"""
        print_test_start("Browser Setup")
        try:
            chrome_options = Options()
            # Allow microphone access without prompting
            chrome_options.add_argument("--use-fake-ui-for-media-stream")
            chrome_options.add_argument("--use-fake-device-for-media-stream")
            # Use a fake audio file for testing
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-file-access-from-files")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(1920, 1080)
            
            print_success("Browser initialized successfully")
            record_test_result("Browser Setup", True)
            return True
        except Exception as e:
            error_msg = f"Failed to setup browser: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("Browser Setup", False, error_msg)
            return False
    
    def test_page_load(self):
        """Test if recording page loads correctly"""
        print_test_start("Page Load")
        try:
            self.driver.get(f"{BASE_URL}/record")
            
            # Wait for page to load - look for tab class instead of ID
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "record-tab"))
            )
            
            print_success("Recording page loaded successfully")
            print_info(f"Page URL: {self.driver.current_url}", indent=1)
            record_test_result("Page Load", True)
            return True
        except TimeoutException:
            error_msg = "Page load timeout - record-tab class not found"
            print_error(error_msg)
            print_info(f"Current URL: {self.driver.current_url}", indent=1)
            record_test_result("Page Load", False, error_msg)
            return False
        except Exception as e:
            error_msg = f"Page load failed: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("Page Load", False, error_msg)
            return False
    
    def test_tab1_ui_elements(self):
        """Test if all Tab 1 UI elements are present"""
        print_test_start("Tab 1 UI Elements")
        
        elements_to_check = {
            'micPanel': 'Mic Panel Container',
            'micRecordBtn': 'Record Button (Toggle Start/Stop)',
            'micTimer': 'Recording Timer',
            'micStatus': 'Recording Status Display',
            'micSaveSection': 'Save Section',
            'micSaveBtn': 'Save Button',
            'micDiscardBtn': 'Discard Button'
        }
        
        all_present = True
        missing_elements = []
        
        for element_id, description in elements_to_check.items():
            try:
                element = self.driver.find_element(By.ID, element_id)
                print_success(f"{description} found (ID: {element_id})")
            except NoSuchElementException:
                print_error(f"{description} NOT FOUND (ID: {element_id})")
                missing_elements.append(element_id)
                all_present = False
        
        if all_present:
            record_test_result("Tab 1 UI Elements", True)
        else:
            error_msg = f"Missing elements: {', '.join(missing_elements)}"
            record_test_result("Tab 1 UI Elements", False, error_msg, 
                             {'missing_elements': missing_elements})
        
        return all_present
    
    def test_record_button_clickable(self):
        """Test if record button is clickable"""
        print_test_start("Record Button Clickable")
        try:
            record_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "micRecordBtn"))
            )
            
            # Check button properties
            is_displayed = record_btn.is_displayed()
            is_enabled = record_btn.is_enabled()
            
            print_info(f"Button displayed: {is_displayed}", indent=1)
            print_info(f"Button enabled: {is_enabled}", indent=1)
            
            if is_displayed and is_enabled:
                print_success("Record button is clickable")
                record_test_result("Record Button Clickable", True)
                return True
            else:
                error_msg = f"Button not clickable - displayed: {is_displayed}, enabled: {is_enabled}"
                print_error(error_msg)
                record_test_result("Record Button Clickable", False, error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Failed to check button: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("Record Button Clickable", False, error_msg)
            return False
    
    def test_recording_flow(self):
        """Test the complete recording flow"""
        print_test_start("Recording Flow (Start → Record → Stop)")
        
        try:
            # Step 1: Click record button to start
            print_info("Step 1: Clicking record button to start...", indent=1)
            record_btn = self.driver.find_element(By.ID, "micRecordBtn")
            record_btn.click()
            time.sleep(1)
            
            # Step 2: Check if recording started
            print_info("Step 2: Checking recording status...", indent=1)
            status_element = self.driver.find_element(By.ID, "micStatus")
            status_text = status_element.text
            print_info(f"Status: {status_text}", indent=2)
            
            # Step 3: Wait for recording (simulate 3 seconds)
            print_info("Step 3: Recording for 3 seconds...", indent=1)
            time.sleep(3)
            
            # Step 4: Check timer is running
            timer_element = self.driver.find_element(By.ID, "micTimer")
            timer_text = timer_element.text
            print_info(f"Timer: {timer_text}", indent=2)
            
            # Step 5: Stop recording (click same button again)
            print_info("Step 4: Stopping recording (clicking button again)...", indent=1)
            record_btn = self.driver.find_element(By.ID, "micRecordBtn")
            record_btn.click()
            time.sleep(2)
            
            print_success("Recording flow completed successfully")
            record_test_result("Recording Flow", True)
            return True
            
        except Exception as e:
            error_msg = f"Recording flow failed: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("Recording Flow", False, error_msg)
            return False
    
    def test_api_save_endpoint(self):
        """Test the save-only API endpoint"""
        print_test_start("API Save Endpoint")
        
        try:
            # Create test audio file
            test_audio_dir = Path('data/test_audio')
            test_audio_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_audio_dir / 'test_mic_recording.webm'
            
            # Create minimal WebM file
            webm_header = bytes([
                0x1A, 0x45, 0xDF, 0xA3, 0x9F, 0x42, 0x86, 0x81, 0x01,
                0x42, 0xF7, 0x81, 0x01, 0x42, 0xF2, 0x81, 0x04
            ])
            
            with open(test_file, 'wb') as f:
                f.write(webm_header)
            
            print_info(f"Test file created: {test_file}", indent=1)
            
            # Test API endpoint
            with open(test_file, 'rb') as f:
                files = {'audio': ('test_mic.webm', f, 'audio/webm')}
                data = {'type': 'mic'}
                response = requests.post(
                    f"{API_BASE}/recording/save-only",
                    files=files,
                    data=data,
                    timeout=10
                )
            
            print_info(f"Response status: {response.status_code}", indent=1)
            
            if response.status_code == 200:
                result = response.json()
                print_info(f"Response: {json.dumps(result, indent=2)}", indent=1)
                
                if result.get('success'):
                    print_success("API endpoint working correctly")
                    print_info(f"Saved file: {result.get('filename')}", indent=2)
                    record_test_result("API Save Endpoint", True)
                    return True
                else:
                    error_msg = f"API returned success=false: {result.get('error')}"
                    print_error(error_msg)
                    record_test_result("API Save Endpoint", False, error_msg, result)
                    return False
            else:
                error_msg = f"API returned status {response.status_code}"
                print_error(error_msg)
                print_info(f"Response: {response.text}", indent=1)
                record_test_result("API Save Endpoint", False, error_msg)
                return False
                
        except Exception as e:
            error_msg = f"API test failed: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("API Save Endpoint", False, error_msg)
            return False
    
    def test_whisperx_integration(self):
        """Test Whisper X transcription integration"""
        print_test_start("Whisper X Integration")
        
        if not COLAB_URL:
            error_msg = "COLAB_WHISPERX_URL not configured in .env"
            print_warning(error_msg)
            print_info("Skipping Whisper X test", indent=1)
            record_test_result("Whisper X Integration", False, error_msg)
            return False
        
        try:
            # Test health endpoint
            print_info(f"Testing Colab URL: {COLAB_URL}", indent=1)
            response = requests.get(f"{COLAB_URL}/health", timeout=5)
            
            if response.status_code == 200:
                print_success("Whisper X server is reachable")
                record_test_result("Whisper X Integration", True)
                return True
            else:
                error_msg = f"Whisper X server returned status {response.status_code}"
                print_error(error_msg)
                record_test_result("Whisper X Integration", False, error_msg)
                return False
                
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Whisper X server"
            print_error(error_msg)
            print_info("Make sure Google Colab notebook is running", indent=1)
            record_test_result("Whisper X Integration", False, error_msg)
            return False
        except Exception as e:
            error_msg = f"Whisper X test failed: {str(e)}"
            print_error(error_msg)
            print_info(f"Traceback: {traceback.format_exc()}", indent=1)
            record_test_result("Whisper X Integration", False, error_msg)
            return False
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
            print_info("Browser closed")

def print_final_summary():
    """Print comprehensive test summary"""
    print_header("COMPREHENSIVE TEST SUMMARY")
    
    total = len(test_results)
    passed = sum(1 for r in test_results if r['passed'])
    failed = total - passed
    
    print(f"{Colors.BOLD}Total Tests: {total}{Colors.ENDC}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    # Detailed results
    print(f"\n{Colors.BOLD}Detailed Results:{Colors.ENDC}")
    for result in test_results:
        status = "[PASS]" if result['passed'] else "[FAIL]"
        color = Colors.OKGREEN if result['passed'] else Colors.FAIL
        print(f"{color}{status} {result['name']}{Colors.ENDC}")
        if not result['passed'] and 'error' in result:
            print(f"  {Colors.FAIL}Error: {result['error']}{Colors.ENDC}")
    
    # Failed tests details
    if failed_tests:
        print(f"\n{Colors.BOLD}{Colors.FAIL}FAILED TESTS DETAILS:{Colors.ENDC}")
        print(f"{Colors.FAIL}{'='*80}{Colors.ENDC}")
        
        for i, test in enumerate(failed_tests, 1):
            print(f"\n{Colors.FAIL}{Colors.BOLD}[{i}] {test['name']}{Colors.ENDC}")
            print(f"{Colors.FAIL}Time: {test['timestamp']}{Colors.ENDC}")
            print(f"{Colors.FAIL}Error: {test['error']}{Colors.ENDC}")
            if 'details' in test:
                print(f"{Colors.FAIL}Details: {json.dumps(test['details'], indent=2)}{Colors.ENDC}")
    
    # Final verdict
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    if passed == total:
        print_success("\nALL TESTS PASSED! Tab 1 Recording is working perfectly!")
    else:
        print_error(f"\n{failed} TEST(S) FAILED - Please review errors above and fix issues")
        print_info("\nNext steps:")
        for i, test in enumerate(failed_tests, 1):
            print_info(f"  {i}. Fix: {test['name']}", indent=1)

def main():
    """Run comprehensive Tab 1 recording tests"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("="*80)
    print("          COMPREHENSIVE TAB 1 (MIC RECORDING) TEST SUITE                    ")
    print("                    Detailed Testing & Failure Reporting                    ")
    print("="*80)
    print(f"{Colors.ENDC}")
    
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Testing server: {BASE_URL}")
    print_info(f"Whisper X URL: {COLAB_URL or 'Not configured'}")
    
    tester = Tab1RecordingTester()
    
    try:
        # Run all tests in sequence
        if tester.setup_browser():
            tester.test_page_load()
            tester.test_tab1_ui_elements()
            tester.test_record_button_clickable()
            tester.test_recording_flow()
        
        # API tests (don't require browser)
        tester.test_api_save_endpoint()
        tester.test_whisperx_integration()
        
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
        print_info(f"Traceback: {traceback.format_exc()}")
    finally:
        tester.cleanup()
    
    # Print final summary
    print_final_summary()
    
    print(f"\n{Colors.OKCYAN}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
