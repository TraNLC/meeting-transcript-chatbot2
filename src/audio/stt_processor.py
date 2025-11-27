"""Speech-to-Text processor using OpenAI Whisper API."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import openai


class STTProcessor:
    """Process audio files to text using Whisper API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize STT processor.
        
        Args:
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
            base_url: Custom base URL (or use OPENAI_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        
        if self.api_key:
            openai.api_key = self.api_key
        if self.base_url:
            openai.api_base = self.base_url
    
    def transcribe_audio(
        self,
        audio_file_path: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe audio file to text.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (e.g., 'vi', 'en', 'ja')
            prompt: Optional prompt to guide transcription
            
        Returns:
            Dict with 'text', 'language', and 'duration'
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "OpenAI API key not configured",
                    "text": ""
                }
            
            # Check file exists
            if not os.path.exists(audio_file_path):
                return {
                    "success": False,
                    "error": f"File not found: {audio_file_path}",
                    "text": ""
                }
            
            # Open audio file
            with open(audio_file_path, "rb") as audio_file:
                # Call Whisper API
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    prompt=prompt,
                    response_format="verbose_json"
                )
            
            return {
                "success": True,
                "text": response.get("text", ""),
                "language": response.get("language", language),
                "duration": response.get("duration", 0),
                "segments": response.get("segments", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }
    
    def transcribe_with_timestamps(
        self,
        audio_file_path: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe with word-level timestamps.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Returns:
            Dict with transcription and timestamps
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "OpenAI API key not configured"
                }
            
            with open(audio_file_path, "rb") as audio_file:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"]
                )
            
            return {
                "success": True,
                "text": response.get("text", ""),
                "language": response.get("language", language),
                "duration": response.get("duration", 0),
                "words": response.get("words", []),
                "segments": response.get("segments", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_transcript(
        self,
        transcript: str,
        output_path: str
    ) -> bool:
        """Save transcript to file.
        
        Args:
            transcript: Transcript text
            output_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            
            return True
        except Exception as e:
            print(f"Error saving transcript: {e}")
            return False
