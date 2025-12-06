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
    
    // Hide all views
    const views = ['initialView', 'recordingView', 'uploadView', 'exportView', 'smartSearchView'];
    views.forEach(viewId => {
        const el = document.getElementById(viewId);
        if (el) el.style.display = 'none';
    });
    
    // Show/hide history lists
    const recordingList = document.getElementById('recordingList');
    const analysisHistoryList = document.getElementById('analysisHistoryList');
    
    if (recordingList) recordingList.style.display = 'none';
    if (analysisHistoryList) analysisHistoryList.style.display = 'none';
    
    // Show appropriate view and list
    switch(category) {
        case 'recording':
            document.getElementById('initialView').style.display = 'block';
            if (recordingList) recordingList.style.display = 'block';
            refreshHistory();
            console.log('✅ Showing: Recording view');
            break;
            
        case 'upload':
            document.getElementById('uploadView').style.display = 'block';
            if (analysisHistoryList) analysisHistoryList.style.display = 'block';
            try { refreshAnalysisHistory(); } catch(e) {}
            console.log('✅ Showing: Upload view');
            break;
            
        case 'export':
            document.getElementById('exportView').style.display = 'block';
            console.log('✅ Showing: Export view');
            break;
            
        case 'smart-search':
            document.getElementById('smartSearchView').style.display = 'block';
            try { refreshRAGStats(); } catch(e) { console.log('RAG stats not available'); }
            console.log('✅ Showing: Smart Search view');
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
        updateTranscript(data.text);
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
        const response = await fetch('/api/transcribe/stream', {
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

function updateTranscript(text) {
    document.getElementById('transcriptContent').textContent = text;
}

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

function setupFilterTabs() {
    console.log('Setting up filter tabs...');
    // Handle category tab clicks
    const links = document.querySelectorAll('.nav-link[data-category]');
    console.log('Found links:', links.length);

    links.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            console.log('Tab clicked:', this.dataset.category);

            // Update active state
            document.querySelectorAll('.nav-link[data-category]').forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // Get category
            const category = this.dataset.category;

            // Show appropriate view
            showViewForCategory(category);

            // Show/hide appropriate history list
            if (category === 'recording') {
                document.getElementById('recordingList').style.display = 'block';
                document.getElementById('analysisHistoryList').style.display = 'none';
                refreshHistory();
            } else if (category === 'upload') {
                document.getElementById('recordingList').style.display = 'none';
                document.getElementById('analysisHistoryList').style.display = 'block';
                refreshAnalysisHistory();
            } else {
                document.getElementById('recordingList').style.display = 'none';
                document.getElementById('analysisHistoryList').style.display = 'none';
            }
        });
    });
}

function showViewForCategory(category) {
    console.log('=== Switching to view:', category, '===');
    
    // Get all view elements
    const views = {
        'initialView': document.getElementById('initialView'),
        'recordingView': document.getElementById('recordingView'),
        'uploadView': document.getElementById('uploadView'),
        'exportView': document.getElementById('exportView'),
        'smartSearchView': document.getElementById('smartSearchView')
    };
    
    // Check if all views exist
    Object.keys(views).forEach(id => {
        if (!views[id]) {
            console.error('❌ View not found:', id);
        }
    });
    
    // Hide all views
    Object.values(views).forEach(view => {
        if (view) view.style.display = 'none';
    });

    // Show appropriate view
    if (category === 'recording') {
        if (views.initialView) {
            views.initialView.style.display = 'block';
            console.log('✅ Showing initialView');
        }
    } else if (category === 'upload') {
        if (views.uploadView) {
            views.uploadView.style.display = 'block';
            console.log('✅ Showing uploadView');
        }
    } else if (category === 'export') {
        if (views.exportView) {
            views.exportView.style.display = 'block';
            console.log('✅ Showing exportView');
        }
    } else if (category === 'smart-search') {
        if (views.smartSearchView) {
            views.smartSearchView.style.display = 'block';
            console.log('✅ Showing smartSearchView');
            // Auto-load RAG stats
            try {
                if (typeof refreshRAGStats === 'function') {
                    refreshRAGStats();
                }
            } catch (e) {
                console.log('RAG stats not available:', e);
            }
        }
    }
    
    console.log('=== View switch complete ===');
}


