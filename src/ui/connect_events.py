"""Connect event handlers to UI components."""


def connect_recording_events(tab, handlers):
    """Connect recording tab events."""
    # Auto-transcribe when recording stops
    tab['audio'].stop_recording(
        fn=handlers['transcribe'],
        inputs=[tab['audio'], tab['lang'], tab['realtime']],
        outputs=[tab['transcript']],
        show_progress="full"
    )
    
    # Manual transcribe button (for uploaded files)
    tab['transcribe_btn'].click(
        fn=handlers['transcribe'],
        inputs=[tab['audio'], tab['lang'], tab['realtime']],
        outputs=[tab['transcript']],
        show_progress="full"
    )
    
    tab['save_btn'].click(
        fn=handlers['save_recording'],
        inputs=[tab['audio'], tab['title'], tab['lang'], tab['transcript']],
        outputs=[tab['save_status'], tab['id']]
    ).then(
        fn=handlers['refresh_recording_history'],
        outputs=[tab['recording_list']]
    )
    
    tab['clear_btn'].click(
        fn=lambda: (None, "", "", ""),
        outputs=[tab['audio'], tab['transcript'], tab['save_status'], tab['id']]
    )
    
    # History sidebar events
    tab['refresh_history_btn'].click(
        fn=handlers['refresh_recording_history'],
        inputs=[tab['history_filter'], tab['history_search']],
        outputs=[tab['recording_list']]
    )
    
    tab['history_filter'].change(
        fn=handlers['refresh_recording_history'],
        inputs=[tab['history_filter'], tab['history_search']],
        outputs=[tab['recording_list']]
    )
    
    tab['history_search'].change(
        fn=handlers['refresh_recording_history'],
        inputs=[tab['history_filter'], tab['history_search']],
        outputs=[tab['recording_list']]
    )


def connect_upload_events(tab, handlers):
    """Connect upload tab events."""
    tab['process_btn'].click(
        fn=handlers['process_upload'],
        inputs=[
            tab['file_type'],
            tab['audio_file'],
            tab['text_file'],
            tab['transcribe_lang'],
            tab['enable_diarization'],
            tab['meeting_type'],
            tab['output_lang']
        ],
        outputs=[
            tab['status'],
            tab['transcript'],
            tab['summary'],
            tab['topics'],
            tab['actions'],
            tab['decisions'],
            tab['participants']
        ],
        show_progress="full"
    )


def connect_chat_events(tab, handlers):
    """Connect chat tab events."""
    tab['send_btn'].click(
        fn=handlers['chat'],
        inputs=[tab['input'], tab['chatbot']],
        outputs=[tab['chatbot']]
    ).then(
        fn=lambda: "",
        outputs=[tab['input']]
    )
    
    tab['input'].submit(
        fn=handlers['chat'],
        inputs=[tab['input'], tab['chatbot']],
        outputs=[tab['chatbot']]
    ).then(
        fn=lambda: "",
        outputs=[tab['input']]
    )
    
    tab['clear_btn'].click(
        fn=lambda: [],
        outputs=[tab['chatbot']]
    )
    
    # Quick questions
    def send_q(q, h):
        return handlers['chat'](q, h)
    
    tab['quick_btns'][0].click(fn=lambda h: send_q("Tóm tắt cuộc họp này", h), inputs=[tab['chatbot']], outputs=[tab['chatbot']])
    tab['quick_btns'][1].click(fn=lambda h: send_q("Ai tham gia cuộc họp?", h), inputs=[tab['chatbot']], outputs=[tab['chatbot']])
    tab['quick_btns'][2].click(fn=lambda h: send_q("Action items là gì?", h), inputs=[tab['chatbot']], outputs=[tab['chatbot']])
    tab['quick_btns'][3].click(fn=lambda h: send_q("Những quyết định quan trọng nào được đưa ra?", h), inputs=[tab['chatbot']], outputs=[tab['chatbot']])
    tab['quick_btns'][4].click(fn=lambda h: send_q("Chủ đề chính của cuộc họp là gì?", h), inputs=[tab['chatbot']], outputs=[tab['chatbot']])


def connect_analysis_history_events(tab, handlers):
    """Connect analysis history tab events."""
    tab['refresh_btn'].click(
        fn=handlers['refresh_history'],
        outputs=[tab['dropdown'], tab['info']]
    )
    
    tab['load_btn'].click(
        fn=handlers['load_history'],
        inputs=[tab['dropdown']],
        outputs=[tab['info'], tab['summary'], tab['topics']]
    )


def connect_recording_history_events(tab, handlers):
    """Connect recording history tab events."""
    tab['refresh_btn'].click(
        fn=handlers['refresh_recordings'],
        outputs=[tab['dropdown'], tab['stats']]
    )
    
    tab['dropdown'].change(
        fn=handlers['load_recording_info'],
        inputs=[tab['dropdown']],
        outputs=[tab['info'], tab['notes'], tab['player']]
    )
    
    tab['delete_btn'].click(
        fn=handlers['delete_recording'],
        inputs=[tab['dropdown']],
        outputs=[tab['status'], tab['dropdown'], tab['stats']]
    )


def connect_search_export_events(tab, handlers):
    """Connect search & export tab events."""
    # Search stats
    tab['refresh_stats_btn'].click(
        fn=handlers['get_stats'],
        outputs=[tab['stats_display']]
    )
    
    # Search analyses (simplified - removed language filter)
    tab['search_btn'].click(
        fn=lambda q, t, n: handlers['search_meetings'](q, t, "Tất cả", n),
        inputs=[tab['search_query'], tab['meeting_type_filter'], tab['n_results']],
        outputs=[tab['search_status'], tab['search_results']]
    )
    
    # Export
    tab['export_txt_btn'].click(
        fn=handlers['export_txt'],
        outputs=[tab['export_file']]
    )
    
    tab['export_docx_btn'].click(
        fn=handlers['export_docx'],
        outputs=[tab['export_file']]
    )
