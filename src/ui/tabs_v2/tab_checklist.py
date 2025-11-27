"""Tab 7: Checklist - Manage action items and tasks from meetings."""

import gradio as gr


def create_checklist_tab():
    """Create Checklist tab - Clean & Simple."""
    
    with gr.Tab("✅ Checklist"):
        with gr.Row():
            # Left: Task List
            with gr.Column(scale=2):
                gr.Markdown("### 📋 Danh Sách Công Việc")
                
                # Filter and actions
                with gr.Row():
                    filter_status = gr.Dropdown(
                        label="",
                        choices=[
                            ("📋 Tất cả", "all"),
                            ("⏳ Chưa xong", "pending"),
                            ("✅ Đã xong", "completed")
                        ],
                        value="all",
                        scale=2,
                        show_label=False
                    )
                    refresh_checklist_btn = gr.Button("🔄", scale=1)
                    import_btn = gr.Button("📥 Import", variant="secondary", scale=1)
                
                # Task table - editable
                checklist_display = gr.Dataframe(
                    headers=["ID", "Công việc", "Người làm", "Deadline", "Status", "Nguồn"],
                    datatype=["str", "str", "str", "str", "str", "str"],
                    interactive=True,  # Allow editing
                    wrap=True,
                    row_count=12,
                    show_label=False,
                    col_count=(6, "fixed")
                )
                
                import_status = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    lines=1
                )
            
            # Right: Add Task & Stats
            with gr.Column(scale=1):
                # Stats
                with gr.Accordion("📊 Thống Kê", open=True):
                    stats_display = gr.Markdown("""
                    - **Tổng:** 0
                    - **Hoàn thành:** 0 ✅
                    - **Chưa xong:** 0 ⏳
                    - **Tỷ lệ:** 0%
                    """)
                
                # Add new task
                gr.Markdown("### ➕ Thêm Task")
                
                new_task_input = gr.Textbox(
                    label="Công việc",
                    placeholder="Mô tả công việc...",
                    lines=2
                )
                
                with gr.Row():
                    new_assignee_input = gr.Textbox(
                        label="Người làm",
                        placeholder="Tên",
                        scale=1
                    )
                    new_deadline_input = gr.Textbox(
                        label="Deadline",
                        placeholder="30/11",
                        scale=1
                    )
                
                new_priority = gr.Dropdown(
                    label="Ưu tiên",
                    choices=[
                        ("🔴 Cao", "high"),
                        ("🟡 TB", "medium"),
                        ("🟢 Thấp", "low")
                    ],
                    value="medium"
                )
                
                add_task_btn = gr.Button("➕ Thêm Task", variant="primary")
                
                gr.Markdown("""
                ---
                **💡 Hướng dẫn:**
                - Click vào ô Status để edit
                - Đổi thành "✅" hoặc "⏳"
                - Import từ phân tích để tự động tạo tasks
                """)
    
    return {
        'filter': filter_status,
        'refresh_btn': refresh_checklist_btn,
        'checklist': checklist_display,
        'new_task': new_task_input,
        'new_assignee': new_assignee_input,
        'new_deadline': new_deadline_input,
        'new_priority': new_priority,
        'add_btn': add_task_btn,
        'stats': stats_display,
        'import_btn': import_btn,
        'import_status': import_status
    }