// ============================================================================
// AI Chat Widget
// ============================================================================

let chatHistory = [];

function toggleAIChat() {
    const chatWindow = document.getElementById('aiChatWindow');
    const chatToggle = document.getElementById('aiChatToggle');

    if (chatWindow.style.display === 'none') {
        chatWindow.style.display = 'flex';
        chatToggle.style.display = 'none';

        // Hide badge
        document.getElementById('chatBadge').style.display = 'none';
    } else {
        chatWindow.style.display = 'none';
        chatToggle.style.display = 'flex';
    }
}

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

            // Get AI response (last message in history)
            const aiResponse = data.history[data.history.length - 1][1];

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
            showExportStatus('✅ Đã xuất file TXT thành công!', 'success');

            // Add to recent exports
            addRecentExport(a.download, 'TXT');
        })
        .catch(err => {
            hideLoadingPopup();
            console.error('Export error:', err);
            showExportStatus('❌ ' + err.message, 'danger');
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
            showExportStatus('✅ Đã xuất file DOCX thành công!', 'success');

            // Add to recent exports
            addRecentExport(a.download, 'DOCX');
        })
        .catch(err => {
            hideLoadingPopup();
            console.error('Export error:', err);
            showExportStatus('❌ ' + err.message, 'danger');
        });
}

