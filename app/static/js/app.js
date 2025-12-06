// Meeting Analyzer Pro - Main JavaScript

let currentRecordingConfig = {};
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let timerInterval = null;
let socket = null;
let isRealtimeTranscription = false;

// ============================================================================
// Tab Switching - Simple and Reliable
// ============================================================================

function switchTab(category) {
    console.log('🔄 Switching to tab:', category);

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-category="${category}"]`)?.classList.add('active');

    const views = ['initialView', 'recordingView', 'uploadView', 'chatView', 'historyView', 'resultView'];
    views.forEach(viewId => {
        const el = document.getElementById(viewId);
        if (el) el.style.display = 'none';
    });

    // Show/hide history lists (Compact Sidebar)
    const recordingList = document.getElementById('recordingList');


    if (recordingList) recordingList.style.display = 'none';


    // Show appropriate view and list
    switch (category) {
        case 'recording':
            document.getElementById('initialView').style.display = 'block';
            if (recordingList) recordingList.style.display = 'block';
            refreshHistory();
            console.log('✅ Showing: Recording view');
            break;

        case 'upload':
            document.getElementById('uploadView').style.display = 'block';
            console.log('✅ Showing: Upload view');
            break;





        case 'chat':
            document.getElementById('chatView').style.display = 'block';
            console.log('✅ Showing: Chat view');
            break;

        case 'history':
            document.getElementById('historyView').style.display = 'block';
            loadHistoryView();
            console.log('✅ Showing: History view');
            break;
    }
}

// ============================================================================
// Initialize
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Socket.IO
    initializeSocket();

    // Load recording history (default view)
    refreshHistory();

    // Setup filter tabs
    setupFilterTabs();

    // Setup realtime mode toggle
    setupRealtimeToggle();

    // Initialize file type toggle for upload view
    initializeFileTypeToggle();
});

// ============================================================================
// WebSocket Setup
// ============================================================================

function initializeSocket() {
    socket = io();

    socket.on('connected', (data) => {
        console.log('WebSocket connected:', data);
    });

    socket.on('transcript_update', (data) => {
        // Update transcript in realtime
        // Pass the whole data object to handle segments or text
        updateTranscript(data);
    });

    socket.on('transcript_final', (data) => {
        // Final transcript received
        console.log('Final transcript:', data.text);
        handleFinalTranscript(data.text);
    });

    socket.on('error', (data) => {
        console.error('WebSocket error:', data.message);
        updateTranscript('❌ Lỗi: ' + data.message);
    });
}

// ============================================================================
// Recording History
// ============================================================================

function refreshHistory() {
    const category = document.querySelector('.nav-link.active[data-category]')?.dataset.category || 'recording';

    fetch(`/api/recording/history?filter=Tất cả&category=${category}`)
        .then(res => res.json())
        .then(data => {
            renderHistoryList(data.recordings || []);
        })
        .catch(err => {
            console.error('Error loading history:', err);
            document.getElementById('recordingList').innerHTML = `
                <div class="alert alert-danger small">
                    Lỗi tải lịch sử: ${err.message}
                </div>
            `;
        });
}

function renderHistoryList(recordings) {
    if (!recordings || recordings.length === 0) {
        document.getElementById('recordingList').innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                <p class="mt-2 small">Chưa có bản ghi nào</p>
            </div>
        `;
        return;
    }

    // Group by date
    const grouped = groupRecordingsByDate(recordings);

    let html = '';
    for (const [dateLabel, items] of Object.entries(grouped)) {
        html += `
            <div class="mb-3">
                <div class="text-muted small fw-bold mb-2">${dateLabel}</div>
        `;

        items.forEach(rec => {
            const duration = rec.duration || '0:00';
            html += `
                <div class="recording-item compact-item" onclick="loadRecording('${rec.id}')" title="${rec.title}">
                    <div class="item-title">${rec.title}</div>
                    <div class="item-meta">
                        <i class="bi bi-clock"></i> ${duration}
                    </div>
                </div>
            `;
        });

        html += `</div>`;
    }

    document.getElementById('recordingList').innerHTML = html;
}

