/**
 * Screen Audio Recorder - Capture audio from browser tabs/windows
 * Uses getDisplayMedia API to record audio from screen shares
 */

class ScreenAudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.stream = null;
    }

    /**
     * Start recording audio from screen/tab
     * @returns {Promise<boolean>} Success status
     */
    async startRecording() {
        try {
            // Request screen share with audio
            this.stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,  // Need video to get tab selection UI
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                }
            });

            // Check if audio track exists
            const audioTracks = this.stream.getAudioTracks();
            if (audioTracks.length === 0) {
                throw new Error('Không có audio track. Hãy bật "Chia sẻ cả âm thanh trên thẻ"');
            }

            // Create audio-only stream (remove video)
            const audioStream = new MediaStream(audioTracks);

            // Setup MediaRecorder
            this.mediaRecorder = new MediaRecorder(audioStream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                console.log('Recording stopped');
            };

            // Start recording
            this.mediaRecorder.start(1000); // Collect data every 1 second

            // Stop video track (we only need audio)
            this.stream.getVideoTracks().forEach(track => track.stop());

            return true;

        } catch (error) {
            console.error('Error starting screen audio recording:', error);
            
            if (error.name === 'NotAllowedError') {
                alert('Bạn đã từ chối chia sẻ màn hình. Vui lòng cho phép để ghi âm.');
            } else if (error.message.includes('audio track')) {
                alert('⚠️ Không phát hiện audio!\n\nHãy đảm bảo:\n1. Chọn tab có audio đang phát\n2. Bật "Chia sẻ cả âm thanh trên thẻ" (checkbox ở dưới)');
            } else {
                alert('Lỗi: ' + error.message);
            }
            
            return false;
        }
    }

    /**
     * Stop recording and return audio blob
     * @returns {Promise<Blob>} Audio blob
     */
    async stopRecording() {
        return new Promise((resolve, reject) => {
            if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
                reject(new Error('No active recording'));
                return;
            }

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                
                // Stop all tracks
                if (this.stream) {
                    this.stream.getTracks().forEach(track => track.stop());
                }
                
                resolve(audioBlob);
            };

            this.mediaRecorder.stop();
        });
    }

    /**
     * Check if recording is active
     * @returns {boolean}
     */
    isRecording() {
        return this.mediaRecorder && this.mediaRecorder.state === 'recording';
    }
}

// Export for use in Gradio
window.ScreenAudioRecorder = ScreenAudioRecorder;
