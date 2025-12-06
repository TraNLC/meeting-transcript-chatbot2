"""Test script for speaker diarization functionality.

Usage:
    python scripts/test_speaker_diarization.py <audio_file>
    
Example:
    python scripts/test_speaker_diarization.py data/recordings/meeting_001.wav
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from src.audio.speaker_diarization import (
    SpeakerDiarizer,
    diarize_audio_with_progress,
    transcribe_with_speakers
)


def test_diarization_only(audio_file: str):
    """Test speaker diarization only."""
    print("=" * 60)
    print("TEST 1: Speaker Diarization Only")
    print("=" * 60)
    
    for message in diarize_audio_with_progress(audio_file):
        print(message)
        print()


def test_transcription_with_speakers(audio_file: str, language: str = "vi"):
    """Test transcription with speaker labels."""
    print("=" * 60)
    print("TEST 2: Transcription with Speaker Labels")
    print("=" * 60)
    
    for message in transcribe_with_speakers(audio_file, language):
        print(message)
        print()


def test_manual_diarization(audio_file: str):
    """Test manual diarization API."""
    print("=" * 60)
    print("TEST 3: Manual Diarization API")
    print("=" * 60)
    
    try:
        diarizer = SpeakerDiarizer()
        
        print("Loading pipeline...")
        diarizer.load_pipeline()
        print("✅ Pipeline loaded\n")
        
        print("Analyzing audio...")
        segments = diarizer.diarize_audio(audio_file)
        print(f"✅ Found {len(segments)} segments\n")
        
        # Show first 10 segments
        print("First 10 segments:")
        for seg in segments[:10]:
            start_min = int(seg["start"] // 60)
            start_sec = int(seg["start"] % 60)
            end_min = int(seg["end"] // 60)
            end_sec = int(seg["end"] % 60)
            
            time_str = f"{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}"
            speaker = seg["speaker"].replace("SPEAKER_", "Guest-")
            
            print(f"  {time_str}: {speaker}")
        
        if len(segments) > 10:
            print(f"  ... and {len(segments) - 10} more segments")
        
        # Count speakers
        speakers = set(seg["speaker"] for seg in segments)
        print(f"\n✅ Total speakers detected: {len(speakers)}")
        print(f"   Speakers: {', '.join(sorted([s.replace('SPEAKER_', 'Guest-') for s in speakers]))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main test function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_speaker_diarization.py <audio_file>")
        print("\nExample:")
        print("  python scripts/test_speaker_diarization.py data/recordings/meeting_001.wav")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"❌ Error: File not found: {audio_file}")
        sys.exit(1)
    
    print(f"Testing speaker diarization on: {audio_file}\n")
    
    # Check HuggingFace token
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("⚠️  Warning: HUGGINGFACE_TOKEN not found in .env")
        print("\n💡 Setup Instructions:")
        print("1. Get token from: https://huggingface.co/settings/tokens")
        print("2. Accept terms at: https://huggingface.co/pyannote/speaker-diarization-3.1")
        print("3. Add to .env: HUGGINGFACE_TOKEN=your_token_here\n")
        sys.exit(1)
    
    print(f"✅ HuggingFace token found: {hf_token[:10]}...\n")
    
    # Run tests
    try:
        # Test 1: Diarization only
        test_diarization_only(audio_file)
        
        print("\n" + "=" * 60 + "\n")
        
        # Test 2: Transcription with speakers (optional - takes longer)
        response = input("Run transcription with speakers test? (y/n): ")
        if response.lower() == 'y':
            language = input("Language code (vi/en/ja/ko/zh) [default: vi]: ").strip() or "vi"
            test_transcription_with_speakers(audio_file, language)
        
        print("\n" + "=" * 60 + "\n")
        
        # Test 3: Manual API
        test_manual_diarization(audio_file)
        
        print("\n✅ All tests completed!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
