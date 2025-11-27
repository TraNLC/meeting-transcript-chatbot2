"""Tab 4: Analysis History - Manage saved analyses."""

import gradio as gr


def create_analysis_history_tab():
    """Create Analysis History tab - Smart & Compact Layout."""
    
    with gr.Tab("📊 Lịch Sử Phân Tích"):
        with gr.Row():
            # Left: History List & Actions
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Danh Sách")
                
                with gr.Row():
                    history_dropdown = gr.Dropdown(
                        label="Chọn phân tích",
                        choices=[],
                        interactive=True,
                        scale=3,
                        show_label=False
                    )
                    refresh_history_btn = gr.Button("🔄", scale=1)
                
                history_info = gr.Markdown(
                    "_Chọn một phân tích để xem chi tiết_",
                    elem_classes="info-box"
                )
                
                # Action buttons
                with gr.Row():
                    load_analysis_btn = gr.Button("📂 Tải vào", variant="primary", scale=2)
                    delete_analysis_btn = gr.Button("🗑️", variant="stop", scale=1)
                
                # Quick stats
                gr.Markdown("---")
                stats_display = gr.Markdown("""
                **📊 Thống kê:**
                - Tổng: 0 phân tích
                - Hôm nay: 0
                """)
            
            # Right: Preview Content
            with gr.Column(scale=2):
                gr.Markdown("### 👁️ Xem Trước")
                
                # Tabs for different sections
                with gr.Tabs():
                    with gr.Tab("📝 Tóm tắt"):
                        summary_history = gr.Textbox(
                            lines=10,
                            interactive=False,
                            show_label=False,
                            placeholder="Tóm tắt sẽ hiển thị ở đây..."
                        )
                    
                    with gr.Tab("🎯 Chủ đề"):
                        topics_history = gr.Markdown("_Chưa có dữ liệu_")
                    
                    with gr.Tab("✅ Actions"):
                        actions_history = gr.Markdown("_Chưa có dữ liệu_")
                    
                    with gr.Tab("🎯 Quyết định"):
                        decisions_history = gr.Markdown("_Chưa có dữ liệu_")
    
    return {
        'dropdown': history_dropdown,
        'refresh_btn': refresh_history_btn,
        'info': history_info,
        'summary': summary_history,
        'topics': topics_history,
        'actions': actions_history,
        'decisions': decisions_history,
        'load_btn': load_analysis_btn,
        'delete_btn': delete_analysis_btn,
        'stats': stats_display
    }
