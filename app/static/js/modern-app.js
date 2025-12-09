// ============================================================================
// Meeting Analyzer Pro - Modern UI JavaScript
// ============================================================================

// Global State
let selectedLanguage = 'en';
let selectedFile = null;
let currentView = 'homepage';

// ============================================================================
// Modal Functions
// ============================================================================

// Recording popup is handled by app.js showRecordingPopup() function
// Card onclick directly calls it via global scope

function showUploadFileModal() {
    const modal = new bootstrap.Modal(document.getElementById('uploadFileModal'));
    modal.show();
}

function selectLanguage(lang) {
    selectedLanguage = lang;
    // Update active state on language buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.getAttribute('onclick')?.includes(lang)) {
            btn.classList.add('active');
        } else if (btn.getAttribute('onclick')?.includes('selectLanguage')) {
            btn.classList.remove('active');
        }
    });
}

// ============================================================================
// Online Meeting Functions
// ============================================================================

function startOnlineMeeting() {
    const urlInput = document.getElementById('meetingUrlInput');
    const url = urlInput.value.trim();

    if (!url) {
        alert('Please enter a meeting URL');
        return;
    }

    // Validate URL
    if (!url.includes('zoom.us') && !url.includes('meet.google.com') && !url.includes('teams.microsoft.com')) {
        alert('Please enter a valid Zoom, Google Meet, or Microsoft Teams URL');
        return;
    }

    // Close modal
    bootstrap.Modal.getInstance(document.getElementById('onlineMeetingModal')).hide();

    // Show loading
    showLoadingPopup('Connecting to meeting...', 'Please wait while we join the meeting');

    // Simulate connection (replace with actual API call)
    setTimeout(() => {
        hideLoadingPopup();
        alert('Feature coming soon! This will connect to your online meeting.');
    }, 2000);
}

// ============================================================================
// In-person Recording Functions
// ============================================================================

async function requestMicPermission() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());

        // Enable start button
        document.getElementById('startRecordingBtn').disabled = false;

        // Update UI
        document.querySelector('.alert-warning').classList.remove('alert-warning');
        document.querySelector('.alert').classList.add('alert-success');
        document.querySelector('.alert strong').textContent = 'Microphone access granted!';
        document.querySelector('.alert p').textContent = 'You can now start recording';

    } catch (error) {
        console.error('Microphone permission denied:', error);
        alert('Please allow microphone access to continue');
    }
}

function startInPersonRecording() {
    // Close modal handled in startModernRecording or here
    if (!file) return;

    selectedFile = file;

    // Show file info
    document.getElementById('selectedFileName').textContent = file.name;
    document.getElementById('selectedFileSize').textContent = formatFileSize(file.size);
    document.getElementById('selectedFileInfo').style.display = 'block';
    document.getElementById('processFileBtn').disabled = false;
}

