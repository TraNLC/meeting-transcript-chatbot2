"""Main Application V2 - 6 Tabs Reorganized.

Cleaner structure with separate tabs for better UX.
"""

import gradio as gr
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Auto-setup ffmpeg PATH
try:
    from src.utils.ffmpeg_helper import setup_ffmpeg_path
    setup_ffmpeg_path()
except Exception as e:
    print(f"WARNING: Could not setup ffmpeg: {e}")

# Import all handler functions from gradio_app_final
from src.ui.gradio_app_final import (
    transcribe_audio_whisper,
    save_recording_and_transcribe,
    process_file,
    chat_with_ai,
    export_to_txt,
    export_to_docx,
    refresh_history,
    load_history,
    get_recordings_list_ui,
    load_recording_info_ui,
    delete_recording_ui,
    get_vectordb_stats_ui,
    search_meetings_ui,
    search_recordings_ui
)

# Import tabs
from tabs_v2 import (
    create_recording_tab,
    create_upload_tab,
    create_chat_tab,
    create_analysis_history_tab,
    create_recording_history_tab,
    create_search_export_tab,
    create_checklist_tab
)

# Import checklist manager
from src.data.checklist_manager import get_checklist_manager


# Custom CSS - Navy Blue Theme
custom_css = """
/* Global Styles - Allow Scroll */
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    padding-top: 70px !important;
    min-height: 100vh;
    overflow-y: auto !important;
}

/* Fixed Header - Navy Blue */
.main-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    text-align: center;
    padding: 0.6rem 2rem;
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
}

.main-header h1 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.1rem 0 0 0;
    font-size: 0.8rem;
    opacity: 0.9;
}

/* Tabs Styling - Navy */
.tabs {
    margin-top: 0.3rem;
}

button.selected {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
    color: white !important;
}

/* Buttons - Navy */
.primary {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
    border: none !important;
    color: white !important;
}

.primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4) !important;
}

/* Cards & Sections */
.gr-box {
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}

.gr-box:hover {
    border-color: #2563eb;
}

/* Tab Content - Scrollable */
.tabitem {
    overflow-y: auto !important;
    max-height: calc(100vh - 120px);
}

/* Compact spacing */
.gr-form {
    gap: 0.3rem !important;
}

.gr-padded {
    padding: 0.4rem !important;
}

/* Smaller textboxes */
textarea {
    min-height: 60px !important;
}
"""


# Build UI
with gr.Blocks(css=custom_css, title="Meeting Analyzer Pro", theme=gr.themes.Soft()) as demo:
    
    # Fixed Header
    gr.HTML("""
    <div class="main-header">
        <h1>🎯 Meeting Analyzer Pro</h1>
        <p>Phân Tích Cuộc Họp với AI</p>
    </div>
    """)
    
    # Main tabs
    with gr.Tabs() as tabs:
        tab1 = create_recording_tab()
        tab2 = create_upload_tab()
        tab3 = create_chat_tab()
        tab4 = create_analysis_history_tab()
        tab5 = create_recording_history_tab()
        tab6 = create_search_export_tab()
        tab7 = create_checklist_tab()
    
    # Footer removed for compact layout
    
    # Checklist handler functions
    def refresh_checklist(filter_status):
        """Refresh checklist display."""
        manager = get_checklist_manager()
        data = manager.to_dataframe_data(filter_status)
        stats = manager.get_statistics()
        stats_md = f"""
- **Tổng tasks:** {stats['total']}
- **Hoàn thành:** {stats['completed']} ✅
- **Chưa xong:** {stats['pending']} ⏳
- **Tỷ lệ:** {stats['completion_rate']}%
        """
        return data, stats_md
    
    # Checklist handlers - simplified
    def add_new_task(task, assignee, deadline, priority):
        """Add a new task."""
        if not task.strip():
            return None, None
        manager = get_checklist_manager()
        manager.add_task(task, assignee, deadline, priority, source="manual")
        data = manager.to_dataframe_data("all")
        stats = manager.get_statistics()
        stats_md = f"""
- **Tổng:** {stats['total']}
- **Hoàn thành:** {stats['completed']} ✅
- **Chưa xong:** {stats['pending']} ⏳
- **Tỷ lệ:** {stats['completion_rate']}%
        """
        return data, stats_md
    
    def import_from_analysis():
        """Import action items from current analysis."""
        manager = get_checklist_manager()
        # Demo: import sample tasks
        count = manager.import_from_analysis("""
        - Hoàn thành báo cáo Q4 (Nguyễn Văn A, 30/11/2025)
        - Review code module authentication (Trần Văn B, 25/11/2025)
        - Chuẩn bị slide cho meeting tuần sau (Lê Thị C, 28/11/2025)
        """, source="analysis")
        if count > 0:
            return f"✅ Đã import {count} action items!"
        return "⚠️ Không có action items để import"
    
    # Connect event handlers
    from connect_events import (
        connect_recording_events,
        connect_upload_events,
        connect_chat_events,
        connect_analysis_history_events,
        connect_recording_history_events,
        connect_search_export_events
    )
    
    handlers = {
        'transcribe': transcribe_audio_whisper,
        'save_recording': save_recording_and_transcribe,
        'process_file': process_file,
        'chat': chat_with_ai,
        'refresh_history': refresh_history,
        'load_history': load_history,
        'refresh_recordings': get_recordings_list_ui,
        'load_recording_info': load_recording_info_ui,
        'delete_recording': delete_recording_ui,
        'get_stats': get_vectordb_stats_ui,
        'search_meetings': search_meetings_ui,
        'search_recordings': search_recordings_ui,
        'export_txt': export_to_txt,
        'export_docx': export_to_docx,
    }
    
    connect_recording_events(tab1, handlers)
    connect_upload_events(tab2, handlers)
    connect_chat_events(tab3, handlers)
    connect_analysis_history_events(tab4, handlers)
    connect_recording_history_events(tab5, handlers)
    connect_search_export_events(tab6, handlers)
    
    # Connect checklist events - simplified
    tab7['refresh_btn'].click(
        fn=refresh_checklist,
        inputs=[tab7['filter']],
        outputs=[tab7['checklist'], tab7['stats']]
    )
    
    tab7['filter'].change(
        fn=refresh_checklist,
        inputs=[tab7['filter']],
        outputs=[tab7['checklist'], tab7['stats']]
    )
    
    tab7['add_btn'].click(
        fn=add_new_task,
        inputs=[tab7['new_task'], tab7['new_assignee'], tab7['new_deadline'], tab7['new_priority']],
        outputs=[tab7['checklist'], tab7['stats']]
    )
    
    tab7['import_btn'].click(
        fn=import_from_analysis,
        outputs=[tab7['import_status']]
    )
    
    # Auto-load on startup
    demo.load(
        fn=get_vectordb_stats_ui,
        outputs=[tab6['stats_display']]
    ).then(
        fn=get_recordings_list_ui,
        outputs=[tab5['dropdown'], tab5['stats']]
    ).then(
        fn=refresh_history,
        outputs=[tab4['dropdown'], tab4['info']]
    ).then(
        fn=lambda: refresh_checklist("all"),
        outputs=[tab7['checklist'], tab7['stats']]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="localhost",
        server_port=7779,
        share=False
    )
