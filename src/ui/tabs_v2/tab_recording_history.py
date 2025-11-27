"""Tab 5: Recording History - Manage saved recordings."""

import gradio as gr


def create_recording_history_tab():
    """Create Recording History tab - Smart & Compact Layout."""
    
    with gr.Tab("🎙️ Lịch Sử Ghi Âm"):
        with gr.Row():
            # Left: Recording List & Actions
            with gr.Column(scale=1):
                gr.Markdown("### 🎤 Danh Sách")
                
                with gr.Row():
                    recordings_dropdown = gr.Dropdown(
                        label="Chọn ghi âm",
                        choices=[],
                        interactive=True,
                        scale=3,
                        show_label=False
                    )
                    refresh_recordings_btn = gr.Button("🔄", scale=1)
                
                # Recording info card
                recording_info_display = gr.Markdown(
                    "_Chọn một ghi âm để xem chi tiết_",
                    elem_classes="info-box"
                )
                
                # Action buttons
                with gr.Row():
                    play_btn = gr.Button("▶️ Phát", variant="primary", scale=2)
                    delete_recording_btn = gr.Button("🗑️", variant="stop", scale=1)
                
                delete_status = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    lines=1
                )
                
                # Quick stats
                gr.Markdown("---")
                recordings_stats = gr.Markdown("""
                **📊 Thống kê:**
                - Tổng: 0 ghi âm
                - Tổng thời lượng: 0 phút
                """)
            
            # Right: Audio Player & Details
            with gr.Column(scale=2):
                gr.Markdown("### 🎵 Audio Player")
                
                audio_player = gr.Audio(
                    label="",
                    interactive=False,
                    show_label=False
                )
                
                # Tabs for different info
                with gr.Tabs():
                    with gr.Tab("📝 Transcript"):
                        transcript_display = gr.Textbox(
                            lines=10,
                            interactive=False,
                            show_label=False,
                            placeholder="Transcript sẽ hiển thị ở đây..."
                        )
                    
                    with gr.Tab("📋 Ghi chú"):
                        recording_notes_display = gr.Textbox(
                            lines=10,
                            interactive=False,
                            show_label=False,
                            placeholder="Ghi chú về ghi âm..."
                        )
                    
                    with gr.Tab("ℹ️ Thông tin"):
                        metadata_display = gr.Markdown("""
                        **Chi tiết:**
                        - ID: -
                        - Ngày: -
                        - Thời lượng: -
                        - Ngôn ngữ: -
                        - Trạng thái: -
                        """)
    
    return {
        'dropdown': recordings_dropdown,
        'refresh_btn': refresh_recordings_btn,
        'stats': recordings_stats,
        'info': recording_info_display,
        'notes': recording_notes_display,
        'transcript': transcript_display,
        'metadata': metadata_display,
        'player': audio_player,
        'play_btn': play_btn,
        'delete_btn': delete_recording_btn,
        'status': delete_status
    }