function showExportStatus(message, type) {
    const statusDiv = document.getElementById('exportStatus');
    statusDiv.style.display = 'block';
    statusDiv.className = `alert alert-${type}`;
    statusDiv.innerHTML = message;

    // Auto hide after 5 seconds
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

function addRecentExport(filename, type) {
    const recentDiv = document.getElementById('recentExports');

    // Initialize if empty
    if (recentDiv.innerHTML.includes('Chưa có file')) {
        recentDiv.innerHTML = '';
    }

    const now = new Date().toLocaleString('vi-VN');
    const icon = type === 'TXT' ? 'file-text' : 'file-earmark-word';

    const exportItem = document.createElement('div');
    exportItem.className = 'export-item';
    exportItem.innerHTML = `
        <div>
            <i class="bi bi-${icon} text-primary"></i>
            <strong>${filename}</strong>
            <br>
            <small class="text-muted">${now}</small>
        </div>
        <span class="badge bg-primary">${type}</span>
    `;

    // Add to top
    recentDiv.insertBefore(exportItem, recentDiv.firstChild);

    // Keep only last 5
    while (recentDiv.children.length > 5) {
        recentDiv.removeChild(recentDiv.lastChild);
    }
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

function groupAnalysisByDate(items) {
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

    items.forEach(item => {
        let label;
        if (Array.isArray(item)) {
            label = item[0];
        } else {
            label = item;
        }

        // Parse timestamp from label string "YYYY-MM-DD - filename"
        const parts = label.split(' - ');
        if (parts.length < 2) {
            groups['30 Ngày trước'].push(item);
            return;
        }

        const timestampStr = parts[0]; // First part is timestamp
        const itemDate = new Date(timestampStr);
        const itemDateOnly = new Date(itemDate.getFullYear(), itemDate.getMonth(), itemDate.getDate());

        if (itemDateOnly.getTime() === today.getTime()) {
            groups['Hôm nay'].push(item);
        } else if (itemDateOnly.getTime() === yesterday.getTime()) {
            groups['Hôm qua'].push(item);
        } else if (itemDate >= thirtyDaysAgo && itemDate < yesterday) {
            groups['30 Ngày trước'].push(item);
        } else {
            // Group by month
            const monthKey = `Tháng ${itemDate.getMonth() + 1} năm ${itemDate.getFullYear()}`;
            if (!monthGroups[monthKey]) {
                monthGroups[monthKey] = [];
            }
            monthGroups[monthKey].push(item);
        }
    });

    // Remove empty groups
    Object.keys(groups).forEach(key => {
        if (groups[key].length === 0) {
            delete groups[key];
        }
    });

    // Merge month groups
    return { ...groups, ...monthGroups };
}

function loadAnalysisHistory(historyId) {
    showLoadingPopup('Đang tải phân tích...', 'Vui lòng đợi');

    fetch(`/api/history/load/${encodeURIComponent(historyId)}`)
        .then(res => res.json())
        .then(data => {
            hideLoadingPopup();

            // Switch to upload view
            showViewForCategory('upload');

            // Populate results
            document.getElementById('uploadTranscript').innerHTML =
                '<div class="text-muted"><em>Transcript không có sẵn trong lịch sử</em></div>';

            document.getElementById('uploadSummary').innerHTML =
                formatMarkdown(data.summary) || '<em class="text-muted">Không có dữ liệu</em>';

            document.getElementById('uploadTopics').innerHTML =
                formatMarkdown(data.topics) || '<em class="text-muted">Không có dữ liệu</em>';

            // Parse actions and decisions from info if available
            const infoLines = data.info ? data.info.split('\n') : [];
            let actionsText = '';
            let decisionsText = '';

            // Try to extract from info
            let inActionsSection = false;
            let inDecisionsSection = false;

            infoLines.forEach(line => {
                if (line.includes('Action Items') || line.includes('Công việc')) {
                    inActionsSection = true;
                    inDecisionsSection = false;
                } else if (line.includes('Decisions') || line.includes('Quyết định')) {
                    inDecisionsSection = true;
                    inActionsSection = false;
                } else if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
                    if (inActionsSection) {
                        actionsText += line + '\n';
                    } else if (inDecisionsSection) {
                        decisionsText += line + '\n';
                    }
                }
            });

            document.getElementById('uploadActions').innerHTML =
                formatMarkdown(actionsText) || '<em class="text-muted">Không có dữ liệu</em>';

            document.getElementById('uploadDecisions').innerHTML =
                formatMarkdown(decisionsText) || '<em class="text-muted">Không có dữ liệu</em>';

            document.getElementById('uploadParticipants').innerHTML =
                '<em class="text-muted">Không có thông tin</em>';

            // Switch to analysis tab
            setTimeout(() => {
                document.getElementById('analysis-tab').click();
            }, 300);

            // Show success message
            showUploadStatus(`✅ Đã tải: ${historyId}`, 'success');
        })
        .catch(err => {
            hideLoadingPopup();
            console.error('Error loading history:', err);
            showUploadStatus('❌ Lỗi tải lịch sử: ' + err.message, 'danger');
        });
}


// ============================================================================
// Smart Search with Advanced RAG
// ============================================================================

function handleSmartSearchKeyPress(event) {
    if (event.key === 'Enter') {
        performSmartSearch();
    }
}

function quickSearch(query) {
    document.getElementById('smartSearchInput').value = query;
    performSmartSearch();
}

function performSmartSearch() {
    const query = document.getElementById('smartSearchInput').value.trim();

    if (!query) {
        showSmartSearchResults('<div class="alert alert-warning">Vui lòng nhập câu hỏi tìm kiếm</div>');
        return;
    }

    // Show loading
    showSmartSearchResults(`
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3">AI đang tìm kiếm trong các cuộc họp...</p>
        </div>
    `);

    // Perform smart search
    fetch('/api/rag/smart-search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: query,
            k: 5
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                showSmartSearchResults(`<div class="alert alert-danger">❌ ${data.error}</div>`);
                return;
            }

            renderSmartSearchResults(data);
        })
        .catch(err => {
            console.error('Smart search error:', err);
            showSmartSearchResults(`<div class="alert alert-danger">❌ Lỗi: ${err.message}</div>`);
        });
}

function showSmartSearchResults(html) {
    document.getElementById('smartSearchResults').innerHTML = html;
}

