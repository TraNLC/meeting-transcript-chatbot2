
import os
import sys
from pathlib import Path

# Add project root to path to verify src imports work
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.audio.huggingface_stt import transcribe_audio_huggingface
from backend.audio.speaker_diarization import SpeakerDiarizer

class AudioService:
    _instance = None
    _whisper_model = None
    _diarizer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioService, cls).__new__(cls)
        return cls._instance

    @property
    def whisper_model(self):
        if self._whisper_model is None:
            try:
                from faster_whisper import WhisperModel
                print("Loading faster-whisper model (base)...")
                self._whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
                print("[OK] faster-whisper model loaded!")
            except Exception as e:
                print(f"[ERROR] Error loading faster-whisper: {e}")
                self._whisper_model = None
        return self._whisper_model

    @property
    def diarizer(self):
        if self._diarizer is None:
            try:
                # Assuming SpeakerDiarizer is lightweight to init, pipeline load is heavy
                # We will instantiate it. The class itself handles lazy loading of pipeline?
                # Looking at src/audio/speaker_diarization.py, load_pipeline() does the work.
                self._diarizer = SpeakerDiarizer()
                # Pre-load?
                # self._diarizer.load_pipeline() 
            except Exception as e:
                print(f"[ERROR] Error loading diarizer: {e}")
                self._diarizer = None
        return self._diarizer

    def transcribe_realtime(self, audio_path, language='vi'):
        """Wrapper for realtime transcription logic"""
        model = self.whisper_model
        if not model:
            raise RuntimeError("Whisper model not available")
            
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=1,
            vad_filter=True,
            condition_on_previous_text=False,
            # Anti-hallucination settings
            temperature=0.0,
            compression_ratio_threshold=2.4,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.6,
            initial_prompt=None
        )
        return list(segments)

    def diarize(self, audio_path):
        """Wrapper for diarization"""
        diarizer = self.diarizer
        if not diarizer:
            return []
        try:
            return diarizer.diarize_audio(audio_path)
        except Exception as e:
            print(f"Diarization failed: {e}")
            return []

audio_service = AudioService()