function groupRecordingsByDate(recordings) {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const groups = {
        'Hôm nay': [],
        'Hôm qua': [],
        '30 Ngày trước': []
    };

    const monthGroups = {};

    recordings.forEach(rec => {
        const recDate = new Date(rec.timestamp);
        const recDateOnly = new Date(recDate.getFullYear(), recDate.getMonth(), recDate.getDate());

        if (recDateOnly.getTime() === today.getTime()) {
            groups['Hôm nay'].push(rec);
        } else if (recDateOnly.getTime() === yesterday.getTime()) {
            groups['Hôm qua'].push(rec);
        } else if (recDate >= thirtyDaysAgo && recDate < yesterday) {
            groups['30 Ngày trước'].push(rec);
        } else {
            // Group by month
            const monthKey = `Tháng ${recDate.getMonth() + 1} năm ${recDate.getFullYear()}`;
            if (!monthGroups[monthKey]) {
                monthGroups[monthKey] = [];
            }
            monthGroups[monthKey].push(rec);
        }
    });

    // Remove empty groups
    const result = {};
    for (const [key, items] of Object.entries(groups)) {
        if (items.length > 0) {
            result[key] = items;
        }
    }

    // Add month groups
    Object.assign(result, monthGroups);

    return result;
}

// Duplicate setupFilterTabs removed. Using the implementation at the bottom of the file.

// ============================================================================
// Recording Popup Workflow
// ============================================================================

function showRecordingPopup() {
    // Show setup modal
    const modal = new bootstrap.Modal(document.getElementById('recordingSetupModal'));
    modal.show();
}

function setupRealtimeToggle() {
    const realtimeCheckbox = document.getElementById('realtimeMode');
    const translateOptions = document.getElementById('translateOptions');

    if (realtimeCheckbox) {
        realtimeCheckbox.addEventListener('change', function () {
            translateOptions.style.display = this.checked ? 'block' : 'none';
        });
    }
}

function startRecording() {
    // Get form values
    const title = document.getElementById('recordingTitle').value;
    const language = document.getElementById('recordingLanguage').value;
    const audioSource = document.querySelector('input[name="audioSource"]:checked').value;
    const realtimeMode = document.getElementById('realtimeMode').checked;
    const translateLang = document.getElementById('translateLanguage').value;

    // Save config
    currentRecordingConfig = {
        title,
        language,
        audioSource,
        realtimeMode,
        translateLang
    };

    // Close setup modal
    bootstrap.Modal.getInstance(document.getElementById('recordingSetupModal')).hide();

    // Check audio source
    if (audioSource === 'screen') {
        // Show screen share confirmation
        const screenModal = new bootstrap.Modal(document.getElementById('screenShareModal'));
        screenModal.show();
    } else {
        // Start microphone recording directly
        startMicrophoneRecording();
    }
}

function confirmScreenShare() {
    const allowScreenShare = document.getElementById('allowScreenShare').checked;

    // Close screen share modal
    bootstrap.Modal.getInstance(document.getElementById('screenShareModal')).hide();

    if (allowScreenShare) {
        startScreenRecording();
    } else {
        // Fallback to microphone
        startMicrophoneRecording();
    }
}

// ============================================================================
// Microphone Recording
// ============================================================================

async function startMicrophoneRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        audioChunks = [];
        isRealtimeTranscription = currentRecordingConfig.realtimeMode;

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);

                // Send chunk to server for realtime transcription
                if (isRealtimeTranscription && socket) {
                    sendAudioChunk(event.data);
                }
            }
        };

        mediaRecorder.onstop = () => {
            handleRecordingComplete();
        };

        // Collect data every 2 seconds for realtime transcription
        mediaRecorder.start(2000);

        // Show recording view
        showRecordingView();

    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Lỗi: Không thể truy cập microphone. Vui lòng cho phép quyền truy cập.');
    }
}

function sendAudioChunk(audioBlob) {
    // Convert blob to base64 and send via WebSocket
    const reader = new FileReader();
    reader.onloadend = () => {
        const base64Audio = reader.result.split(',')[1];
        socket.emit('audio_chunk', {
            audio: base64Audio,
            language: currentRecordingConfig.language
        });
    };
    reader.readAsDataURL(audioBlob);
}

// ============================================================================
// Screen Recording
// ============================================================================

async function startScreenRecording() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({
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
            stream.getTracks().forEach(track => track.stop());
            return;
        }

        const audioStream = new MediaStream(audioTracks);
        mediaRecorder = new MediaRecorder(audioStream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            handleRecordingComplete();
        };

        mediaRecorder.start(1000);

        // Stop video tracks (we only need audio)
        stream.getVideoTracks().forEach(track => track.stop());

        // Show recording view
        showRecordingView();

    } catch (error) {
        console.error('Error accessing screen:', error);
        if (error.name === 'NotAllowedError') {
            alert('Bạn đã từ chối chia sẻ màn hình.');
        } else {
            alert('Lỗi: ' + error.message);
        }
    }
}

// ============================================================================
// View Management
// ============================================================================

function showInitialView() {
    document.getElementById('initialView').style.display = 'block';
    document.getElementById('recordingView').style.display = 'none';
    document.getElementById('resultView').style.display = 'none';
}

