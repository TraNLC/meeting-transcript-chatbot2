"""Audio recording and processing module."""

from .audio_manager import AudioManager
from .speaker_diarization import (
    SpeakerDiarizer,
    diarize_audio_with_progress,
    transcribe_with_speakers
)

__all__ = [
    'AudioManager',
    'SpeakerDiarizer',
    'diarize_audio_with_progress',
    'transcribe_with_speakers'
]