function clearFileSelection() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('selectedFileInfo').style.display = 'none';
    document.getElementById('processFileBtn').disabled = true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function processUploadedFile() {
    if (!selectedFile) {
        alert('Please select a file first');
        return;
    }

    // Determine file type
    const fileName = selectedFile.name.toLowerCase();
    let fileType = 'audio';
    let fieldName = 'audio_file';

    if (fileName.endsWith('.txt') || fileName.endsWith('.docx') || fileName.endsWith('.pdf')) {
        fileType = 'text';
        fieldName = 'text_file';
    }

    // Close modal
    bootstrap.Modal.getInstance(document.getElementById('uploadFileModal')).hide();

    // Show loading
    showLoadingPopup('Processing file...', 'Analyzing your meeting recording');

    // Create FormData
    const formData = new FormData();
    formData.append(fieldName, selectedFile);
    formData.append('transcribe_lang', selectedLanguage);
    formData.append('file_type', fileType);
    formData.append('meeting_type', 'meeting');
    formData.append('output_lang', selectedLanguage);

    try {
        const response = await fetch('/api/upload/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        hideLoadingPopup();

        if (data.status && typeof data.status === 'string' && data.status.startsWith('✅')) {
            // Show detail view with results
            // Normalize data structure if needed
            const uiData = {
                filename: fileName,
                summary: data.summary,
                topics: data.topics,
                transcript: data.transcript,
                // ... map other fields
            };
            showDetailView(uiData);
        } else if (data.success) {
            showDetailView(data);
        } else {
            // If status contains error or just unexpected
            if (data.status && data.status.startsWith('❌')) {
                alert(data.status);
            } else {
                alert('Error processing file: ' + (data.error || 'Unknown error'));
            }
        }
    } catch (error) {
        hideLoadingPopup();
        console.error('Upload error:', error);
        alert('Error uploading file: ' + error.message);
    }
}

// ============================================================================
// View Navigation
// ============================================================================

function showHistoryView() {
    document.getElementById('homepageView').style.display = 'none';
    document.getElementById('historyView').style.display = 'block';
    currentView = 'history';

    // Load history
    if (typeof loadHistoryView === 'function') {
        loadHistoryView();
    }
}

function showHomepage() {
    document.getElementById('homepageView').style.display = 'block';
    document.getElementById('historyView').style.display = 'none';
    document.getElementById('detailView').style.display = 'none';
    document.getElementById('recordingView').style.display = 'none';
    currentView = 'homepage';
}

function showDetailView(meetingData) {
    // Create detail view HTML
    const detailHTML = createDetailViewHTML(meetingData);
    document.getElementById('detailView').innerHTML = detailHTML;

    // Show detail view
    document.getElementById('homepageView').style.display = 'none';
    document.getElementById('detailView').style.display = 'block';
    currentView = 'detail';
}

function createDetailViewHTML(data) {
    return `
        <div class="container-fluid" style="max-width: 1400px; padding: 2rem;">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <button class="btn btn-outline-secondary" onclick="showHomepage()">
                        <i class="bi bi-arrow-left me-2"></i>Back
                    </button>
                </div>
                    <div class="btn-group">
                        <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-download me-2"></i>Export
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="exportMeeting('txt')"><i class="bi bi-file-text me-2"></i>Text (.txt)</a></li>
                            <li><a class="dropdown-item" href="#" onclick="exportMeeting('docx')"><i class="bi bi-file-word me-2"></i>Word (.docx)</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            </div>
            
            <h2 class="mb-4">${data.filename || 'Meeting Analysis'}</h2>
            
            <ul class="nav nav-tabs mb-4" role="tablist">
                <li class="nav-item">
                    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#notes-tab">Notes</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#askai-tab">Ask AI</button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#transcript-tab">Transcript</button>
                </li>
            </ul>
            
            <div class="tab-content">
                <div class="tab-pane fade show active" id="notes-tab">
                    <div class="row">
                        <div class="col-md-8">
                            <div class="card mb-3">
                                <div class="card-body">
                                    <h5>Summary</h5>
                                    <div>${formatMarkdown(data.summary || 'No summary available')}</div>
                                </div>
                            </div>
                            <div class="card mb-3">
                                <div class="card-body">
                                    <h5>Key Topics</h5>
                                    <div>${formatMarkdown(data.topics || 'No topics available')}</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h6>Visual Notes</h6>
                                    <p class="text-muted small">Mind map coming soon...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="tab-pane fade" id="askai-tab">
                    <div class="card">
                        <div class="card-body">
                            <p class="text-muted">Ask AI feature coming soon...</p>
                        </div>
                    </div>
                </div>
                
                <div class="tab-pane fade" id="transcript-tab">
                    <div class="card">
                        <div class="card-body">
                            <div style="white-space: pre-wrap;">${data.transcript || 'No transcript available'}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ============================================================================
// Meeting List Functions
// ============================================================================

async function loadRecentMeetings() {
    const meetingList = document.getElementById('meetingList');

    try {
        const response = await fetch('/api/recording/history?category=recording');
        const data = await response.json();

        if (data.recordings && data.recordings.length > 0) {
            renderMeetingList(data.recordings);
        } else {
            meetingList.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-inbox" style="font-size: 3rem; color: var(--text-muted);"></i>
                    <p class="mt-3 text-muted">No meetings yet. Start by recording or uploading a meeting!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading meetings:', error);
        meetingList.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: var(--text-danger);"></i>
                <p class="mt-3 text-danger">Error loading meetings</p>
            </div>
        `;
    }
}

function renderMeetingList(meetings) {
    const meetingList = document.getElementById('meetingList');

    // Group by date
    const grouped = groupMeetingsByDate(meetings);

    let html = '';
    for (const [dateLabel, items] of Object.entries(grouped)) {
        html += `
                < div class="meeting-group" >
                    <div class="meeting-group-header">
                        <i class="bi bi-calendar3 meeting-group-icon"></i>
                        <span class="meeting-group-title">${dateLabel}</span>
                        <span class="meeting-group-count">${items.length} meetings - ${calculateTotalDuration(items)}</span>
                    </div>
                ${items.map(item => createMeetingCard(item)).join('')}
            </div >
                `;
    }

    meetingList.innerHTML = html;
}