function showRecordingView() {
    document.getElementById('initialView').style.display = 'none';
    document.getElementById('recordingView').style.display = 'block';
    document.getElementById('resultView').style.display = 'none';

    // Update header info
    document.getElementById('recordingViewTitle').textContent = currentRecordingConfig.title;
    document.getElementById('recordingViewLang').textContent = getLanguageName(currentRecordingConfig.language);

    // Clear transcript
    document.getElementById('transcriptContent').innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="bi bi-mic" style="font-size: 3rem;"></i>
            <p class="mt-3">Transcript sẽ xuất hiện ở đây khi bạn nói...</p>
        </div>
    `;

    // Start timer
    recordingStartTime = Date.now();
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
}

function showResultView() {
    document.getElementById('initialView').style.display = 'none';
    document.getElementById('recordingView').style.display = 'none';
    document.getElementById('resultView').style.display = 'block';
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;

    const timerText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Update both timers
    const viewTimer = document.getElementById('recordingViewTimer');
    if (viewTimer) {
        viewTimer.textContent = timerText;
    }
}

function getLanguageName(code) {
    const names = {
        'vi': 'Tiếng Việt',
        'en': 'English',
        'ja': '日本語',
        'ko': '한국어',
        'zh': '中文'
    };
    return names[code] || code;
}

function toggleTranslation() {
    // TODO: Implement translation toggle
    alert('Tính năng dịch đang được phát triển');
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();

        // Stop timer
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }

        // Notify server to process final transcription
        if (socket && isRealtimeTranscription) {
            socket.emit('stop_recording', {
                language: currentRecordingConfig.language
            });
        }

        // Stop all tracks
        if (mediaRecorder.stream) {
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
}

function handleFinalTranscript(transcript) {
    // Show final transcript
    document.getElementById('finalTranscript').textContent = transcript;
    document.getElementById('resultViewTitle').textContent = currentRecordingConfig.title;

    // Calculate duration
    const duration = Math.floor((Date.now() - recordingStartTime) / 1000);
    const mins = Math.floor(duration / 60);
    const secs = duration % 60;
    document.getElementById('resultViewDuration').textContent = `${mins}:${String(secs).padStart(2, '0')}`;

    // Switch to result view
    showResultView();

    // Save recording
    saveRecording(transcript);

    // Refresh history
    refreshHistory();
}

// ============================================================================
// Handle Recording Complete
// ============================================================================

async function handleRecordingComplete() {
    // Stop timer
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    // Create audio blob
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

    // Show processing message in transcript area
    updateTranscript('🔄 Đang xử lý audio và transcribe...\n\nVui lòng đợi, quá trình này có thể mất vài phút.');

    // Upload and transcribe with streaming
    const formData = new FormData();
    formData.append('audio', audioBlob, `recording_${Date.now()}.webm`);
    formData.append('language', currentRecordingConfig.language);
    formData.append('realtime', currentRecordingConfig.realtimeMode);

    try {
        // Use streaming endpoint
        const response = await fetch('/api/upload/process/stream', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Transcription failed');
        }

        // Read SSE stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullTranscript = '';

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.substring(6));

                    if (data.error) {
                        updateTranscript('❌ Lỗi: ' + data.error);
                        return;
                    }

                    if (data.done) {
                        // Transcription complete
                        document.getElementById('finalTranscript').textContent = fullTranscript;
                        document.getElementById('resultViewTitle').textContent = currentRecordingConfig.title;

                        // Calculate duration
                        const duration = Math.floor((Date.now() - recordingStartTime) / 1000);
                        const mins = Math.floor(duration / 60);
                        const secs = duration % 60;
                        document.getElementById('resultViewDuration').textContent = `${mins}:${String(secs).padStart(2, '0')}`;

                        // Switch to result view
                        showResultView();

                        // Save recording
                        await saveRecording(fullTranscript);

                        // Refresh history
                        refreshHistory();

                        return;
                    }

                    if (data.update) {
                        // Update transcript in real-time
                        fullTranscript = data.update;
                        updateTranscript(data.update);
                    }
                }
            }
        }

    } catch (error) {
        console.error('Error transcribing:', error);
        updateTranscript('❌ Lỗi khi transcribe: ' + error.message);
    }
}

async function saveRecording(transcript) {
    try {
        const response = await fetch('/api/recording/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: currentRecordingConfig.title,
                language: currentRecordingConfig.language,
                transcript: transcript
            })
        });

        const data = await response.json();
        console.log('Recording saved:', data);
    } catch (error) {
        console.error('Error saving recording:', error);
    }
}

// ============================================================================
// Transcript Display
// ============================================================================

// ============================================================================
// Transcript Display
// ============================================================================

function updateTranscript(text_or_data) {
    const container = document.getElementById('transcriptContent');
    const placeholder = document.getElementById('transcriptPlaceholder');

    // Hide placeholder if we have content
    if (placeholder) {
        placeholder.style.display = 'none';
    }

    // Handle legacy text-only updates
    if (typeof text_or_data === 'string') {
        // Only if empty
        if (container.children.length <= 1) { // 1 is placeholder
            const bubble = createBubble('Guest-1', text_or_data, 1);
            container.appendChild(bubble);
        } else {
            // Update last bubble
            const lastBubble = container.lastElementChild;
            const textEl = lastBubble.querySelector('.chat-text');
            if (textEl) textEl.textContent = text_or_data;
        }
        return;
    }

    // Handle segment-based updates
    if (text_or_data && text_or_data.segments) {
        // We will rebuild the view for simplicity to keep sync
        // Optimization: In production, we should diff.

        // Clear current bubbles (except placeholder if we want to keep it hidden)
        // Actually, let's keep it simple: wipe and rebuild.
        container.innerHTML = '';
        if (placeholder) {
            placeholder.style.display = 'none';
        }

        // Render segments
        let lastSpeaker = null;
        let speakerIndex = 1;
        const speakerMap = {}; // Map 'SPEAKER_00' -> 1

        text_or_data.segments.forEach(seg => {
            const rawSpeaker = seg.speaker || 'Guest-1';

            // Map raw speaker to index 1, 2, 3...
            if (!speakerMap[rawSpeaker]) {
                speakerMap[rawSpeaker] = Object.keys(speakerMap).length + 1;
            }
            const processedSpeakerIndex = speakerMap[rawSpeaker];
            const displaySpeaker = rawSpeaker.replace('SPEAKER_', 'Guest-');

            const bubble = createBubble(displaySpeaker, seg.text, processedSpeakerIndex);
            container.appendChild(bubble);
        });

        // Auto scroll to bottom
        container.scrollTop = container.scrollHeight;
    }
}

function createBubble(speakerName, text, speakerIndex = 1) {
    // Determine class based on speaker index to alternate colors
    // 1 -> speaker-1 (Left, Blue)
    // 2 -> speaker-2 (Right, Cyan)
    // 3 -> speaker-3 (Left, Amber)
    // ...
    const styleIndex = ((speakerIndex - 1) % 3) + 1; // 1, 2, 3

    const div = document.createElement('div');
    div.className = `chat-bubble speaker-${styleIndex}`;

    // Format timestamp if available (optional)
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    div.innerHTML = `
        <div class="chat-header">
            <div class="speaker-avatar">${speakerName.charAt(0)}</div>
            <div class="speaker-name">${speakerName}</div>
            <div class="timestamp">${timeStr}</div>
        </div>
        <div class="chat-text">${text}</div>
    `;

    return div;
}

// Update socket event handler structure in initializeSocket
// Existing: socket.on('transcript_update', (data) => updateTranscript(data.text));
// We need to change receiving logic too.


function saveCurrentRecording() {
    alert('Bản ghi đã được lưu!');
    showInitialView();
}

// ============================================================================
// Load Recording from History
// ============================================================================

function loadRecording(recordingId) {
    fetch(`/api/recording/load/${recordingId}`)
        .then(res => res.json())
        .then(data => {
            showTranscriptArea();
            updateTranscript(data.transcript || 'Không có transcript');

            // TODO: Show audio player if needed
        })
        .catch(err => {
            console.error('Error loading recording:', err);
            alert('Lỗi tải bản ghi: ' + err.message);
        });
}

// ============================================================================
// Delete Recording
// ============================================================================

function deleteRecording(recordingId) {
    if (!confirm('Bạn có chắc muốn xóa bản ghi này?')) {
        return;
    }

    fetch(`/api/recording/delete/${recordingId}`, {
        method: 'DELETE'
    })
        .then(res => res.json())
        .then(data => {
            alert(data.status);
            refreshHistory();
        })
        .catch(err => {
            console.error('Error deleting recording:', err);
            alert('Lỗi xóa bản ghi: ' + err.message);
        });
}


// ============================================================================
// Upload & Transcribe (Tab 3)
// ============================================================================

function initializeFileTypeToggle() {
    // Toggle file type
    const fileTypeRadios = document.querySelectorAll('input[name="fileType"]');
    if (fileTypeRadios.length === 0) return; // Not loaded yet

    fileTypeRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            const fileType = this.value;

            if (fileType === 'audio') {
                document.getElementById('audioFileSection').style.display = 'block';
                document.getElementById('textFileSection').style.display = 'none';
                document.getElementById('audioOptions').style.display = 'block';
            } else {
                document.getElementById('audioFileSection').style.display = 'none';
                document.getElementById('textFileSection').style.display = 'block';
                document.getElementById('audioOptions').style.display = 'none';
            }
        });
    });
}

function processUpload() {
    const fileType = document.querySelector('input[name="fileType"]:checked').value;
    const meetingType = document.getElementById('uploadMeetingType').value;
    const outputLang = document.getElementById('uploadOutputLang').value;
    const transcribeLang = document.getElementById('transcribeLang').value;
    const enableDiarization = document.getElementById('enableDiarization').checked;

    let fileInput, file;

    if (fileType === 'audio') {
        fileInput = document.getElementById('audioFileInput');
        file = fileInput.files[0];

        if (!file) {
            showUploadStatus('❌ Vui lòng chọn file audio!', 'danger');
            return;
        }
    } else {
        fileInput = document.getElementById('textFileInput');
        file = fileInput.files[0];

        if (!file) {
            showUploadStatus('❌ Vui lòng chọn file text!', 'danger');
            return;
        }
    }

    // Show loading popup
    showLoadingPopup(
        fileType === 'audio' ? 'Đang transcribe audio...' : 'Đang đọc file...',
        'Vui lòng đợi, quá trình này có thể mất vài phút'
    );

    // Clear previous results
    document.getElementById('uploadTranscript').innerHTML = '<div class="text-center text-muted py-5"><i class="bi bi-hourglass-split" style="font-size: 2rem;"></i><p class="mt-2">Đang xử lý...</p></div>';
    document.getElementById('uploadSummary').innerHTML = '<em class="text-muted">Đang phân tích...</em>';
    document.getElementById('uploadTopics').innerHTML = '<em class="text-muted">Đang phân tích...</em>';
    document.getElementById('uploadActions').innerHTML = '<em class="text-muted">Đang phân tích...</em>';
    document.getElementById('uploadDecisions').innerHTML = '<em class="text-muted">Đang phân tích...</em>';
    document.getElementById('uploadParticipants').innerHTML = '<em class="text-muted">Đang phân tích...</em>';

    // Prepare form data
    const formData = new FormData();
    formData.append('file_type', fileType);
    formData.append('meeting_type', meetingType);
    formData.append('output_lang', outputLang);
    formData.append('transcribe_lang', transcribeLang);
    formData.append('enable_diarization', enableDiarization);

    if (fileType === 'audio') {
        formData.append('audio_file', file);
    } else {
        formData.append('text_file', file);
    }

    // Update loading message after 3 seconds
    setTimeout(() => {
        updateLoadingPopup('Đang phân tích với AI...', 'Trợ lý AI đang xử lý nội dung');
    }, 3000);

    // Send request
    fetch('/api/upload/process', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            // Hide loading popup
            hideLoadingPopup();

            if (data.error) {
                showUploadStatus('❌ Lỗi: ' + data.error, 'danger');
                return;
            }

            // Show results
            showUploadStatus(data.status, 'success');

            // Update transcript with better formatting
            document.getElementById('uploadTranscript').innerHTML =
                `<div style="white-space: pre-wrap; line-height: 1.8; font-size: 15px;">${formatTranscript(data.transcript)}</div>`;

            // Update analysis with markdown rendering
            document.getElementById('uploadSummary').innerHTML = formatMarkdown(data.summary) || '<em class="text-muted">Không có dữ liệu</em>';
            document.getElementById('uploadTopics').innerHTML = formatMarkdown(data.topics) || '<em class="text-muted">Không có dữ liệu</em>';
            document.getElementById('uploadActions').innerHTML = formatMarkdown(data.actions) || '<em class="text-muted">Không có dữ liệu</em>';
            document.getElementById('uploadDecisions').innerHTML = formatMarkdown(data.decisions) || '<em class="text-muted">Không có dữ liệu</em>';
            document.getElementById('uploadParticipants').innerHTML = formatMarkdown(data.participants) || '<em class="text-muted">Không có thông tin</em>';

            // Switch to analysis tab if analysis is done
            if (data.summary) {
                setTimeout(() => {
                    document.getElementById('analysis-tab').click();
                }, 500);
            }
        })
        .catch(err => {
            console.error('Upload error:', err);
            hideLoadingPopup();
            showUploadStatus('❌ Lỗi: ' + err.message, 'danger');
        });
}

function showUploadStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.style.display = 'block';
    statusDiv.className = `alert alert-${type}`;
    statusDiv.innerHTML = message;
}


// ============================================================================
// Category Navigation
// ============================================================================

// ============================================================================
// Category Navigation
// ============================================================================

function setupFilterTabs() {
    // Legacy function kept for compatibility if needed, but navigation is now handled
    // directly by onclick="switchTab()" in index.html to avoid conflicts.
    console.log('Navigation initialized via inline onclick handlers.');
}

// showViewForCategory removed to prevent conflict with switchTab



// ============================================================================
// AI Chat Widget
// ============================================================================



function sendQuickQuestion(question) {
    // Add user message
    addChatMessage(question, 'user');

    // Send to API
    sendChatToAPI(question);
}

function sendChatMessage() {
    const input = document.getElementById('aiChatInputField');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addChatMessage(message, 'user');

    // Clear input
    input.value = '';

    // Send to API
    sendChatToAPI(message);
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('aiChatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'ai-message';

    const now = new Date();
    const timeStr = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="bi bi-${sender === 'user' ? 'person-fill' : 'robot'}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${text}</div>
            <div class="message-time">${timeStr}</div>
        </div>
    `;

    messagesDiv.appendChild(messageDiv);

    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Update history
    chatHistory.push({
        role: sender === 'user' ? 'user' : 'assistant',
        content: text
    });
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('aiChatMessages');

    const typingDiv = document.createElement('div');
    typingDiv.className = 'ai-message';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="bi bi-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideTypingIndicator() {
    const typingDiv = document.getElementById('typingIndicator');
    if (typingDiv) {
        typingDiv.remove();
    }
}

