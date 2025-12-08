"""Speaker Diarization using pyannote.audio.

Identifies and labels different speakers in audio recordings.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class SpeakerDiarizer:
    """Handle speaker diarization using pyannote.audio."""
    
    def __init__(self, hf_token: Optional[str] = None):
        """Initialize speaker diarizer.
        
        Args:
            hf_token: HuggingFace token for accessing pyannote models
        """
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_TOKEN")
        self.pipeline = None
        
    def load_pipeline(self):
        """Load pyannote speaker diarization pipeline."""
        if self.pipeline is not None:
            return self.pipeline
            
        try:
            from pyannote.audio import Pipeline
            
            if not self.hf_token:
                raise ValueError(
                    "HuggingFace token required. "
                    "Get token from: https://huggingface.co/settings/tokens\n"
                    "Accept terms at: https://huggingface.co/pyannote/speaker-diarization-3.1"
                )
            
            # Load speaker diarization pipeline
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token
            )
            
            # Use GPU if available
            import torch
            if torch.cuda.is_available():
                self.pipeline = self.pipeline.to(torch.device("cuda"))
                
            return self.pipeline
            
        except Exception as e:
            raise RuntimeError(f"Failed to load diarization pipeline: {e}")
    
    def diarize_audio(self, audio_file: str) -> List[Dict]:
        """Perform speaker diarization on audio file.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            List of diarization segments with speaker labels
            Format: [{"start": 0.0, "end": 5.2, "speaker": "SPEAKER_00"}, ...]
        """
        pipeline = self.load_pipeline()
        
        # Run diarization
        diarization = pipeline(audio_file)
        
        # Extract segments
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
        
        return segments
    
    def format_diarization(self, segments: List[Dict]) -> str:
        """Format diarization results as readable text.
        
        Args:
            segments: List of diarization segments
            
        Returns:
            Formatted string with speaker timeline
        """
        if not segments:
            return "No speakers detected"
        
        lines = ["🎤 **Speaker Timeline:**\n"]
        
        for seg in segments:
            start_min = int(seg["start"] // 60)
            start_sec = int(seg["start"] % 60)
            end_min = int(seg["end"] // 60)
            end_sec = int(seg["end"] % 60)
            
            time_str = f"{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"
            speaker = seg["speaker"].replace("SPEAKER_", "Guest-")
            
            lines.append(f"{time_str}: {speaker}")
        
        return "\n".join(lines)
    
    def merge_with_transcript(
        self, 
        transcript_chunks: List[Dict],
        diarization_segments: List[Dict]
    ) -> str:
        """Merge transcript with speaker labels.
        
        Args:
            transcript_chunks: List of transcript chunks with timestamps
                Format: [{"timestamp": (start, end), "text": "..."}, ...]
            diarization_segments: List of diarization segments
                Format: [{"start": 0.0, "end": 5.2, "speaker": "SPEAKER_00"}, ...]
                
        Returns:
            Formatted transcript with speaker labels
        """
        if not transcript_chunks or not diarization_segments:
            return ""
        
        lines = ["📝 **Transcript with Speakers:**\n"]
        
        for chunk in transcript_chunks:
            timestamp = chunk.get("timestamp", (0, 0))
            text = chunk.get("text", "").strip()
            
            if not text:
                continue
            
            # Find speaker for this chunk
            chunk_start = timestamp[0] if timestamp[0] is not None else 0
            chunk_end = timestamp[1] if timestamp[1] is not None else chunk_start
            chunk_mid = (chunk_start + chunk_end) / 2
            
            # Find overlapping speaker
            speaker = "Unknown"
            for seg in diarization_segments:
                if seg["start"] <= chunk_mid <= seg["end"]:
                    speaker = seg["speaker"].replace("SPEAKER_", "Guest-")
                    break
            
            # Format timestamp
            minutes = int(chunk_start // 60)
            seconds = int(chunk_start % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            
            lines.append(f"[{time_str}] **{speaker}**: {text}")
        
        return "\n".join(lines)


def diarize_audio_with_progress(audio_file: str, hf_token: Optional[str] = None):
    """Diarize audio with progress updates (generator).
    
    Args:
        audio_file: Path to audio file
        hf_token: HuggingFace token
        
    Yields:
        str: Progress messages and results
    """
    if not audio_file or audio_file == "":
        yield "🎙️ No audio file provided"
        return
    
    try:
        yield "🔄 Initializing speaker diarization..."
        
        diarizer = SpeakerDiarizer(hf_token)
        
        yield "📥 Loading pyannote.audio model..."
        diarizer.load_pipeline()
        
        yield "🎤 Analyzing speakers in audio..."
        segments = diarizer.diarize_audio(audio_file)
        
        # Count unique speakers
        speakers = set(seg["speaker"] for seg in segments)
        num_speakers = len(speakers)
        
        yield f"✅ Detected {num_speakers} speaker(s)\n"
        
        # Format results
        formatted = diarizer.format_diarization(segments)
        yield formatted
        
    except ValueError as e:
        yield f"""❌ Configuration Error: {str(e)}