function groupMeetingsByDate(meetings) {
    const groups = {};
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    meetings.forEach(item => {
        // Handle both older array format and new object format
        let dateStr;
        if (item.timestamp) {
            dateStr = item.timestamp;
        } else if (Array.isArray(item)) {
            // Legacy format: ["2024-12-06 10:00:00 - Title", "id"]
            dateStr = item[0].split(' - ')[0];
        } else {
            return;
        }

        const itemDate = new Date(dateStr);
        const itemDateOnly = new Date(itemDate.getFullYear(), itemDate.getMonth(), itemDate.getDate());

        let groupLabel;
        const diffDays = Math.floor((today - itemDateOnly) / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            groupLabel = 'Today';
        } else if (diffDays === 1) {
            groupLabel = 'Yesterday';
        } else if (diffDays < 30) {
            groupLabel = 'Last 30 days';
        } else {
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            groupLabel = `${monthNames[itemDate.getMonth()]} ${itemDate.getFullYear()} `;
        }

        if (!groups[groupLabel]) {
            groups[groupLabel] = [];
        }
        groups[groupLabel].push(item);
    });

    return groups;
}

function calculateTotalDuration(items) {
    // Placeholder - calculate from actual data
    return `${items.length * 10} .7 minutes`;
}

function createMeetingCard(item) {
    let id, title, dateTime, duration;

    if (item.id) {
        // Object format
        id = item.id;
        title = item.title;
        dateTime = new Date(item.timestamp).toLocaleString();
        duration = item.duration || '0:00';
    } else {
        // Legacy array format
        const label = item[0];
        id = item[1];
        const parts = label.split(' - ');
        dateTime = parts[0];
        title = parts.slice(1).join(' - ');
        duration = 'Unknown';
    }

    return `
                < div class="meeting-card" onclick = "loadMeetingDetail('${id}')" >
            <div class="meeting-card-header">
                <div class="meeting-card-icon">
                    <i class="bi bi-file-earmark-text text-primary"></i>
                </div>
                <div class="meeting-card-info">
                    <h4 class="meeting-card-title">${title}</h4>
                    <div class="meeting-card-meta">
                        <span><i class="bi bi-calendar3 me-1"></i>${dateTime}</span>
                        <span><i class="bi bi-clock me-1"></i>${duration}</span>
                        <span class="meeting-card-badge">
                            <i class="bi bi-person-check"></i>
                            Shared with me
                        </span>
                    </div>
                </div>
            </div>
            <p class="meeting-card-preview">
                Click to view meeting details...
            </p>
        </div >
                `;
}

async function loadMeetingDetail(meetingId) {
    showLoadingPopup('Loading meeting...', 'Please wait');

    try {
        const response = await fetch(`/ api / recording / load / ${encodeURIComponent(meetingId)} `);
        const data = await response.json();

        hideLoadingPopup();

        // Map backend response to UI format
        const uiData = {
            filename: data.info?.title || 'Meeting Analysis',
            summary: data.info?.summary || 'No summary available',
            topics: data.info?.topics || '',
            transcript: data.transcript || 'No transcript available'
        };

        showDetailView(uiData);
    } catch (error) {
        hideLoadingPopup();
        console.error('Error loading meeting:', error);
        alert('Error loading meeting details');
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

function showLoadingPopup(title, message) {
    document.getElementById('loadingTitle').textContent = title;
    document.getElementById('loadingMessage').textContent = message;
    document.getElementById('loadingPopup').style.display = 'flex';
}

function hideLoadingPopup() {
    document.getElementById('loadingPopup').style.display = 'none';
}

function formatMarkdown(text) {
    if (!text) return '';

    // Simple markdown formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function exportMeeting(type) {
    // Open in new tab to trigger download
    // Ensure we have a meeting ID or global context.
    // The backend uses global state for now (based on last analysis).
    // TODO: Pass meeting ID if backend logic changes to stateless.
    window.open(`/api/export/${type}`, '_blank');
}

// ============================================================================
// Search Functions
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('globalSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
});

function handleSearch(event) {
    const query = event.target.value.trim();
    if (query.length < 2) {
        loadRecentMeetings();
        return;
    }

    // Filter meetings based on search query
    // Implement search logic here
    console.log('Searching for:', query);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
