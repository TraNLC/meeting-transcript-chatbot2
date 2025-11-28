"""Tab 1: Recording - Audio recording and transcription."""

import gradio as gr
from datetime import datetime


def create_recording_tab():
    """Create Recording tab - Clean Layout 1:2."""
    
    with gr.Tab("🎙️ Ghi Âm"):
        with gr.Row():
            # Left: Controls (1)
            with gr.Column(scale=1):
                gr.Markdown("### 🎤 Ghi Âm")
                
                recording_title_input = gr.Textbox(
                    label="Tiêu đề",
                    placeholder=f"Ghi âm {datetime.now().strftime('%d/%m/%Y')}",
                )
                
                recording_lang_input = gr.Dropdown(
                    label="Ngôn ngữ",
                    choices=[
                        ("Tiếng Việt", "vi"),
                        ("English", "en"),
                        ("日本語", "ja"),
                        ("한국어", "ko"),
                        ("中文", "zh")
                    ],
                    value="vi"
                )
                
                audio_recorder_main = gr.Audio(
                    sources=["microphone", "upload"],  # Cho phép ghi âm HOẶC upload
                    type="filepath",
                    label="",
                    waveform_options={"show_recording_waveform": True},
                    show_label=False
                )
                
                with gr.Row():
                    transcribe_btn = gr.Button("🎤 Transcribe", variant="secondary", scale=1)
                    save_recording_btn = gr.Button("💾 Lưu", variant="primary", scale=1)
                    clear_recording_btn = gr.Button("🗑️ Hủy", variant="secondary", scale=1)
                
                save_status = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=1,
                    show_label=False,
                    visible=False  # Ẩn khi chưa có status
                )
                
                recording_id_hidden = gr.Textbox(visible=False)
            
            # Right: Transcript (2)
            with gr.Column(scale=2):
                gr.Markdown("### 📝 Transcript")
                
                transcript_display = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=25,
                    show_label=False,
                    placeholder="Nhấn Stop để tự động transcribe..."
                )
    
    return {
        'lang': recording_lang_input,
        'audio': audio_recorder_main,
        'transcript': transcript_display,
        'title': recording_title_input,
        'transcribe_btn': transcribe_btn,
        'save_btn': save_recording_btn,
        'clear_btn': clear_recording_btn,
        'save_status': save_status,
        'id': recording_id_hidden
    }
