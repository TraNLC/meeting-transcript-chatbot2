"""Test Meeting Types Processing - Workshop, Brainstorming, Regular Meeting.

Test với các transcript files có sẵn để verify output khác nhau.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.ui.gradio_app_final import process_file
from src.rag.meeting_types import (
    MeetingTypeDetector,
    WorkshopFunctions,
    BrainstormingFunctions
)

print("=" * 80)
print("MEETING TYPES PROCESSING TEST")
print("=" * 80)
print()

# Test cases with expected outputs
test_cases = [
    {
        'file': 'data/transcripts/meeting_regular.txt',
        'type': 'meeting',
        'language': 'vi',
        'description': 'Regular Meeting - Product Development',
        'expected_sections': ['summary', 'topics', 'actions', 'decisions']
    },
    {
        'file': 'data/transcripts/workshop_training.txt',
        'type': 'workshop',
        'language': 'vi',
        'description': 'Workshop - React Hooks Training',
        'expected_sections': ['summary', 'topics', 'key_learnings', 'exercises', 'qa_pairs']
    },
    {
        'file': 'data/transcripts/brainstorming_session.txt',
        'type': 'brainstorming',
        'language': 'vi',
        'description': 'Brainstorming - E-commerce Features',
        'expected_sections': ['summary', 'ideas', 'categorized_ideas', 'concerns']
    }
]

passed = 0
failed = 0

print("📋 Test Cases:")
for i, tc in enumerate(test_cases, 1):
    file_path = Path(tc['file'])
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"  {i}. {file_path.name} ({size_kb:.1f} KB)")
        print(f"     Type: {tc['type']} | Language: {tc['language']}")
        print(f"     Description: {tc['description']}")
    else:
        print(f"  {i}. {file_path.name} - ❌ NOT FOUND")

print()
print("=" * 80)
print()

# ============================================================================
# Test 1: Meeting Type Detection
# ============================================================================
print("🧪 TEST 1: Meeting Type Auto-Detection")
print("-" * 80)

for i, tc in enumerate(test_cases, 1):
    file_path = Path(tc['file'])
    
    if not file_path.exists():
        print(f"  {i}. {file_path.name} - ❌ SKIP (file not found)")
        failed += 1
        continue
    
    try:
        # Read transcript
        transcript = file_path.read_text(encoding='utf-8')
        
        # Detect meeting type
        detected_type = MeetingTypeDetector.detect(transcript)
        
        expected_type = tc['type']
        
        if detected_type.value == expected_type:
            print(f"  ✓ {i}. {file_path.name}")
            print(f"     Detected: {detected_type.value} (Expected: {expected_type})")
            passed += 1
        else:
            print(f"  ✗ {i}. {file_path.name}")
            print(f"     Detected: {detected_type.value} (Expected: {expected_type})")
            failed += 1
            
    except Exception as e:
        print(f"  ✗ {i}. {file_path.name} - ERROR: {e}")
        failed += 1

print()

# ============================================================================
# Test 2: Workshop-Specific Extraction
# ============================================================================
print("🧪 TEST 2: Workshop-Specific Data Extraction")
print("-" * 80)

workshop_file = Path('data/transcripts/workshop_training.txt')

if workshop_file.exists():
    try:
        transcript = workshop_file.read_text(encoding='utf-8')
        
        # Extract key learnings
        learnings = WorkshopFunctions.extract_key_learnings(transcript)
        print(f"  ✓ Key Learnings: {len(learnings.get('key_learnings', []))} found")
        if learnings.get('key_learnings'):
            for i, learning in enumerate(learnings['key_learnings'][:3], 1):
                print(f"     {i}. {learning[:80]}...")
        passed += 1
        
        print()
        
        # Extract exercises
        exercises = WorkshopFunctions.extract_exercises(transcript)
        print(f"  ✓ Exercises: {len(exercises.get('exercises', []))} found")
        if exercises.get('exercises'):
            for i, ex in enumerate(exercises['exercises'][:3], 1):
                print(f"     {i}. {ex.get('title', 'N/A')[:80]}")
        passed += 1
        
        print()
        
        # Extract Q&A
        qa_pairs = WorkshopFunctions.extract_qa_pairs(transcript)
        print(f"  ✓ Q&A Pairs: {len(qa_pairs.get('qa_pairs', []))} found")
        if qa_pairs.get('qa_pairs'):
            for i, qa in enumerate(qa_pairs['qa_pairs'][:2], 1):
                print(f"     Q{i}: {qa.get('question', 'N/A')[:60]}...")
                print(f"     A{i}: {qa.get('answer', 'N/A')[:60]}...")
        passed += 1
        
    except Exception as e:
        print(f"  ✗ Workshop extraction failed: {e}")
        failed += 3
else:
    print(f"  ✗ Workshop file not found")
    failed += 3

print()

# ============================================================================
# Test 3: Brainstorming-Specific Extraction
# ============================================================================
print("🧪 TEST 3: Brainstorming-Specific Data Extraction")
print("-" * 80)

brainstorm_file = Path('data/transcripts/brainstorming_session.txt')

if brainstorm_file.exists():
    try:
        transcript = brainstorm_file.read_text(encoding='utf-8')
        
        # Extract ideas
        ideas_result = BrainstormingFunctions.extract_ideas(transcript)
        ideas = ideas_result.get('ideas', [])
        print(f"  ✓ Ideas: {len(ideas)} found")
        if ideas:
            for i, idea in enumerate(ideas[:3], 1):
                print(f"     {i}. {idea.get('idea', 'N/A')[:80]}")
        passed += 1
        
        print()
        
        # Categorize ideas
        categorized = BrainstormingFunctions.categorize_ideas(ideas_result)
        categories = categorized.get('categorized_ideas', {})
        print(f"  ✓ Categorized Ideas: {len(categories)} categories")
        for category, cat_ideas in categories.items():
            if cat_ideas:
                print(f"     {category}: {len(cat_ideas)} ideas")
        passed += 1
        
        print()
        
        # Extract concerns
        concerns = BrainstormingFunctions.extract_concerns(transcript)
        print(f"  ✓ Concerns: {len(concerns.get('concerns', []))} found")
        if concerns.get('concerns'):
            for i, concern in enumerate(concerns['concerns'][:3], 1):
                print(f"     {i}. {concern[:80]}...")
        passed += 1
        
    except Exception as e:
        print(f"  ✗ Brainstorming extraction failed: {e}")
        failed += 3
else:
    print(f"  ✗ Brainstorming file not found")
    failed += 3

print()

# ============================================================================
# Test 4: Full Processing Pipeline (requires API key)
# ============================================================================
print("🧪 TEST 4: Full Processing Pipeline")
print("-" * 80)
print("⚠️  Note: This test requires valid Gemini API key")
print()

# Check if API key is available
from src.config import Settings

if Settings.GEMINI_API_KEY and Settings.GEMINI_API_KEY != "your-gemini-api-key-here":
    print("  ✓ API key found - Running full pipeline tests")
    print()
    
    for i, tc in enumerate(test_cases, 1):
        file_path = Path(tc['file'])
        
        if not file_path.exists():
            print(f"  {i}. {file_path.name} - ❌ SKIP (file not found)")
            continue
        
        print(f"  🔄 Processing: {file_path.name} ({tc['type']})")
        
        try:
            # Create a mock file object
            class MockFile:
                def __init__(self, path):
                    self.name = str(path)
            
            mock_file = MockFile(file_path)
            
            # Process file
            status, summary, topics, actions, decisions = process_file(
                file=mock_file,
                meeting_type=tc['type'],
                output_language=tc['language']
            )
            
            # Check results
            if "✅" in status:
                print(f"     ✓ Status: {status[:60]}...")
                
                # Check summary
                if summary and len(summary) > 50:
                    print(f"     ✓ Summary: {len(summary)} chars")
                else:
                    print(f"     ⚠️  Summary: Too short ({len(summary)} chars)")
                
                # Check topics
                if topics and len(topics) > 20:
                    print(f"     ✓ Topics: {len(topics)} chars")
                    
                    # Check for specialized sections
                    if tc['type'] == 'workshop':
                        if 'Key Learnings' in topics or 'Exercises' in topics:
                            print(f"     ✓ Workshop-specific sections found")
                            passed += 1
                        else:
                            print(f"     ⚠️  Workshop sections missing")
                    elif tc['type'] == 'brainstorming':
                        if 'Ideas' in topics or 'Category' in topics:
                            print(f"     ✓ Brainstorming-specific sections found")
                            passed += 1
                        else:
                            print(f"     ⚠️  Brainstorming sections missing")
                    else:
                        passed += 1
                else:
                    print(f"     ⚠️  Topics: Too short ({len(topics)} chars)")
                
                # Check actions
                if actions and len(actions) > 20:
                    print(f"     ✓ Actions: {len(actions)} chars")
                else:
                    print(f"     ⚠️  Actions: {len(actions)} chars")
                
                passed += 1
                
            else:
                print(f"     ✗ Processing failed: {status}")
                failed += 1
                
        except Exception as e:
            print(f"     ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        
        print()
        
else:
    print("  ⚠️  API key not configured - Skipping full pipeline tests")
    print("     Set GEMINI_API_KEY in .env to run these tests")
    print()

# ============================================================================
# Test 5: Time Estimation for Audio Files
# ============================================================================
print("🧪 TEST 5: Audio File Time Estimation")
print("-" * 80)

try:
    import librosa
    import torch
    librosa_available = True
except ImportError:
    librosa_available = False

if librosa_available:
    try:
        from src.audio.huggingface_stt import transcribe_audio_huggingface
        
        # Check for sample audio files
        audio_samples = list(Path('data/recordings').glob('*.wav'))[:3]
        
        if audio_samples:
            print(f"  Found {len(audio_samples)} audio samples")
            print()
            
            for audio_file in audio_samples:
                print(f"  📁 {audio_file.name}")
                
                try:
                    # Get file info
                    file_size_mb = audio_file.stat().st_size / (1024 * 1024)
                    audio_data, sr = librosa.load(str(audio_file), sr=None)
                    duration_sec = len(audio_data) / sr
                    duration_min = duration_sec / 60
                    
                    # Estimate time
                    device = 0 if torch.cuda.is_available() else -1
                    device_name = "GPU" if device == 0 else "CPU"
                    
                    if device == 0:
                        est_time = duration_min / 5
                    else:
                        est_time = duration_min * 1.2
                    
                    print(f"     Size: {file_size_mb:.1f} MB")
                    print(f"     Duration: {duration_min:.1f} min")
                    print(f"     Device: {device_name}")
                    print(f"     Estimated time: {est_time:.1f} min")
                    
                    # Check warnings
                    if duration_min > 120:
                        print(f"     🚨 WARNING: Very long file!")
                    elif duration_min > 60:
                        print(f"     ⚠️  WARNING: Long file")
                    
                    if file_size_mb > 200:
                        print(f"     🚨 WARNING: Very large file!")
                    elif file_size_mb > 100:
                        print(f"     ⚠️  WARNING: Large file")
                    
                    print()
                    passed += 1
                    
                except Exception as e:
                    print(f"     ✗ Error analyzing: {e}")
                    failed += 1
                    print()
        else:
            print("  ⚠️  No audio samples found in data/recordings/")
            print()
            
    except ImportError as e:
        print(f"  ⚠️  Required libraries not installed: {e}")
        print("     Install: pip install librosa torch")
        print()
else:
    print("  ⚠️  librosa not installed - Skipping audio time estimation tests")
    print("     Install: pip install librosa")
    print("     Note: This is optional for meeting type processing")
    print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print()
print(f"Total Tests: {passed + failed}")
print(f"✓ Passed: {passed}")
print(f"✗ Failed: {failed}")
if passed + failed > 0:
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
print()

if failed > 0:
    print("⚠️  Some tests failed. Check output above for details.")
else:
    print("🎉 All tests passed!")

print()
print("=" * 80)

# Exit with appropriate code
sys.exit(0 if failed == 0 else 1)