function sendChatToAPI(message) {
    // Show typing indicator
    showTypingIndicator();

    // Prepare chat history for API
    const apiHistory = chatHistory.map(msg => [
        msg.role === 'user' ? message : '',
        msg.role === 'assistant' ? msg.content : ''
    ]);

    // Send to API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            history: apiHistory
        })
    })
        .then(res => res.json())
        .then(data => {
            // Hide typing indicator
            hideTypingIndicator();

            // Get AI response
            const aiResponse = data.answer;

            // Add AI message
            addChatMessage(aiResponse, 'ai');
        })
        .catch(err => {
            console.error('Chat error:', err);
            hideTypingIndicator();
            addChatMessage('❌ Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.', 'ai');
        });
}

// Show notification badge when new message arrives (optional)
function showChatNotification() {
    const badge = document.getElementById('chatBadge');
    const chatWindow = document.getElementById('aiChatWindow');

    if (chatWindow.style.display === 'none') {
        badge.style.display = 'flex';
        badge.textContent = '1';
    }
}


// ============================================================================
// Loading Popup Helpers
// ============================================================================

function showLoadingPopup(title, message) {
    document.getElementById('loadingTitle').textContent = title;
    document.getElementById('loadingMessage').textContent = message;
    document.getElementById('loadingPopup').style.display = 'flex';
}

