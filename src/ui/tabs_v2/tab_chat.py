"""Tab 3: Chat with AI - Interactive Q&A about meetings."""

import gradio as gr


def create_chat_tab():
    """Create Chat with AI tab."""
    
    with gr.Tab("💬 Chat với AI"):
        gr.Markdown("### 🤖 Hỏi đáp thông minh về cuộc họp")
        
        with gr.Row():
            with gr.Column(scale=3):
                chatbot_display = gr.Chatbot(
                    height=500,
                    label="Cuộc trò chuyện",
                    type="messages"
                )
                
                with gr.Row():
                    chat_input = gr.Textbox(
                        placeholder="Nhập câu hỏi của bạn...",
                        show_label=False,
                        scale=4
                    )
                
                with gr.Row():
                    send_btn = gr.Button("📤 Gửi", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ Xóa lịch sử", variant="primary", scale=1)
            
            with gr.Column(scale=1):
                gr.Markdown("### 💡 Câu Hỏi Gợi Ý")
                
                q1 = gr.Button("📋 Tóm tắt cuộc họp", size="sm")
                q2 = gr.Button("👥 Ai tham gia?", size="sm")
                q3 = gr.Button("✅ Action items là gì?", size="sm")
                q4 = gr.Button("🎯 Quyết định quan trọng?", size="sm")
                q5 = gr.Button("📊 Chủ đề chính?", size="sm")
                
                gr.Markdown("""
                ---
                **💬 Bạn có thể hỏi:**
                - Tóm tắt cuộc họp
                - Ai tham gia meeting?
                - Action items là gì?
                - Quyết định nào được đưa ra?
                - Chủ đề chính là gì?
                """)
    
    return {
        'chatbot': chatbot_display,
        'input': chat_input,
        'send_btn': send_btn,
        'clear_btn': clear_btn,
        'quick_btns': [q1, q2, q3, q4, q5]
    }
