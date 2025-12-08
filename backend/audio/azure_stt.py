"""Azure Speech-to-Text Service."""

import os
import azure.cognitiveservices.speech as speechsdk
from typing import Generator


class AzureSpeechSTT:
    """Azure Speech Service for Speech-to-Text."""
    
    def __init__(self):
        """Initialize Azure Speech Service."""
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        
        if not self.speech_key:
            raise ValueError("AZURE_SPEECH_KEY not found in environment variables")
    
    def transcribe_audio(self, audio_file_path: str, language: str = "vi-VN") -> Generator[str, None, None]:
        """Transcribe audio file with progress updates.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (vi-VN, en-US, ja-JP, ko-KR)
            
        Yields:
            Progress updates and transcript
        """
        try:
            # Map language codes
            language_map = {
                "vi": "vi-VN",
                "en": "en-US",
                "ja": "ja-JP",
                "ko": "ko-KR"
            }
            speech_language = language_map.get(language, language)
            
            yield f"🎙️ Đang khởi động Azure Speech Service...\n\nNgôn ngữ: {speech_language}"
            
            # Configure speech service
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            speech_config.speech_recognition_language = speech_language
            
            # Configure audio input
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
            
            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            yield "🔄 Đang xử lý audio...\n\n⏳ Vui lòng đợi..."
            
            # Recognize speech
            full_transcript = []
            done = False
            
            def recognized_cb(evt):
                """Callback for recognized speech."""
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    full_transcript.append(evt.result.text)
            
            def canceled_cb(evt):
                """Callback for canceled recognition."""
                nonlocal done
                done = True
            
            def stopped_cb(evt):
                """Callback for stopped recognition."""
                nonlocal done
                done = True
            
            # Connect callbacks
            speech_recognizer.recognized.connect(recognized_cb)
            speech_recognizer.canceled.connect(canceled_cb)
            speech_recognizer.session_stopped.connect(stopped_cb)
            
            # Start continuous recognition
            speech_recognizer.start_continuous_recognition()
            
            # Wait for completion
            import time
            elapsed = 0
            while not done and elapsed < 300:  # Max 5 minutes
                time.sleep(1)
                elapsed += 1
                
                # Yield progress every 10 seconds
                if elapsed % 10 == 0 and full_transcript:
                    current_text = " ".join(full_transcript)
                    yield f"""📝 Transcript (đang xử lý... {elapsed}s):

{current_text}

⏱️ Đang tiếp tục..."""
            
            # Stop recognition
            speech_recognizer.stop_continuous_recognition()
            
            # Final result
            final_text = " ".join(full_transcript)
            
            if final_text:
                yield f"""✅ Hoàn thành!

📝 **Transcript đầy đủ:**

{final_text.strip()}

---
💡 Transcribed bằng Azure Speech Service
                """
            else:
                yield "⚠️ Không phát hiện được giọng nói trong audio. Vui lòng thử lại."
                
        except Exception as e:
            yield f"""❌ Lỗi Azure Speech: {str(e)}

💡 **Kiểm tra:**
- AZURE_SPEECH_KEY trong file .env
- AZURE_SPEECH_REGION (mặc định: eastus)
- File audio hợp lệ
- Kết nối internet

**Cài đặt:**
```bash
pip install azure-cognitiveservices-speech
```
            """
    
    def transcribe_simple(self, audio_file_path: str, language: str = "vi-VN") -> str:
        """Simple transcription without streaming.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Returns:
            Full transcript
        """
        try:
            language_map = {
                "vi": "vi-VN",
                "en": "en-US",
                "ja": "ja-JP",
                "ko": "ko-KR"
            }
            speech_language = language_map.get(language, language)
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            speech_config.speech_recognition_language = speech_language
            
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return "Không phát hiện được giọng nói"
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                return f"Lỗi: {cancellation.reason}"
            else:
                return "Lỗi không xác định"
                
        except Exception as e:
            return f"Lỗi: {str(e)}"