function updateLoadingPopup(title, message) {
    document.getElementById('loadingTitle').textContent = title;
    document.getElementById('loadingMessage').textContent = message;
}

function hideLoadingPopup() {
    document.getElementById('loadingPopup').style.display = 'none';
}

// ============================================================================
// Text Formatting Helpers
// ============================================================================

function formatTranscript(text) {
    if (!text) return '<em class="text-muted">Không có transcript</em>';

    // Clean up text
    text = text.trim();

    // Highlight speaker labels if present
    text = text.replace(/\[(\d+:\d+)\] \*\*(Guest-\d+)\*\*:/g,
        '<span style="color: #0d6efd; font-weight: 600;">[$1] $2:</span>');

    // Highlight timestamps
    text = text.replace(/\[(\d+:\d+)\]/g,
        '<span style="color: #6c757d; font-size: 0.9em;">[$1]</span>');

    return text;
}

function formatMarkdown(text) {
    if (!text) return '';

    // Clean up text
    text = text.trim();

    // Convert markdown-style headers
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Convert bold
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Convert italic
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Convert lists
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');

    // Wrap consecutive <li> in <ul>
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Convert line breaks to paragraphs
    text = text.split('\n\n').map(para => {
        if (para.trim() && !para.startsWith('<')) {
            return '<p>' + para + '</p>';
        }
        return para;
    }).join('\n');

    // Highlight action items
    text = text.replace(/<li>(.+?)\((.+?)\)<\/li>/g,
        '<li class="action-item"><strong>$1</strong> <span style="color: #6c757d;">($2)</span></li>');

    return text;
}


