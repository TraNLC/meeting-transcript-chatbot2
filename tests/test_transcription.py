"""Test HuggingFace Speech-to-Text Transcription.

Test với các audio files có sẵn.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.audio.huggingface_stt import transcribe_audio_huggingface

print("=" * 70)
print("HUGGINGFACE WHISPER TRANSCRIPTION TEST")
print("=" * 70)
print()

# Test files
audio_files = [
    "data/recordings/20251127_023126.wav",
    "data/recordings/20251127_023208.wav",
    "data/recordings/output_audio_4_eng.wav"
]

# Test languages
test_cases = [
    ("data/recordings/20251127_023126.wav", "vi", "Vietnamese audio"),
    ("data/recordings/20251127_023208.wav", "vi", "Vietnamese audio"),
    ("data/recordings/output_audio_4_eng.wav", "en", "English audio")
]

print("📋 Test Cases:")
for i, (file, lang, desc) in enumerate(test_cases, 1):
    file_path = Path(file)
    if file_path.exists():
        size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"  {i}. {file_path.name} ({size_mb:.2f} MB) - {desc} [{lang}]")
    else:
        print(f"  {i}. {file_path.name} - ❌ NOT FOUND")

print()
print("=" * 70)
print()

# Run tests
for i, (audio_file, language, description) in enumerate(test_cases, 1):
    print(f"🧪 Test {i}/{len(test_cases)}: {description}")
    print(f"   File: {Path(audio_file).name}")
    print(f"   Language: {language}")
    print("-" * 70)
    
    if not Path(audio_file).exists():
        print(f"   ❌ SKIP: File not found")
        print()
        continue
    
    try:
        # Transcribe (generator function)
        print("   🔄 Transcribing...")
        
        for progress in transcribe_audio_huggingface(audio_file, language):
            # Print progress updates
            if "🔄" in progress or "⚙️" in progress or "📥" in progress or "🎤" in progress:
                print(f"   {progress}")
            elif "📝" in progress:
                # Final result
                print()
                print("   ✅ RESULT:")
                print("-" * 70)
                print(progress)
                print("-" * 70)
        
        print(f"   ✅ Test {i} PASSED")
        
    except Exception as e:
        print(f"   ❌ Test {i} FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print()

print()
print("🎉 All tests completed!")
print()
print("💡 Tips:")
print("  - First run will download Whisper model (~1.5GB)")
print("  - Subsequent runs will be faster (model cached)")
print("  - Medium model provides high accuracy")
print("  - Supports 50+ languages")
print()
