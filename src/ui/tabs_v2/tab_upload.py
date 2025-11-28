"""Tab 2: Upload & Analysis - File upload and meeting analysis."""

import gradio as gr


def create_upload_tab():
    """Create Upload & Analysis tab - Clean Layout 1:2."""
    
    with gr.Tab("📤 Upload & Phân Tích"):
        with gr.Row():
            # Left: Upload & Controls (1)
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Upload File")
                
                file_input = gr.File(
                    label="Chọn file transcript",
                    file_count="single",
                    file_types=[".txt", ".docx"]
                )
                
                meeting_type = gr.Dropdown(
                    label="Loại cuộc họp",
                    choices=[
                        ("📋 Meeting - Cuộc họp thường", "meeting"),
                        ("🎓 Workshop - Đào tạo/Hội thảo", "workshop"),
                        ("💡 Brainstorming - Động não", "brainstorming")
                    ],
                    value="meeting",
                    info="Output sẽ khác nhau tùy loại cuộc họp"
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
                
                process_btn = gr.Button("🚀 Phân Tích", variant="primary", size="lg")
                
                status_box = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=1,
                    show_label=False,
                    visible=False  # Ẩn khi chưa có status
                )
            
            # Right: Results (2)
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Kết Quả Phân Tích")
                
                with gr.Tabs():
                    with gr.Tab("📝 Tóm tắt"):
                        summary_output = gr.Textbox(
                            lines=15,
                            interactive=False,
                            show_label=False,
                            placeholder="Tóm tắt sẽ hiển thị ở đây..."
                        )
                    
                    with gr.Tab("🎯 Chủ đề"):
                        topics_output = gr.Markdown("_Chưa có dữ liệu_")
                    
                    with gr.Tab("✅ Actions"):
                        actions_output = gr.Markdown("_Chưa có dữ liệu_")
                    
                    with gr.Tab("🎯 Quyết định"):
                        decisions_output = gr.Markdown("_Chưa có dữ liệu_")
    
    return {
        'file': file_input,
        'meeting_type': meeting_type,
        'output_lang': output_lang,
        'process_btn': process_btn,
        'status': status_box,
        'summary': summary_output,
        'topics': topics_output,
        'actions': actions_output,
        'decisions': decisions_output
    }
