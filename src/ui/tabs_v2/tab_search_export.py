"""Tab 6: Search & Export - Semantic search and export results."""

import gradio as gr


def create_search_export_tab():
    """Create Search & Export tab - Clear purpose."""
    
    with gr.Tab("🔍 Tìm Kiếm & Xuất"):
        with gr.Tabs():
            # Sub-tab 1: Semantic Search
            with gr.Tab("🔍 Tìm Kiếm Thông Minh"):
                gr.Markdown("""
                ### 🎯 Tìm kiếm các cuộc họp đã phân tích
                
                Tìm kiếm dựa trên **nội dung** (không chỉ tên file). 
                VD: Tìm "React Hooks" sẽ tìm tất cả cuộc họp có nói về React Hooks.
                """)
                
                with gr.Row():
                    # Left: Search Controls
                    with gr.Column(scale=1):
                        search_query = gr.Textbox(
                            label="🔍 Nội dung cần tìm",
                            placeholder="VD: React Hooks, ngân sách Q4, kế hoạch marketing...",
                            lines=2
                        )
                        
                        with gr.Row():
                            meeting_type_filter = gr.Dropdown(
                                label="Loại cuộc họp",
                                choices=["Tất cả", "meeting", "workshop", "brainstorming"],
                                value="Tất cả",
                                scale=1
                            )
                            n_results = gr.Slider(
                                label="Số kết quả",
                                minimum=1,
                                maximum=10,
                                value=5,
                                step=1
                            )
                        
                        search_btn = gr.Button("🔍 Tìm kiếm", variant="primary")
                        search_status = gr.Textbox(show_label=False, interactive=False, lines=1)
                    
                    # Right: Search Results
                    with gr.Column(scale=2):
                        gr.Markdown("### 📋 Kết Quả Tìm Kiếm")
                        search_results = gr.Markdown("""
                        _Nhập nội dung cần tìm và nhấn "Tìm kiếm"_
                        
                        **Cách hoạt động:**
                        - Tìm kiếm dựa trên **ý nghĩa** nội dung (AI semantic search)
                        - Không cần nhớ chính xác tên file
                        - Tìm được cả các cuộc họp liên quan
                        """)
                
                # Database stats
                with gr.Accordion("📊 Thống Kê Database", open=False):
                    with gr.Row():
                        stats_display = gr.Markdown("_Đang tải thống kê..._")
                        refresh_stats_btn = gr.Button("🔄 Refresh", scale=1)
            
            # Sub-tab 2: Export Current Analysis
            with gr.Tab("📄 Xuất File"):
                gr.Markdown("""
                ### 📥 Xuất kết quả phân tích hiện tại
                
                **Lưu ý:** Cần phân tích transcript ở tab "Upload & Phân Tích" trước khi xuất.
                """)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("""
                        #### 📄 Xuất TXT
                        
                        **Ưu điểm:**
                        - Đơn giản, dễ đọc
                        - Mở được trên mọi thiết bị
                        - Dung lượng nhỏ
                        - Phù hợp gửi email nhanh
                        """)
                        export_txt_btn = gr.Button("📄 Xuất TXT", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.Markdown("""
                        #### 📝 Xuất DOCX (Word)
                        
                        **Ưu điểm:**
                        - Format chuyên nghiệp
                        - Có thể chỉnh sửa trong Word
                        - Phù hợp làm báo cáo
                        - Có định dạng đẹp (heading, bullet)
                        """)
                        export_docx_btn = gr.Button("📝 Xuất DOCX", variant="primary", size="lg")
                
                export_file = gr.File(label="File đã xuất", show_label=False)
                
                gr.Markdown("""
                ---
                **📌 File sẽ bao gồm:**
                - Tóm tắt cuộc họp
                - Chủ đề chính
                - Action items (công việc cần làm)
                - Quyết định quan trọng
                
                **📁 Tên file:** `meeting_analysis_YYYYMMDD_HHMMSS.txt/docx`
                """)
    
    return {
        'stats_display': stats_display,
        'refresh_stats_btn': refresh_stats_btn,
        'search_query': search_query,
        'meeting_type_filter': meeting_type_filter,
        'language_filter': None,  # Removed for simplicity
        'n_results': n_results,
        'search_btn': search_btn,
        'search_status': search_status,
        'search_results': search_results,
        'search_recording_query': None,  # Removed - use tab 5 instead
        'search_recording_btn': None,
        'search_recording_results': None,
        'export_txt_btn': export_txt_btn,
        'export_docx_btn': export_docx_btn,
        'export_file': export_file
    }
