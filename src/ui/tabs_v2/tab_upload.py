"""Tab 3: Upload & Transcribe - Upload audio/text and analyze."""

import gradio as gr


def create_upload_tab():
    """Create Upload & Transcribe tab - Upload audio or text for analysis."""
    
    with gr.Tab("📤 Tải lên & Chuyển văn bản"):
        with gr.Row():
            # Left: Upload & Controls (1)
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Tải File Lên")
                
                # File type selector
                file_type = gr.Radio(
                    label="Loại file",
                    choices=[
                        ("🎵 Audio (WAV, MP3, M4A)", "audio"),
                        ("📄 Text (TXT, DOCX)", "text")
                    ],
                    value="audio",
                    info="Chọn loại file bạn muốn upload"
                )
                
                # Audio file input
                audio_file_input = gr.File(
                    label="Chọn file audio",
                    file_count="single",
                    file_types=[".wav", ".mp3", ".m4a", ".webm", ".ogg"],
                    visible=True
                )
                
                # Text file input
                text_file_input = gr.File(
                    label="Chọn file text",
                    file_count="single",
                    file_types=[".txt", ".docx"],
                    visible=False
                )
                
                # Audio transcription options (only for audio)
                with gr.Group(visible=True) as audio_options:
                    transcribe_lang = gr.Dropdown(
                        label="Ngôn ngữ audio",
                        choices=[
                            ("Tiếng Việt", "vi"),
                            ("English", "en"),
                            ("日本語", "ja"),
                            ("한국어", "ko"),
                            ("中文", "zh")
                        ],
                        value="vi"
                    )
                    
                    enable_diarization = gr.Checkbox(
                        label="🎤 Phân biệt người nói (Speaker Diarization)",
                        value=False,
                        info="Gán nhãn Guest-1, Guest-2,... cho từng người nói"
                    )
                
                gr.Markdown("---")
                gr.Markdown("### ⚙️ Cài Đặt Phân Tích")
                
                meeting_type = gr.Dropdown(
                    label="Loại cuộc họp",
                    choices=[
                        ("📋 Meeting - Cuộc họp thường", "meeting"),
                        ("🎓 Workshop - Đào tạo/Hội thảo", "workshop"),
                        ("💡 Brainstorming - Động não", "brainstorming")
                    ],
                    value="meeting",
                    info="Output sẽ khác nhau tùy loại"
                )
                
                output_lang = gr.Dropdown(
                    label="Ngôn ngữ output",
                    choices=[
                        ("Tiếng Việt", "vi"),
                        ("English", "en"),
                        ("日本語", "ja"),
                        ("한국어", "ko"),
                        ("中文", "zh")
                    ],
                    value="vi"
                )
                
                process_btn = gr.Button("🚀 Xử Lý & Phân Tích", variant="primary", size="lg")
                
                status_box = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=2,
                    show_label=False,
                    visible=False
                )
            
            # Right: Results (2)
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Kết Quả")
                
                with gr.Tabs() as result_tabs:
                    # Tab 1: Transcript (for audio) or Original Text
                    with gr.Tab("📝 Transcript") as transcript_tab:
                        transcript_output = gr.Textbox(
                            lines=20,
                            interactive=False,
                            show_label=False,
                            placeholder="Transcript sẽ hiển thị ở đây sau khi xử lý audio..."
                        )
                    
                    # Tab 2: Analysis Results
                    with gr.Tab("📊 Kết Quả Phân Tích") as analysis_tab:
                        with gr.Tabs():
                            with gr.Tab("📝 Tóm tắt"):
                                summary_output = gr.Textbox(
                                    lines=15,
                                    interactive=False,
                                    show_label=False,
                                    placeholder="Tóm tắt cuộc họp..."
                                )
                            
                            with gr.Tab("🎯 Chủ đề chính"):
                                topics_output = gr.Markdown("_Chưa có dữ liệu_")
                            
                            with gr.Tab("✅ Action Items"):
                                actions_output = gr.Markdown("_Chưa có dữ liệu_")
                            
                            with gr.Tab("🎯 Quyết định"):
                                decisions_output = gr.Markdown("_Chưa có dữ liệu_")
                            
                            with gr.Tab("👥 Người tham gia"):
                                participants_output = gr.Markdown("_Chưa có dữ liệu_")
    
    # Toggle file inputs based on file type
    def update_file_inputs(file_type_value):
        if file_type_value == "audio":
            return (
                gr.update(visible=True),   # audio_file_input
                gr.update(visible=False),  # text_file_input
                gr.update(visible=True)    # audio_options
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )
    
    file_type.change(
        fn=update_file_inputs,
        inputs=[file_type],
        outputs=[audio_file_input, text_file_input, audio_options]
    )
    
    return {
        'file_type': file_type,
        'audio_file': audio_file_input,
        'text_file': text_file_input,
        'transcribe_lang': transcribe_lang,
        'enable_diarization': enable_diarization,
        'meeting_type': meeting_type,
        'output_lang': output_lang,
        'process_btn': process_btn,
        'status': status_box,
        'transcript': transcript_output,
        'summary': summary_output,
        'topics': topics_output,
        'actions': actions_output,
        'decisions': decisions_output,
        'participants': participants_output
    }
