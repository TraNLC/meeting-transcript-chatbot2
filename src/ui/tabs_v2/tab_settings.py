"""Tab Settings: System management, backup, cleanup, cache."""

import gradio as gr


def create_settings_tab():
    """Create Settings tab for system management."""
    
    with gr.Tab("⚙️ Cài Đặt"):
        gr.Markdown("## 🔧 Quản Lý Hệ Thống")
        
        with gr.Tabs():
            # Backup & Restore
            with gr.Tab("💾 Backup & Restore"):
                gr.Markdown("### Sao lưu và khôi phục dữ liệu")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### Tạo Backup")
                        backup_name = gr.Textbox(
                            label="Tên backup (tùy chọn)",
                            placeholder="Để trống để tự động đặt tên"
                        )
                        include_recordings = gr.Checkbox(
                            label="Bao gồm file ghi âm",
                            value=False,
                            info="Tăng kích thước backup đáng kể"
                        )
                        create_backup_btn = gr.Button("💾 Tạo Backup", variant="primary")
                        backup_status = gr.Textbox(label="Trạng thái", interactive=False)
                    
                    with gr.Column():
                        gr.Markdown("#### Danh Sách Backup")
                        backup_list = gr.Dataframe(
                            headers=["Tên", "Ngày tạo", "Kích thước (MB)", "Có ghi âm"],
                            label="",
                            interactive=False
                        )
                        refresh_backup_btn = gr.Button("🔄 Làm mới")
                        
                        with gr.Row():
                            selected_backup = gr.Dropdown(
                                label="Chọn backup để khôi phục",
                                choices=[],
                                interactive=True
                            )
                            restore_btn = gr.Button("♻️ Khôi phục", variant="secondary")
                            delete_backup_btn = gr.Button("🗑️ Xóa", variant="stop")
            
            # Data Cleanup
            with gr.Tab("🧹 Dọn Dẹp"):
                gr.Markdown("### Dọn dẹp dữ liệu cũ để tiết kiệm dung lượng")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### Thống Kê Dung Lượng")
                        storage_stats = gr.Markdown("_Đang tải..._")
                        refresh_stats_btn = gr.Button("🔄 Làm mới thống kê")
                    
                    with gr.Column():
                        gr.Markdown("#### Dọn Dẹp Tự Động")
                        
                        recordings_days = gr.Slider(
                            label="Xóa ghi âm cũ hơn (ngày)",
                            minimum=30,
                            maximum=365,
                            value=90,
                            step=30
                        )
                        cleanup_recordings_btn = gr.Button("🗑️ Xóa ghi âm cũ", variant="secondary")
                        
                        history_days = gr.Slider(
                            label="Xóa lịch sử cũ hơn (ngày)",
                            minimum=90,
                            maximum=730,
                            value=180,
                            step=30
                        )
                        cleanup_history_btn = gr.Button("🗑️ Xóa lịch sử cũ", variant="secondary")
                        
                        cleanup_status = gr.Textbox(label="Trạng thái", interactive=False)
            
            # Cache Management
            with gr.Tab("⚡ Cache"):
                gr.Markdown("### Quản lý bộ nhớ đệm")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### Thống Kê Cache")
                        cache_stats = gr.Markdown("_Đang tải..._")
                        refresh_cache_btn = gr.Button("🔄 Làm mới")
                    
                    with gr.Column():
                        gr.Markdown("#### Quản Lý")
                        clear_llm_cache_btn = gr.Button("🗑️ Xóa LLM Cache", variant="secondary")
                        clear_all_cache_btn = gr.Button("🗑️ Xóa Tất Cả Cache", variant="stop")
                        cache_status = gr.Textbox(label="Trạng thái", interactive=False)
            
            # Logs
            with gr.Tab("📋 Logs"):
                gr.Markdown("### Xem log hệ thống")
                
                log_lines = gr.Slider(
                    label="Số dòng hiển thị",
                    minimum=50,
                    maximum=500,
                    value=100,
                    step=50
                )
                refresh_logs_btn = gr.Button("🔄 Làm mới logs")
                logs_display = gr.Textbox(
                    label="",
                    lines=20,
                    interactive=False,
                    show_label=False
                )
    
    return {
        # Backup
        'backup_name': backup_name,
        'include_recordings': include_recordings,
        'create_backup_btn': create_backup_btn,
        'backup_status': backup_status,
        'backup_list': backup_list,
        'refresh_backup_btn': refresh_backup_btn,
        'selected_backup': selected_backup,
        'restore_btn': restore_btn,
        'delete_backup_btn': delete_backup_btn,
        
        # Cleanup
        'storage_stats': storage_stats,
        'refresh_stats_btn': refresh_stats_btn,
        'recordings_days': recordings_days,
        'cleanup_recordings_btn': cleanup_recordings_btn,
        'history_days': history_days,
        'cleanup_history_btn': cleanup_history_btn,
        'cleanup_status': cleanup_status,
        
        # Cache
        'cache_stats': cache_stats,
        'refresh_cache_btn': refresh_cache_btn,
        'clear_llm_cache_btn': clear_llm_cache_btn,
        'clear_all_cache_btn': clear_all_cache_btn,
        'cache_status': cache_status,
        
        # Logs
        'log_lines': log_lines,
        'refresh_logs_btn': refresh_logs_btn,
        'logs_display': logs_display
    }
