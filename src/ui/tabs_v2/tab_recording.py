"""Tab 1: Recording - Audio recording and transcription."""

import gradio as gr
from datetime import datetime


def create_recording_tab():
    """Create Recording tab with smart UI and popup workflow."""
    
    with gr.Tab("🎙️ Ghi Âm"):
        with gr.Row():
            # Left Sidebar: Recording History (1) - Simple, no search
            with gr.Column(scale=1):
                gr.Markdown("### 📚 Lịch Sử Ghi Âm")
                
                # Simple filter tabs
                history_filter = gr.Radio(
                    choices=["Tất cả", "Hôm nay", "Tuần này", "Tháng này"],
                    value="Tất cả",
                    show_label=False,
                    container=False
                )
                
                # Recording list (grouped by date) - Clean design
                recording_list = gr.HTML(
                    """
                    <div style="max-height: 600px; overflow-y: auto; padding: 5px;">
                        <div style="margin-bottom: 20px;">
                            <div style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 8px;">Hôm nay</div>
                            <div style="padding: 10px; background: white; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 6px; cursor: pointer; transition: all 0.2s;"
                                 onmouseover="this.style.borderColor='#2563eb'; this.style.boxShadow='0 2px 8px rgba(37,99,235,0.1)'"
                                 onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none'">
                                <div style="font-size: 14px; font-weight: 500; color: #111827;">Ghi âm 6/12/2025</div>
                                <div style="font-size: 12px; color: #6b7280; margin-top: 2px;">2:30 phút</div>
                            </div>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <div style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 8px;">Hôm qua</div>
                            <div style="padding: 10px; background: white; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 6px; cursor: pointer; transition: all 0.2s;"
                                 onmouseover="this.style.borderColor='#2563eb'; this.style.boxShadow='0 2px 8px rgba(37,99,235,0.1)'"
                                 onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none'">
                                <div style="font-size: 14px; font-weight: 500; color: #111827;">Ghi âm 5/12/2025</div>
                                <div style="font-size: 12px; color: #6b7280; margin-top: 2px;">1:45 phút</div>
                            </div>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <div style="font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 8px;">30 Ngày trước</div>
                            <div style="padding: 10px; background: white; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 6px; cursor: pointer; transition: all 0.2s;"
                                 onmouseover="this.style.borderColor='#2563eb'; this.style.boxShadow='0 2px 8px rgba(37,99,235,0.1)'"
                                 onmouseout="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none'">
                                <div style="font-size: 14px; font-weight: 500; color: #111827;">Ghi âm 25/11/2025</div>
                                <div style="font-size: 12px; color: #6b7280; margin-top: 2px;">3:15 phút</div>
                            </div>
                        </div>
                    </div>
                    """
                )
                
                with gr.Row():
                    refresh_history_btn = gr.Button("🔄 Làm mới", scale=1, size="sm")
            
            # Middle: Main Recording Area (2)
            with gr.Column(scale=2):
                # Big "Ghi âm ngay lập tức" button in center
                gr.HTML("""
                <div style="display: flex; justify-content: center; align-items: center; min-height: 400px;">
                    <div style="text-align: center;">
                        <button id="instant-record-btn" style="
                            width: 180px;
                            height: 180px;
                            border-radius: 50%;
                            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                            border: none;
                            cursor: pointer;
                            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3);
                            transition: all 0.3s;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            color: white;
                        "
                        onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 15px 40px rgba(37, 99, 235, 0.4)'"
                        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 10px 30px rgba(37, 99, 235, 0.3)'"
                        onclick="showRecordingPopup()">
                            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                                <line x1="12" y1="19" x2="12" y2="23"></line>
                                <line x1="8" y1="23" x2="16" y2="23"></line>
                            </svg>
                            <div style="margin-top: 15px; font-size: 16px; font-weight: 600;">Ghi âm ngay lập tức</div>
                        </button>
                        <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">Nhấn để bắt đầu ghi âm</p>
                    </div>
                </div>
                """)
                
                # Hidden components for backend
                recording_title_input = gr.Textbox(visible=False)
                recording_lang_input = gr.Dropdown(visible=False)
                audio_source = gr.Radio(visible=False)
                realtime_mode = gr.Checkbox(visible=False, value=True)
                screen_audio_info = gr.Markdown(visible=False)
                screen_audio_recorder = gr.HTML(visible=False)
                audio_recorder_main = gr.Audio(visible=False)
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
                
                # Audio source selection
                audio_source = gr.Radio(
                    label="Nguồn âm thanh",
                    choices=[
                        ("🎤 Microphone", "microphone"),
                        ("🖥️ Tab/Màn hình (Screen Audio)", "screen"),
                        ("📁 Upload File", "upload")
                    ],
                    value="microphone",
                    info="Chọn nguồn để ghi âm"
                )
                
                realtime_mode = gr.Checkbox(
                    label="🎯 Chế độ Realtime (hiển thị từng đoạn)",
                    value=True,
                    info="Bật để xem transcript xuất hiện từng đoạn như realtime"
                )
                
                # Screen audio instructions
                screen_audio_info = gr.Markdown(
                    """
                    ⚠️ **Hướng dẫn ghi âm từ Tab/Màn hình:**
                    1. Nhấn nút ghi âm
                    2. Chọn tab "**Thẻ trình duyệt Chrome**"
                    3. Chọn tab có audio đang phát
                    4. ✅ **BẬT checkbox "Chia sẻ cả âm thanh trên thẻ"**
                    5. Nhấn "Chia sẻ"
                    
                    💡 Dùng để ghi âm từ: YouTube, Google Meet, Teams, Zoom, etc.
                    """,
                    visible=False
                )
                
                # Screen audio recorder (custom HTML)
                screen_audio_recorder = gr.HTML(
                    """
                    <div id="screen-audio-recorder" style="display:none; padding: 10px; border: 2px dashed #2563eb; border-radius: 8px; margin: 10px 0;">
                        <button id="start-screen-record" style="background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px;">
                            🖥️ Bắt đầu ghi âm màn hình
                        </button>
                        <button id="stop-screen-record" style="background: #dc2626; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; display: none; margin-left: 10px;">
                            ⏹️ Dừng ghi âm
                        </button>
                        <div id="screen-record-status" style="margin-top: 10px; font-size: 13px; color: #666;"></div>
                    </div>
                    
                    <script>
                    (function() {
                        let mediaRecorder = null;
                        let audioChunks = [];
                        let stream = null;
                        
                        const startBtn = document.getElementById('start-screen-record');
                        const stopBtn = document.getElementById('stop-screen-record');
                        const status = document.getElementById('screen-record-status');
                        
                        startBtn.onclick = async () => {
                            try {
                                stream = await navigator.mediaDevices.getDisplayMedia({
                                    video: true,
                                    audio: {
                                        echoCancellation: true,
                                        noiseSuppression: true,
                                        sampleRate: 44100
                                    }
                                });
                                
                                const audioTracks = stream.getAudioTracks();
                                if (audioTracks.length === 0) {
                                    alert('⚠️ Không có audio!\\n\\nHãy đảm bảo:\\n1. Chọn tab có audio\\n2. BẬT checkbox "Chia sẻ cả âm thanh trên thẻ"');
                                    stream.getTracks().forEach(t => t.stop());
                                    return;
                                }
                                
                                const audioStream = new MediaStream(audioTracks);
                                mediaRecorder = new MediaRecorder(audioStream);
                                audioChunks = [];
                                
                                mediaRecorder.ondataavailable = (e) => {
                                    if (e.data.size > 0) audioChunks.push(e.data);
                                };
                                
                                mediaRecorder.onstop = () => {
                                    const blob = new Blob(audioChunks, { type: 'audio/webm' });
                                    const url = URL.createObjectURL(blob);
                                    
                                    // Create download link
                                    const a = document.createElement('a');
                                    a.href = url;
                                    a.download = 'screen-audio-' + Date.now() + '.webm';
                                    a.click();
                                    
                                    status.innerHTML = '✅ Đã lưu file! Upload file vừa tải về để transcribe.';
                                };
                                
                                mediaRecorder.start(1000);
                                stream.getVideoTracks().forEach(t => t.stop());
                                
                                startBtn.style.display = 'none';
                                stopBtn.style.display = 'inline-block';
                                status.innerHTML = '🔴 Đang ghi âm...';
                                
                            } catch (error) {
                                console.error(error);
                                if (error.name === 'NotAllowedError') {
                                    alert('Bạn đã từ chối chia sẻ màn hình.');
                                } else {
                                    alert('Lỗi: ' + error.message);
                                }
                            }
                        };
                        
                        stopBtn.onclick = () => {
                            if (mediaRecorder && mediaRecorder.state === 'recording') {
                                mediaRecorder.stop();
                                if (stream) stream.getTracks().forEach(t => t.stop());
                                
                                startBtn.style.display = 'inline-block';
                                stopBtn.style.display = 'none';
                            }
                        };
                    })();
                    </script>
                    """,
                    visible=False
                )
                
                audio_recorder_main = gr.Audio(
                    sources=["microphone", "upload"],
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
            
            # Right: Transcript & Player (2)
            with gr.Column(scale=2):
                # Recording info header
                recording_info_header = gr.Markdown(
                    "### 📝 Transcript",
                    visible=True
                )
                
                # Audio player for selected recording
                selected_audio_player = gr.Audio(
                    label="",
                    show_label=False,
                    interactive=False,
                    visible=False
                )
                
                # Action buttons for selected recording
                with gr.Row(visible=False) as selected_actions:
                    translate_btn = gr.Button("🌐 Dịch", size="sm")
                    export_btn = gr.Button("📥 Export", size="sm")
                    share_btn = gr.Button("🔗 Chia sẻ", size="sm")
                
                transcript_display = gr.Textbox(
                    label="",
                    interactive=False,
                    lines=20,
                    show_label=False,
                    placeholder="Chọn bản ghi âm từ lịch sử hoặc ghi âm mới..."
                )
    
    # Show/hide components based on audio source
    def update_audio_source(source):
        if source == "screen":
            return (
                gr.update(visible=True),  # screen_audio_info
                gr.update(visible=True),  # screen_audio_recorder
                gr.update(visible=False)  # audio_recorder_main
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True)
            )
    
    audio_source.change(
        fn=update_audio_source,
        inputs=[audio_source],
        outputs=[screen_audio_info, screen_audio_recorder, audio_recorder_main]
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
        'id': recording_id_hidden,
        'realtime': realtime_mode,
        'audio_source': audio_source,
        'screen_info': screen_audio_info,
        'screen_recorder': screen_audio_recorder,
        'history_search': history_search,
        'history_filter': history_filter,
        'recording_list': recording_list,
        'refresh_history_btn': refresh_history_btn,
        'delete_selected_btn': delete_selected_btn,
        'selected_audio_player': selected_audio_player,
        'selected_actions': selected_actions,
        'recording_info_header': recording_info_header
    }
