"""Text-to-Speech processor using HuggingFace TTS."""

import os
from pathlib import Path
from typing import Optional
from datetime import datetime


class TTSProcessor:
    """Text-to-Speech processor using Coqui TTS."""
    
    def __init__(self, output_dir: str = "data/tts_output"):
        """Initialize TTS processor.
        
        Args:
            output_dir: Directory to save generated audio
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tts = None
    
    def _init_tts(self):
        """Lazy initialization of TTS model."""
        if self.tts is None:
            try:
                from TTS.api import TTS
                # Use multilingual model
                self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            except ImportError:
                raise ImportError("TTS not installed. Run: pip install TTS")
    
    def text_to_speech(
        self,
        text: str,
        language: str = "en",
        speaker: Optional[str] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """Convert text to speech.
        
        Args:
            text: Text to convert
            language: Language code (en, vi, ja, ko, zh-cn, etc.)
            speaker: Speaker voice (optional)
            output_filename: Custom output filename
            
        Returns:
            Path to generated audio file
        """
        self._init_tts()
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"tts_{timestamp}.wav"
        
        output_path = self.output_dir / output_filename
        
        # Generate speech
        self.tts.tts_to_file(
            text=text,
            language=language,
            file_path=str(output_path)
        )
        
        return str(output_path)
    
    def text_to_speech_with_reference(
        self,
        text: str,
        reference_audio: str,
        language: str = "en",
        output_filename: Optional[str] = None
    ) -> str:
        """Convert text to speech with reference voice.
        
        Args:
            text: Text to convert
            reference_audio: Path to reference audio for voice cloning
            language: Language code
            output_filename: Custom output filename
            
        Returns:
            Path to generated audio file
        """
        self._init_tts()
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"tts_cloned_{timestamp}.wav"
        
        output_path = self.output_dir / output_filename
        
        # Generate speech with voice cloning
        self.tts.tts_to_file(
            text=text,
            language=language,
            speaker_wav=reference_audio,
            file_path=str(output_path)
        )
        
        return str(output_path)
    
    def get_available_languages(self) -> list:
        """Get list of supported languages.
        
        Returns:
            List of language codes
        """
        # XTTS v2 supports these languages
        return [
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "it",  # Italian
            "pt",  # Portuguese
            "pl",  # Polish
            "tr",  # Turkish
            "ru",  # Russian
            "nl",  # Dutch
            "cs",  # Czech
            "ar",  # Arabic
            "zh-cn",  # Chinese
            "ja",  # Japanese
            "ko",  # Korean
            "hu",  # Hungarian
            "hi"   # Hindi
        ]


class SimpleTTSProcessor:
    """Simple TTS using gTTS (Google Text-to-Speech) - Fallback option."""
    
    def __init__(self, output_dir: str = "data/tts_output"):
        """Initialize simple TTS processor.
        
        Args:
            output_dir: Directory to save generated audio
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def text_to_speech(
        self,
        text: str,
        language: str = "en",
        output_filename: Optional[str] = None
    ) -> str:
        """Convert text to speech using gTTS.
        
        Args:
            text: Text to convert
            language: Language code
            output_filename: Custom output filename
            
        Returns:
            Path to generated audio file
        """
        try:
            from gtts import gTTS
        except ImportError:
            raise ImportError("gTTS not installed. Run: pip install gtts")
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"tts_{timestamp}.mp3"
        
        output_path = self.output_dir / output_filename
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(str(output_path))
        
        return str(output_path)
    
    def get_available_languages(self) -> list:
        """Get list of supported languages.
        
        Returns:
            List of language codes
        """
        return [
            "en", "vi", "ja", "ko", "zh-CN", "es", "fr", "de",
            "it", "pt", "ru", "ar", "hi", "th", "id", "ms"
        ]