// ============================================================================
// Export Functions
// ============================================================================

function exportToTXT() {
    showLoadingPopup('Đang tạo file TXT...', 'Vui lòng đợi');

    fetch('/api/export/txt')
        .then(res => {
            if (!res.ok) {
                throw new Error('Không có dữ liệu để xuất. Vui lòng phân tích transcript trước.');
            }
            return res.blob();
        })
        .then(blob => {
            hideLoadingPopup();

            // Download file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `meeting_analysis_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show success
            showUploadStatus('✅ Đã xuất file TXT thành công!', 'success');
        })
        .catch(err => {
            hideLoadingPopup();
            console.error('Export error:', err);
            showUploadStatus('❌ ' + err.message, 'danger');
        });
}

function exportToDOCX() {
    showLoadingPopup('Đang tạo file DOCX...', 'Vui lòng đợi');

    fetch('/api/export/docx')
        .then(res => {
            if (!res.ok) {
                throw new Error('Không có dữ liệu để xuất. Vui lòng phân tích transcript trước.');
            }
            return res.blob();
        })
        .then(blob => {
            hideLoadingPopup();

            // Download file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `meeting_analysis_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.docx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show success
            showUploadStatus('✅ Đã xuất file DOCX thành công!', 'success');
        })
        .catch(err => {
            hideLoadingPopup();
            console.error('Export error:', err);
            showUploadStatus('❌ ' + err.message, 'danger');
        });
}




