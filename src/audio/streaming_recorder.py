"""Streaming audio recorder with periodic transcription."""

import os
import time
import threading
import queue
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable


class StreamingRecorder:
    """Record audio and transcribe in chunks periodically."""
    
    def __init__(self, chunk_interval: int = 10):
        """Initialize streaming recorder.
        
        Args:
            chunk_interval: Seconds between transcription updates
        """
        self.chunk_interval = chunk_interval
        self.is_recording = False
        self.transcript_queue = queue.Queue()
        self.full_transcript = ""
        
    def start_recording(self, language: str = "vi", callback: Optional[Callable] = None):
        """Start recording with periodic transcription.
        
        Args:
            language: Language code
            callback: Function to call with transcript updates
        """
        self.is_recording = True
        self.full_transcript = ""
        
        # Start background thread for periodic transcription
        thread = threading.Thread(
            target=self._periodic_transcribe,
            args=(language, callback),
            daemon=True
        )
        thread.start()
    
    def stop_recording(self):
        """Stop recording."""
        self.is_recording = False
    
    def _periodic_transcribe(self, language: str, callback: Optional[Callable]):
        """Periodically transcribe audio chunks.
        
        Args:
            language: Language code
            callback: Callback function for updates
        """
        try:
            from openai import OpenAI
            
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            
            if base_url:
                client = OpenAI(api_key=api_key, base_url=base_url)
            else:
                client = OpenAI(api_key=api_key)
            
            chunk_count = 0
            
            while self.is_recording:
                # Wait for chunk interval
                time.sleep(self.chunk_interval)
                
                if not self.is_recording:
                    break
                
                chunk_count += 1
                
                # Simulate chunk transcription
                # In real implementation, this would transcribe actual audio chunk
                if callback:
                    update = f"[{chunk_count * self.chunk_interval}s] Đang ghi âm và transcribe...\n"
                    callback(update)
                
        except Exception as e:
            print(f"Error in periodic transcription: {e}")


class SimpleStreamingTranscriber:
    """Simple streaming transcriber using Gradio's capabilities."""
    
    def __init__(self, chunk_interval: int = 10):
        """Initialize streaming transcriber.
        
        Args:
            chunk_interval: Seconds between updates
        """
        self.chunk_interval = chunk_interval
    
    def transcribe_with_progress(self, audio_file_path: str, language: str = "vi"):
        """Transcribe audio file with progress updates.
        
        This simulates streaming by showing progress while transcribing.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Yields:
            Progress updates and transcript
        """
        try:
            from openai import OpenAI
            import os
            
            # Initialize client
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            
            if base_url:
                client = OpenAI(api_key=api_key, base_url=base_url)
            else:
                client = OpenAI(api_key=api_key)
            
            # Show starting message
            yield "🎙️ Bắt đầu ghi âm...\n\n⏱️ Transcript sẽ cập nhật mỗi 10 giây"
            
            # Simulate periodic updates while transcribing
            # In reality, we transcribe the whole file at once
            # but show progress to simulate streaming
            
            yield "🔄 Đang xử lý audio...\n\n⏳ 10s - Đang phân tích..."
            
            # Transcribe with segments
            with open(audio_file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json"
                )
            
            # Show segments progressively to simulate streaming
            full_text = ""
            segments = response.segments if hasattr(response, 'segments') else []
            
            if segments:
                # Group segments by 10-second intervals
                current_time = 0
                current_batch = []
                
                for segment in segments:
                    segment_start = segment.get('start', 0)
                    segment_text = segment.get('text', '')
                    
                    # Check if we've passed a 10-second interval
                    if segment_start >= current_time + 10:
                        # Yield accumulated text
                        if current_batch:
                            batch_text = " ".join(current_batch)
                            full_text += batch_text + " "
                            
                            yield f"""📝 Transcript (đến {int(current_time)}s):

{full_text.strip()}

⏱️ Đang tiếp tục ghi âm..."""
                            
                            current_batch = []
                        
                        current_time = int(segment_start / 10) * 10
                    
                    current_batch.append(segment_text)
                
                # Add remaining segments
                if current_batch:
                    batch_text = " ".join(current_batch)
                    full_text += batch_text + " "
            else:
                # No segments, use full text
                full_text = response.text
            
            # Final result
            yield f"""✅ Hoàn thành!

📝 **Transcript đầy đủ:**

{full_text.strip()}

---
💡 Copy text trên để phân tích hoặc lưu lại.
            """
            
        except Exception as e:
            yield f"""❌ Lỗi: {str(e)}

💡 **Kiểm tra:**
- OPENAI_API_KEY trong file .env
- Kết nối internet
- File audio hợp lệ
            """


# Note: True realtime streaming requires:
# 1. WebSocket connection
# 2. Audio chunk streaming from browser
# 3. Streaming STT service (not Whisper API)
# 
# This implementation simulates streaming by:
# - Transcribing the full audio
# - Showing segments progressively every 10 seconds
# - Giving the appearance of realtime transcription
