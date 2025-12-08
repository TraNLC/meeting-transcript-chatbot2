"""Realtime Speech-to-Text using Vosk (Free & Offline)."""

import os
import json
import wave
from pathlib import Path
from typing import Optional, Generator


class VoskRealtimeSTT:
    """Realtime STT using Vosk - Free, offline, lightweight."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize Vosk STT.
        
        Args:
            model_path: Path to Vosk model directory
        """
        self.model_path = model_path or self._get_default_model_path()
        self.model = None
        
    def _get_default_model_path(self) -> str:
        """Get default model path."""
        return "models/vosk-model-small-vi-0.4"  # Vietnamese small model
    
    def _ensure_model_downloaded(self, language: str = "vi"):
        """Ensure Vosk model is downloaded.
        
        Args:
            language: Language code
        """
        model_dir = Path(self.model_path)
        
        if model_dir.exists():
            return str(model_dir)
        
        # Download model if not exists
        print(f"📥 Downloading Vosk model for {language}...")
        
        model_urls = {
            "vi": "https://alphacephei.com/vosk/models/vosk-model-small-vi-0.4.zip",
            "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
            "ja": "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip",
            "ko": "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip"
        }
        
        url = model_urls.get(language, model_urls["en"])
        
        # Download and extract
        import urllib.request
        import zipfile
        
        model_dir.parent.mkdir(parents=True, exist_ok=True)
        zip_path = model_dir.parent / "model.zip"
        
        print(f"Downloading from {url}...")
        try:
            urllib.request.urlretrieve(url, zip_path)
            
            print("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_dir.parent)
            
            zip_path.unlink()
            print("✅ Model downloaded!")
            
            return str(model_dir)
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            print(f"💡 Please download manually from: {url}")
            print(f"   Extract to: {model_dir.parent}")
            raise Exception(f"Cannot download Vosk model. Please use Whisper instead or download manually.")
    
    def transcribe_realtime(
        self,
        audio_file_path: str,
        language: str = "vi",
        chunk_duration: int = 10
    ) -> Generator[str, None, None]:
        """Transcribe audio file with realtime-like updates.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            chunk_duration: Seconds per update
            
        Yields:
            Progressive transcript updates
        """
        try:
            from vosk import Model, KaldiRecognizer
            import wave
            
            # Ensure model is available
            model_path = self._ensure_model_downloaded(language)
            
            # Load model
            yield "📥 Loading Vosk model..."
            if self.model is None:
                self.model = Model(model_path)
            
            # Open audio file
            wf = wave.open(audio_file_path, "rb")
            
            # Check format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
                yield "❌ Audio format not supported. Need: mono, 16-bit PCM, 8-48kHz"
                return
            
            # Create recognizer
            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)
            
            # Process audio in chunks
            full_transcript = ""
            chunk_size = int(wf.getframerate() * chunk_duration)  # 10 seconds
            chunk_count = 0
            
            yield "🎙️ Bắt đầu transcribe realtime...\n"
            
            while True:
                data = wf.readframes(chunk_size)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get('text', '')
                    
                    if text:
                        full_transcript += text + " "
                        chunk_count += 1
                        
                        # Yield progressive update
                        yield f"""📝 Transcript (đến {chunk_count * chunk_duration}s):

{full_transcript.strip()}

⏱️ Đang tiếp tục..."""
            
            # Final result
            final_result = json.loads(rec.FinalResult())
            final_text = final_result.get('text', '')
            
            if final_text:
                full_transcript += final_text
            
            yield f"""✅ Hoàn thành!

📝 **Transcript đầy đủ:**

{full_transcript.strip()}

---
💡 Transcribed bằng Vosk (Miễn phí, Offline)
            """
            
            wf.close()
            
        except ImportError:
            yield """❌ Vosk chưa được cài đặt!

**Cài đặt:**
```
pip install vosk soundfile
```

Sau đó restart app.
            """
        except Exception as e:
            yield f"""❌ Lỗi: {str(e)}

💡 **Kiểm tra:**
- File audio hợp lệ (WAV format)
- Model đã được download
- Vosk đã được cài đặt
            """
    
    def transcribe_simple(self, audio_file_path: str, language: str = "vi") -> str:
        """Simple transcription without streaming.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Returns:
            Full transcript
        """
        try:
            from vosk import Model, KaldiRecognizer
            import wave
            
            # Ensure model
            model_path = self._ensure_model_downloaded(language)
            
            if self.model is None:
                self.model = Model(model_path)
            
            wf = wave.open(audio_file_path, "rb")
            rec = KaldiRecognizer(self.model, wf.getframerate())
            
            transcript = ""
            
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    transcript += result.get('text', '') + " "
            
            final_result = json.loads(rec.FinalResult())
            transcript += final_result.get('text', '')
            
            wf.close()
            
            return transcript.strip()
            
        except Exception as e:
            return f"Error: {str(e)}"


# Model download info
VOSK_MODELS = {
    "vi": {
        "name": "Vietnamese Small",
        "size": "75MB",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-vi-0.4.zip"
    },
    "en": {
        "name": "English Small",
        "size": "40MB",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    },
    "ja": {
        "name": "Japanese Small",
        "size": "48MB",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip"
    },
    "ko": {
        "name": "Korean Small",
        "size": "42MB",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip"
    }
}
