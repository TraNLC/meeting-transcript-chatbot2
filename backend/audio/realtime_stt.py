"""Realtime Speech-to-Text using streaming."""

import os
import queue
import threading
from typing import Optional, Callable
import time


class RealtimeSTT:
    """Realtime speech-to-text processor."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize realtime STT.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.transcript_callback = None
        
    def start_streaming(self, callback: Callable[[str], None], language: str = "vi"):
        """Start streaming transcription.
        
        Args:
            callback: Function to call with transcript updates
            language: Language code
        """
        self.is_recording = True
        self.transcript_callback = callback
        
        # Start processing thread
        thread = threading.Thread(
            target=self._process_stream,
            args=(language,),
            daemon=True
        )
        thread.start()
    
    def stop_streaming(self):
        """Stop streaming transcription."""
        self.is_recording = False
    
    def add_audio_chunk(self, audio_data):
        """Add audio chunk to processing queue.
        
        Args:
            audio_data: Audio data chunk
        """
        if self.is_recording:
            self.audio_queue.put(audio_data)
    
    def _process_stream(self, language: str):
        """Process audio stream (runs in background thread).
        
        Args:
            language: Language code
        """
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            buffer = []
            last_process_time = time.time()
            
            while self.is_recording:
                try:
                    # Get audio chunk with timeout
                    chunk = self.audio_queue.get(timeout=0.5)
                    buffer.append(chunk)
                    
                    # Process every 2 seconds or when buffer is large
                    current_time = time.time()
                    if current_time - last_process_time >= 2.0 or len(buffer) >= 10:
                        # Combine buffer chunks
                        audio_data = b''.join(buffer)
                        
                        # Transcribe chunk
                        # Note: This is simplified - real implementation needs proper audio handling
                        if self.transcript_callback and len(audio_data) > 0:
                            # Simulate transcription (replace with actual API call)
                            transcript = self._transcribe_chunk(audio_data, language, client)
                            if transcript:
                                self.transcript_callback(transcript)
                        
                        # Clear buffer
                        buffer = []
                        last_process_time = current_time
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error processing chunk: {e}")
                    
        except Exception as e:
            print(f"Error in stream processing: {e}")
    
    def _transcribe_chunk(self, audio_data, language: str, client):
        """Transcribe audio chunk.
        
        Args:
            audio_data: Audio data
            language: Language code
            client: OpenAI client
            
        Returns:
            Transcript text
        """
        try:
            # Save chunk to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_data)
                temp_path = f.name
            
            # Transcribe
            with open(temp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            # Cleanup
            os.unlink(temp_path)
            
            return transcript.text
            
        except Exception as e:
            print(f"Error transcribing chunk: {e}")
            return None


class SimpleRealtimeSTT:
    """Simplified realtime STT using periodic updates."""
    
    def __init__(self):
        """Initialize simple realtime STT."""
        self.current_transcript = ""
        self.is_active = False
    
    def process_audio_file(self, audio_file_path: str, language: str = "vi"):
        """Process audio file and yield transcript updates.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Yields:
            Transcript updates
        """
        try:
            from openai import OpenAI
            import os
            
            # Initialize client with custom base URL if provided
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")
            
            if base_url:
                client = OpenAI(api_key=api_key, base_url=base_url)
            else:
                client = OpenAI(api_key=api_key)
            
            # Show processing message
            yield "🔄 Đang xử lý audio...\n"
            
            # Transcribe with timestamps
            with open(audio_file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json"
                )
            
            # Simulate realtime by yielding segments
            full_text = ""
            segments = response.segments if hasattr(response, 'segments') else []
            
            if segments:
                for segment in segments:
                    text = segment.get('text', '')
                    full_text += text + " "
                    
                    # Yield progressive transcript
                    yield f"📝 Transcript:\n\n{full_text.strip()}\n\n⏱️ {segment.get('start', 0):.1f}s"
                    
                    # Small delay to simulate realtime
                    import time
                    time.sleep(0.1)
            else:
                # No segments, return full text
                full_text = response.text
                yield f"📝 Transcript:\n\n{full_text}"
            
            # Final result
            yield f"""✅ Hoàn thành!

📝 **Transcript đầy đủ:**

{full_text.strip()}

---
💡 Copy text trên để phân tích hoặc lưu lại.
            """
            
        except Exception as e:
            yield f"❌ Lỗi: {str(e)}\n\n💡 Kiểm tra OPENAI_API_KEY trong file .env"
