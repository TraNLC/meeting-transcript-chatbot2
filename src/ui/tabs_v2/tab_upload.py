"""Tab 2: Upload & Analysis - File upload and meeting analysis."""

import gradio as gr


def create_upload_tab():
    """Create Upload & Analysis tab - Simple & Clean Layout."""
    
    with gr.Tab("📤 Upload & Phân Tích"):
        with gr.Row():
            # Left: Upload & Controls
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
                        ("Meeting", "meeting"),
                        ("Workshop", "workshop"),
                        ("Brainstorming", "brainstorming")
                    ],
                    value="meeting"
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
                    label="Trạng thái",
                    interactive=False,
                    lines=2,
                    show_label=False
                )
                

            
            # Right: Results
            with gr.Column(scale=2):
                gr.Markdown("### � Kếmt Quả")
                
                with gr.Tabs():
                    with gr.Tab("📝 Tóm tắt"):
                        summary_output = gr.Textbox(
                            lines=12,
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