function renderSmartSearchResults(data) {
    const results = data.results || [];

    if (results.length === 0) {
        showSmartSearchResults(`
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i>
                Không tìm thấy kết quả phù hợp với: <strong>"${data.query}"</strong>
                <br><br>
                <small>Thử tìm kiếm với từ khóa khác hoặc phân tích thêm cuộc họp.</small>
            </div>
        `);
        return;
    }

    let html = `
        <div class="alert alert-success">
            <i class="bi bi-check-circle"></i>
            Tìm thấy <strong>${results.length}</strong> kết quả cho: <strong>"${data.query}"</strong>
        </div>
    `;

    results.forEach((result, index) => {
        const metadata = result.metadata || {};
        const meetingId = metadata.meeting_id || 'Unknown';
        const meetingType = metadata.meeting_type || 'meeting';
        const language = metadata.language || 'vi';
        const timestamp = metadata.timestamp ? new Date(metadata.timestamp).toLocaleString('vi-VN') : 'N/A';

        html += `
            <div class="card mb-3 search-result-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title mb-0">
                            <i class="bi bi-file-text text-primary"></i>
                            ${meetingId}
                        </h6>
                        <div>
                            <span class="badge bg-primary">${meetingType}</span>
                            <span class="badge bg-secondary">${language}</span>
                        </div>
                    </div>
                    
                    <p class="card-text text-muted small mb-2">
                        <i class="bi bi-clock"></i> ${timestamp}
                    </p>
                    
                    <div class="search-result-content">
                        ${highlightQuery(result.content, data.query)}
                    </div>
                    
                    ${result.score ? `<small class="text-muted">Relevance: ${(result.score * 100).toFixed(1)}%</small>` : ''}
                </div>
            </div>
        `;
    });

    showSmartSearchResults(html);
}

function highlightQuery(text, query) {
    // Simple highlight - can be improved
    const words = query.toLowerCase().split(' ');
    let highlighted = text;

    words.forEach(word => {
        if (word.length > 3) {
            const regex = new RegExp(`(${word})`, 'gi');
            highlighted = highlighted.replace(regex, '<mark>$1</mark>');
        }
    });

    return highlighted;
}