// ============================================================================
// Analysis History
// ============================================================================

function refreshAnalysisHistory() {
    fetch('/api/history/list')
        .then(res => res.json())
        .then(data => {
            renderAnalysisHistoryList(data.dropdown || []);
        })
        .catch(err => {
            console.error('Error loading analysis history:', err);
            document.getElementById('analysisHistoryList').innerHTML = `
                <div class="alert alert-danger small">
                    Lỗi tải lịch sử: ${err.message}
                </div>
            `;
        });
}

function renderAnalysisHistoryList(historyItems) {
    const listDiv = document.getElementById('analysisHistoryList');

    if (!historyItems || historyItems.length === 0) {
        listDiv.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                <p class="mt-2 small">Chưa có phân tích nào</p>
            </div>
        `;
        return;
    }

    // Group by date
    const grouped = groupAnalysisByDate(historyItems);

    let html = '';
    for (const [dateLabel, items] of Object.entries(grouped)) {
        html += `
            <div class="mb-3">
                <div class="text-muted small fw-bold mb-2">${dateLabel}</div>
        `;

        items.forEach(item => {
            let label, id;
            if (Array.isArray(item)) {
                label = item[0];
                id = item[1];
            } else {
                label = item;
                id = item;
            }

            // Parse item format: "YYYY-MM-DD - filename"
            // The backend returns "timestamp - filename"
            const parts = label.split(' - ');
            const timestampPart = parts[0] || '';
            const filename = parts.slice(1).join(' - ') || label;

            html += `
                <div class="compact-item" onclick="loadAnalysisHistory('${id}')" title="${filename}">
                    <div class="item-title">${filename}</div>
                    <div class="item-meta">
                        <i class="bi bi-file-text"></i> ${timestampPart}
                    </div>
                </div>
            `;
        });

        html += `</div>`;
    }

    listDiv.innerHTML = html;
}





// ============================================================================
// Full Page History View
// ============================================================================

function loadHistoryView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = `
        <tr>
            <td colspan="5" class="text-center py-5 text-muted">
                <div class="spinner-border spinner-border-sm" role="status"></div>
                <span class="ms-2">Đang tải dữ liệu...</span>
            </td>
        </tr>
    `;

    // Fetch all history
    fetch('/api/chat/history/list') // Correction: Use correct API endpoint
        .then(res => res.json())
        .then(data => {
            // API returns { dropdown: [[label, id], ...], info: ... }
            if (!data.dropdown || data.dropdown.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center py-5 text-muted">
                            <i class="bi bi-inbox-fill fs-4 d-block mb-2"></i>
                            Chưa có dữ liệu lịch sử
                        </td>
                    </tr>
                `;
                return;
            }

            renderHistoryTable(data.dropdown);
        })
        .catch(err => {
            console.error('Error loading history view:', err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-4 text-danger">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        Lỗi tải dữ liệu: ${err.message}
                    </td>
                </tr>
            `;
        });
}

function renderHistoryTable(items) {
    const tableBody = document.getElementById('historyTableBody');
    tableBody.innerHTML = '';

    items.forEach(item => {
        // item is [label, id]
        // label format: "2023-10-27 - meeting_audio.mp3"
        const label = item[0];
        const id = item[1];

        const date = label.split(' - ')[0] || 'N/A';
        const name = label.split(' - ').slice(1).join(' - ') || 'Bản ghi không tên';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="ps-4 fw-medium text-primary">
                <i class="bi bi-file-earmark-music me-2 text-secondary"></i>
                <a href="#" onclick="loadHistoryItem('${id}')" style="text-decoration: none;">${name}</a>
            </td>
            <td>${date}</td>
            <td>--:--</td>
            <td><span class="badge bg-success bg-opacity-10 text-success">Hoàn thành</span></td>
            <td class="text-end pe-4">
                <button class="btn btn-sm btn-outline-primary me-1" onclick="loadHistoryItem('${id}')" title="Xem chi tiết">
                    <i class="bi bi-eye"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


// ============================================================================
// Full Page Chat Logic
// ============================================================================

function handleFullChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendFullChatMessage();
    }
}

function sendFullChatMessage() {
    const input = document.getElementById('fullChatInput');
    const message = input.value.trim();
    if (!message) return;

    // Clear input
    input.value = '';

    // Add user message
    addFullChatMessage(message, 'user');

    // Show typing
    showFullTyping();

    // Call API
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
        .then(res => res.json())
        .then(data => {
            hideFullTyping();
            const response = data.answer || "Xin lỗi, tôi không hiểu.";
            addFullChatMessage(response, 'ai');
        })
        .catch(err => {
            hideFullTyping();
            addFullChatMessage("❌ Lỗi kết nối: " + err.message, 'ai');
        });
}

function addFullChatMessage(text, sender) {
    const container = document.getElementById('fullChatMessages');
    const welcome = document.getElementById('fullChatWelcome');

    if (welcome) welcome.style.display = 'none';

    const div = document.createElement('div');
    const isAi = sender === 'ai';

    div.className = `d-flex ${isAi ? 'flex-row' : 'flex-row-reverse'} align-items-start`;

    div.style.marginBottom = "1rem";

    div.innerHTML = `
        <div class="flex-shrink-0 ${isAi ? 'me-3' : 'ms-3'}">
            <div class="rounded-circle d-flex align-items-center justify-content-center text-white" 
                 style="width: 40px; height: 40px; background-color: ${isAi ? '#2563eb' : '#475569'}">
                <i class="bi ${isAi ? 'bi-robot' : 'bi-person-fill'}"></i>
            </div>
        </div>
        <div class="p-3 rounded-3 shadow-sm" 
             style="max-width: 75%; background-color: ${isAi ? '#f8fafc' : '#2563eb'}; color: ${isAi ? '#1e293b' : 'white'}">
            <div style="white-space: pre-wrap;">${text}</div>
        </div>
    `;

    container.appendChild(div);
    container.scrollTo(0, container.scrollHeight);
}

function showFullTyping() {
    const typing = document.getElementById('fullChatTyping');
    if (typing) {
        typing.style.display = 'block';
        document.getElementById('fullChatContainer').scrollTo(0, document.getElementById('fullChatContainer').scrollHeight);
    }
}

function hideFullTyping() {
    const typing = document.getElementById('fullChatTyping');
    if (typing) typing.style.display = 'none';
}

function clearChat() {
    document.getElementById('fullChatMessages').innerHTML = '';
    const welcome = document.getElementById('fullChatWelcome');
    if (welcome) welcome.style.display = 'block';
}

function loadHistoryItem(id) {
    // Show loading
    fetch(`/api/chat/history/load/${id}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert('Lỗi: ' + data.error);
                return;
            }

            // Show details in a modal
            showHistoryDetailModal(data);
        })
        .catch(err => {
            console.error('Error loading item:', err);
            alert('Lỗi tải chi tiết: ' + err.message);
        });
}

function showHistoryDetailModal(data) {
    // Create modal if not exists
    let modal = document.getElementById('historyDetailModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'historyDetailModal';
        modal.className = 'modal fade';
        modal.tabIndex = -1;
        modal.innerHTML = `
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Chi tiết Cuộc họp</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="historyModalContent"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    const content = document.getElementById('historyModalContent');
    content.innerHTML = `
        <div class="mb-4">
            <h6 class="fw-bold text-primary">Tóm tắt</h6>
            <div class="bg-light p-3 rounded" style="white-space: pre-wrap;">${data.summary || '_Chưa có tóm tắt_'}</div>
        </div>
        <div class="mb-4">
            <h6 class="fw-bold text-primary">Chủ đề chính</h6>
            <div class="p-2" style="white-space: pre-wrap;">${data.topics || '_Chưa có chủ đề_'}</div>
        </div>
        <div class="row">
             <div class="col-md-6 mb-3">
                <h6 class="fw-bold text-primary">Thông tin</h6>
                <div class="small text-muted p-2 bg-light rounded">${data.info || ''}</div>
             </div>
        </div>
    `;

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}