💡 **Setup Instructions:**

1. Get HuggingFace token:
   - Visit: https://huggingface.co/settings/tokens
   - Create a new token (read access)

2. Accept model terms:
   - Visit: https://huggingface.co/pyannote/speaker-diarization-3.1
   - Click "Agree and access repository"

3. Add token to .env file:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   ```

4. Install dependencies:
   ```bash
   pip install pyannote.audio speechbrain
   ```
"""
    except ImportError as e:
        yield f"""❌ Missing Dependencies: {str(e)}

💡 **Install speaker diarization:**

```bash
pip install pyannote.audio speechbrain
```

**Features:**
- ✅ Identify multiple speakers
- ✅ Label as Guest-1, Guest-2, etc.
- ✅ Timestamp each speaker segment
- ✅ Works with any language
"""
    except Exception as e:
        yield f"""❌ Diarization Error: {str(e)}

💡 **Troubleshooting:**
- Check audio file is valid
- Ensure HuggingFace token is correct
- Verify model access permissions
- Check internet connection (first run downloads model)
"""


def transcribe_with_speakers(
    audio_file: str,
    language: str = "vi",
    hf_token: Optional[str] = None
):
    """Transcribe audio with speaker diarization (generator).
    
    Combines Whisper transcription with pyannote speaker diarization.
    
    Args:
        audio_file: Path to audio file
        language: Language code for transcription
        hf_token: HuggingFace token for diarization
        
    Yields:
        str: Progress messages and final transcript with speakers
    """
    if not audio_file or audio_file == "":
        yield "🎙️ No audio file provided"
        return
    
    try:
        from transformers import pipeline as hf_pipeline
        import torch
        
        yield "🔄 Step 1/2: Transcribing audio with Whisper..."
        
        # Transcribe with Whisper
        device = 0 if torch.cuda.is_available() else -1
        whisper = hf_pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            device=device,
            return_timestamps=True,
            torch_dtype=torch.float16 if device == 0 else torch.float32
        )
        
        result = whisper(
            audio_file,
            generate_kwargs={
                "language": language,
                "task": "transcribe"
            },
            return_timestamps=True
        )
        
        transcript_chunks = result.get("chunks", [])
        
        yield f"✅ Transcription complete ({len(transcript_chunks)} chunks)\n"
        
        yield "🔄 Step 2/2: Identifying speakers..."
        
        # Diarize speakers
        diarizer = SpeakerDiarizer(hf_token)
        diarizer.load_pipeline()
        
        segments = diarizer.diarize_audio(audio_file)
        speakers = set(seg["speaker"] for seg in segments)
        
        yield f"✅ Detected {len(speakers)} speaker(s)\n"
        
        # Merge transcript with speakers
        merged = diarizer.merge_with_transcript(transcript_chunks, segments)
        
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        yield f"""📝 **Complete Transcript with Speakers** - {now}

{merged}

---
💡 Speakers: {', '.join(sorted([s.replace('SPEAKER_', 'Guest-') for s in speakers]))}
"""
        
    except Exception as e:
        yield f"❌ Error: {str(e)}"