function refreshRAGStats() {
    document.getElementById('ragStats').innerHTML = `
        <div class="text-center">
            <div class="spinner-border spinner-border-sm"></div>
            <span class="ms-2">Đang tải...</span>
        </div>
    `;

    fetch('/api/rag/stats')
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById('ragStats').innerHTML = `
                    <div class="alert alert-warning mb-0">
                        <i class="bi bi-exclamation-triangle"></i> ${data.error}
                    </div>
                `;
                return;
            }

            const html = `
                <div class="row text-center">
                    <div class="col-md-3">
                        <div class="stat-box">
                            <i class="bi bi-database-fill text-primary" style="font-size: 2rem;"></i>
                            <h4 class="mt-2">${data.total_chunks || 'N/A'}</h4>
                            <small class="text-muted">Total Chunks</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-box">
                            <i class="bi bi-hdd-stack text-success" style="font-size: 2rem;"></i>
                            <h4 class="mt-2">${data.vector_store || 'N/A'}</h4>
                            <small class="text-muted">Vector Store</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-box">
                            <i class="bi bi-cpu text-info" style="font-size: 2rem;"></i>
                            <h4 class="mt-2">${data.embedding_model || 'N/A'}</h4>
                            <small class="text-muted">Embedding Model</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-box">
                            <i class="bi bi-check-circle-fill text-success" style="font-size: 2rem;"></i>
                            <h4 class="mt-2">${data.status || 'N/A'}</h4>
                            <small class="text-muted">Status</small>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('ragStats').innerHTML = html;
        })
        .catch(err => {
            console.error('Stats error:', err);
            document.getElementById('ragStats').innerHTML = `
                <div class="alert alert-danger mb-0">
                    ❌ Lỗi tải thống kê: ${err.message}
                </div>
            `;
        });
}

// Auto-load RAG stats when view is shown
document.addEventListener('DOMContentLoaded', function () {
    // Will be called when smart-search view is shown
});

// ============================================================================
// AI Smart Chat Logic
// ============================================================================

function handleSmartChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendSmartChatMessage();
    }
}

function sendSmartChatMessage() {
    const input = document.getElementById('smartChatInput');
    const message = input.value.trim();
    if (message) {
        sendSmartChat(message);
        input.value = '';
    }
}

function sendSmartChat(message) {
    // Hide welcome message if visible
    const welcome = document.getElementById('smartChatWelcome');
    if (welcome) welcome.style.display = 'none';

    // Append user message
    appendSmartMessage('user', message);

    // Show typing indicator
    showSmartTyping();

    // Call API
    fetch('/api/rag/smart-qa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: message,
            context_k: 3
        })
    })
        .then(res => res.json())
        .then(data => {
            hideSmartTyping();
            if (data.success) {
                appendSmartMessage('ai', data.answer, data.sources);
            } else {
                appendSmartMessage('ai', '❌ Lỗi: ' + (data.error || 'Không xác định'));
            }
        })
        .catch(err => {
            hideSmartTyping();
            console.error('Chat error:', err);
            appendSmartMessage('ai', '❌ Lỗi kết nối: ' + err.message);
        });
}

function appendSmartMessage(role, text, sources = []) {
    const container = document.getElementById('smartChatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = role === 'user' ? 'user-message' : 'ai-message';

    let avatarHtml = role === 'user'
        ? '<div class="message-avatar"><i class="bi bi-person"></i></div>'
        : '<div class="message-avatar"><i class="bi bi-robot"></i></div>';

    // Basic formatting for text (newlines to br)
    let formattedText = text.replace(/\n/g, '<br>');

    // Add sources if available (for AI)
    if (role === 'ai' && sources && sources.length > 0) {
        let sourcesHtml = '<div class="mt-3 small text-muted border-top pt-2">';
        sourcesHtml += '<strong><i class="bi bi-link-45deg"></i> Nguồn tham khảo:</strong><ul class="mb-0 ps-3 mt-1">';

        // Deduplicate sources based on filename
        const uniqueSources = [];
        const seenFiles = new Set();

        sources.forEach(source => {
            const meta = source.metadata || {};
            const filename = meta.filename || 'Unknown file';
            if (!seenFiles.has(filename)) {
                seenFiles.add(filename);
                uniqueSources.push(meta);
            }
        });

        uniqueSources.forEach(meta => {
            const filename = meta.filename || 'Unknown file';
            // Format timestamp if available
            let timeStr = '';
            if (meta.timestamp) {
                try {
                    timeStr = ` (${new Date(meta.timestamp).toLocaleDateString()})`;
                } catch (e) { }
            }
            sourcesHtml += `<li>${filename}${timeStr}</li>`;
        });

        sourcesHtml += '</ul></div>';

        formattedText += sourcesHtml;
    }

    msgDiv.innerHTML = `
        ${role === 'ai' ? avatarHtml : ''}
        <div class="message-content">
            <div class="message-text">
                ${formattedText}
            </div>
            <div class="message-time">${new Date().toLocaleTimeString()}</div>
        </div>
        ${role === 'user' ? avatarHtml : ''}
    `;

    container.appendChild(msgDiv);

    // Scroll to bottom
    const scrollContainer = document.getElementById('smartChatContainer');
    scrollContainer.scrollTop = scrollContainer.scrollHeight;
}

function showSmartTyping() {
    const typing = document.getElementById('smartChatTyping');
    if (typing) {
        typing.style.display = 'flex';
        const scrollContainer = document.getElementById('smartChatContainer');
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
}

function hideSmartTyping() {
    const typing = document.getElementById('smartChatTyping');
    if (typing) typing.style.display = 'none';
}

function clearSmartChat() {
    if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử chat?')) {
        document.getElementById('smartChatMessages').innerHTML = '';
        const welcome = document.getElementById('smartChatWelcome');
        if (welcome) welcome.style.display = 'block';
    }
}
