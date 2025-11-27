"""Automated Self-Test for All Tabs - Based on Test Cases.

Tests all functionality without running the app.
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

# Test results
test_results = []
passed = 0
failed = 0


def log_test(test_id, test_name, status, message=""):
    """Log test result."""
    global passed, failed
    
    result = {
        'id': test_id,
        'name': test_name,
        'status': status,
        'message': message
    }
    test_results.append(result)
    
    if status == "PASS":
        passed += 1
        print(f"✓ {test_id}: {test_name}")
    else:
        failed += 1
        print(f"✗ {test_id}: {test_name}")
    
    if message:
        print(f"  → {message}")


print("=" * 70)
print("MEETING ANALYZER PRO - AUTOMATED SELF-TEST")
print("=" * 70)
print()

# ============================================================================
# TC_01: Recording Tab Tests
# ============================================================================
print("📋 TC_01: Recording Tab")
print("-" * 70)

try:
    import gradio as gr
    from src.ui.tabs_v2.tab_recording import create_recording_tab
    
    with gr.Blocks():
        tab = create_recording_tab()
        
        # TC_01.1: Check tab structure
        required_keys = ['lang', 'audio', 'transcript', 'title', 'save_btn', 'clear_btn', 'save_status', 'id']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_01.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_01.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_01.2: Check language options
        lang_choices = tab['lang'].choices
        if len(lang_choices) >= 5:
            log_test("TC_01.2", "Language support", "PASS", f"{len(lang_choices)} languages available")
        else:
            log_test("TC_01.2", "Language support", "FAIL", f"Only {len(lang_choices)} languages")
        
        # TC_01.3: Check audio component
        if tab['audio'].sources == ["microphone"]:
            log_test("TC_01.3", "Microphone recording", "PASS", "Audio source configured correctly")
        else:
            log_test("TC_01.3", "Microphone recording", "FAIL", "Audio source not configured")
        
        # TC_01.4: Check buttons
        if tab['save_btn'] and tab['clear_btn']:
            log_test("TC_01.4", "Action buttons", "PASS", "Save and Clear buttons present")
        else:
            log_test("TC_01.4", "Action buttons", "FAIL", "Buttons missing")
            
except Exception as e:
    log_test("TC_01", "Recording Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_02: Upload & Analysis Tab Tests
# ============================================================================
print("📋 TC_02: Upload & Analysis Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_upload import create_upload_tab
    
    with gr.Blocks():
        tab = create_upload_tab()
        
        # TC_02.1: Check tab structure
        required_keys = ['file', 'meeting_type', 'output_lang', 'process_btn', 'status', 'summary', 'topics', 'actions', 'decisions']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_02.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_02.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_02.2: Check file types
        file_types = tab['file'].file_types
        if '.txt' in file_types and '.docx' in file_types:
            log_test("TC_02.2", "File type support", "PASS", "TXT and DOCX supported")
        else:
            log_test("TC_02.2", "File type support", "FAIL", f"File types: {file_types}")
        
        # TC_02.3: Check meeting types
        meeting_types = [choice[1] for choice in tab['meeting_type'].choices]
        if 'meeting' in meeting_types and 'workshop' in meeting_types:
            log_test("TC_02.3", "Meeting types", "PASS", f"{len(meeting_types)} types available")
        else:
            log_test("TC_02.3", "Meeting types", "FAIL", "Missing meeting types")
        
        # TC_02.4: Check output languages
        output_langs = tab['output_lang'].choices
        if len(output_langs) >= 5:
            log_test("TC_02.4", "Output languages", "PASS", f"{len(output_langs)} languages")
        else:
            log_test("TC_02.4", "Output languages", "FAIL", f"Only {len(output_langs)} languages")
            
except Exception as e:
    log_test("TC_02", "Upload & Analysis Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_03: Chat Tab Tests
# ============================================================================
print("📋 TC_03: Chat with AI Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_chat import create_chat_tab
    
    with gr.Blocks():
        tab = create_chat_tab()
        
        # TC_03.1: Check tab structure
        required_keys = ['chatbot', 'input', 'send_btn', 'clear_btn', 'quick_btns']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_03.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_03.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_03.2: Check chatbot type
        if tab['chatbot'].type == "messages":
            log_test("TC_03.2", "Chatbot format", "PASS", "Using modern 'messages' format")
        else:
            log_test("TC_03.2", "Chatbot format", "FAIL", f"Using deprecated '{tab['chatbot'].type}' format")
        
        # TC_03.3: Check quick buttons
        if len(tab['quick_btns']) >= 5:
            log_test("TC_03.3", "Quick question buttons", "PASS", f"{len(tab['quick_btns'])} buttons available")
        else:
            log_test("TC_03.3", "Quick question buttons", "FAIL", f"Only {len(tab['quick_btns'])} buttons")
            
except Exception as e:
    log_test("TC_03", "Chat Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_04: Analysis History Tab Tests
# ============================================================================
print("📋 TC_04: Analysis History Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_analysis_history import create_analysis_history_tab
    
    with gr.Blocks():
        tab = create_analysis_history_tab()
        
        # TC_04.1: Check tab structure
        required_keys = ['dropdown', 'refresh_btn', 'info', 'summary', 'topics', 'actions', 'decisions', 'load_btn', 'delete_btn', 'stats']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_04.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_04.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_04.2: Check action buttons
        if tab['load_btn'] and tab['delete_btn'] and tab['refresh_btn']:
            log_test("TC_04.2", "Action buttons", "PASS", "Load, Delete, Refresh buttons present")
        else:
            log_test("TC_04.2", "Action buttons", "FAIL", "Some buttons missing")
        
        # TC_04.3: Check preview sections
        if tab['summary'] and tab['topics'] and tab['actions'] and tab['decisions']:
            log_test("TC_04.3", "Preview sections", "PASS", "All 4 preview sections present")
        else:
            log_test("TC_04.3", "Preview sections", "FAIL", "Some sections missing")
            
except Exception as e:
    log_test("TC_04", "Analysis History Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_05: Recording History Tab Tests
# ============================================================================
print("📋 TC_05: Recording History Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_recording_history import create_recording_history_tab
    
    with gr.Blocks():
        tab = create_recording_history_tab()
        
        # TC_05.1: Check tab structure
        required_keys = ['dropdown', 'refresh_btn', 'stats', 'info', 'notes', 'transcript', 'metadata', 'player', 'play_btn', 'delete_btn', 'status']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_05.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_05.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_05.2: Check audio player
        if tab['player']:
            log_test("TC_05.2", "Audio player", "PASS", "Audio player component present")
        else:
            log_test("TC_05.2", "Audio player", "FAIL", "Audio player missing")
        
        # TC_05.3: Check info tabs
        if tab['transcript'] and tab['notes'] and tab['metadata']:
            log_test("TC_05.3", "Info tabs", "PASS", "Transcript, Notes, Metadata tabs present")
        else:
            log_test("TC_05.3", "Info tabs", "FAIL", "Some info tabs missing")
            
except Exception as e:
    log_test("TC_05", "Recording History Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_06: Search & Export Tab Tests
# ============================================================================
print("📋 TC_06: Search & Export Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_search_export import create_search_export_tab
    
    with gr.Blocks():
        tab = create_search_export_tab()
        
        # TC_06.1: Check tab structure
        required_keys = ['stats_display', 'refresh_stats_btn', 'search_query', 'meeting_type_filter', 'n_results', 'search_btn', 'search_status', 'search_results', 'export_txt_btn', 'export_docx_btn', 'export_file']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_06.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_06.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_06.2: Check search components
        if tab['search_query'] and tab['search_btn'] and tab['search_results']:
            log_test("TC_06.2", "Search components", "PASS", "Query, Button, Results present")
        else:
            log_test("TC_06.2", "Search components", "FAIL", "Some search components missing")
        
        # TC_06.3: Check export buttons
        if tab['export_txt_btn'] and tab['export_docx_btn']:
            log_test("TC_06.3", "Export buttons", "PASS", "TXT and DOCX export available")
        else:
            log_test("TC_06.3", "Export buttons", "FAIL", "Export buttons missing")
        
        # TC_06.4: Check filters
        if tab['meeting_type_filter'] and tab['n_results']:
            log_test("TC_06.4", "Search filters", "PASS", "Meeting type and result count filters present")
        else:
            log_test("TC_06.4", "Search filters", "FAIL", "Some filters missing")
            
except Exception as e:
    log_test("TC_06", "Search & Export Tab", "FAIL", str(e))

print()

# ============================================================================
# TC_07: Checklist Tab Tests
# ============================================================================
print("📋 TC_07: Checklist Tab")
print("-" * 70)

try:
    from src.ui.tabs_v2.tab_checklist import create_checklist_tab
    
    with gr.Blocks():
        tab = create_checklist_tab()
        
        # TC_07.1: Check tab structure
        required_keys = ['filter', 'refresh_btn', 'checklist', 'new_task', 'new_assignee', 'new_deadline', 'new_priority', 'add_btn', 'stats', 'import_btn', 'import_status']
        missing = [k for k in required_keys if k not in tab]
        
        if missing:
            log_test("TC_07.1", "Tab structure", "FAIL", f"Missing keys: {missing}")
        else:
            log_test("TC_07.1", "Tab structure", "PASS", f"All {len(required_keys)} components present")
        
        # TC_07.2: Check task form
        if tab['new_task'] and tab['new_assignee'] and tab['new_deadline'] and tab['new_priority']:
            log_test("TC_07.2", "Task form", "PASS", "All task input fields present")
        else:
            log_test("TC_07.2", "Task form", "FAIL", "Some task fields missing")
        
        # TC_07.3: Check filter options
        filter_choices = [choice[1] for choice in tab['filter'].choices]
        if 'all' in filter_choices and 'pending' in filter_choices and 'completed' in filter_choices:
            log_test("TC_07.3", "Filter options", "PASS", "All, Pending, Completed filters available")
        else:
            log_test("TC_07.3", "Filter options", "FAIL", f"Filter options: {filter_choices}")
        
        # TC_07.4: Check action buttons
        if tab['add_btn'] and tab['import_btn'] and tab['refresh_btn']:
            log_test("TC_07.4", "Action buttons", "PASS", "Add, Import, Refresh buttons present")
        else:
            log_test("TC_07.4", "Action buttons", "FAIL", "Some buttons missing")
            
except Exception as e:
    log_test("TC_07", "Checklist Tab", "FAIL", str(e))

print()

# ============================================================================
# Integration Tests
# ============================================================================
print("📋 Integration Tests")
print("-" * 70)

# TC_INT.1: Check all modules can be imported
try:
    from src.audio.audio_manager import AudioManager
    from src.vectorstore.chroma_manager import ChromaManager
    from src.data.checklist_manager import ChecklistManager
    from src.ui.connect_events import (
        connect_recording_events,
        connect_upload_events,
        connect_chat_events
    )
    log_test("TC_INT.1", "Module imports", "PASS", "All core modules imported successfully")
except Exception as e:
    log_test("TC_INT.1", "Module imports", "FAIL", str(e))

# TC_INT.2: Check data directories exist
try:
    data_dirs = [
        Path('data/recordings'),
        Path('data/history'),
        Path('data/checklists')
    ]
    
    existing = [d for d in data_dirs if d.exists()]
    
    if len(existing) >= 2:
        log_test("TC_INT.2", "Data directories", "PASS", f"{len(existing)}/{len(data_dirs)} directories exist")
    else:
        log_test("TC_INT.2", "Data directories", "FAIL", f"Only {len(existing)}/{len(data_dirs)} directories exist")
except Exception as e:
    log_test("TC_INT.2", "Data directories", "FAIL", str(e))

# TC_INT.3: Check ffmpeg availability
try:
    from src.utils.ffmpeg_helper import check_ffmpeg
    if check_ffmpeg():
        log_test("TC_INT.3", "ffmpeg availability", "PASS", "ffmpeg is installed and accessible")
    else:
        log_test("TC_INT.3", "ffmpeg availability", "FAIL", "ffmpeg not found")
except Exception as e:
    log_test("TC_INT.3", "ffmpeg availability", "FAIL", str(e))

print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print(f"Total Tests: {passed + failed}")
print(f"✓ Passed: {passed}")
print(f"✗ Failed: {failed}")
print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
print()

if failed > 0:
    print("FAILED TESTS:")
    for result in test_results:
        if result['status'] == 'FAIL':
            print(f"  ✗ {result['id']}: {result['name']}")
            if result['message']:
                print(f"    → {result['message']}")
    print()

print("=" * 70)

# Exit with appropriate code
sys.exit(0 if failed == 0 else 1)
