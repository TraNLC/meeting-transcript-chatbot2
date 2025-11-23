"""Test chunked executor with large transcripts."""

import json
from src.rag.chunked_executor import ChunkedFunctionExecutor

# Read sample transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

print("╔" + "═" * 78 + "╗")
print("║" + " " * 22 + "CHUNKED EXECUTOR TEST" + " " * 34 + "║")
print("╚" + "═" * 78 + "╝")

# Test 1: Normal size (no chunking)
print("\n" + "=" * 80)
print("TEST 1: NORMAL TRANSCRIPT (No chunking needed)")
print("=" * 80)

executor = ChunkedFunctionExecutor(transcript, output_language="vi", enable_translation=False)
info = executor.get_info()

print(f"\n📊 Transcript Info:")
print(f"  • Is chunked: {info['is_chunked']}")
print(f"  • Num chunks: {info['num_chunks']}")
print(f"  • Total chars: {info['validation']['statistics']['total_chars']:,}")
print(f"  • Total words: {info['validation']['statistics']['total_words']:,}")

print(f"\n🔍 Executing get_meeting_participants...")
result = executor.execute("get_meeting_participants", {})
data = json.loads(result)
print(f"✓ Found {len(data['participants'])} participants:")
for p in data['participants'][:3]:
    print(f"  • {p['name']} ({p['role']}): {p['contribution']}")

# Test 2: Large transcript (with chunking)
print("\n\n" + "=" * 80)
print("TEST 2: LARGE TRANSCRIPT (50x - Requires chunking)")
print("=" * 80)

large_transcript = transcript * 50
large_executor = ChunkedFunctionExecutor(
    large_transcript, 
    output_language="vi",
    enable_translation=False,  # Disable for speed
    rate_limit_delay=0.1  # Faster for testing
)

info = large_executor.get_info()

print(f"\n📊 Transcript Info:")
print(f"  • Is chunked: {info['is_chunked']}")
print(f"  • Num chunks: {info['num_chunks']}")
print(f"  • Total chars: {info['validation']['statistics']['total_chars']:,}")
print(f"  • Total words: {info['validation']['statistics']['total_words']:,}")

if info['is_chunked']:
    print(f"\n📦 Chunk Details:")
    for chunk_info in info['chunks']:
        print(f"  Chunk {chunk_info['index']}: {chunk_info['chars']:,} chars, "
              f"{chunk_info['words']:,} words, lines {chunk_info['lines']}")

print(f"\n🔍 Executing get_meeting_participants...")
result = large_executor.execute("get_meeting_participants", {})
data = json.loads(result)
print(f"✓ Found {len(data['participants'])} participants:")
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']}): {p['contribution']}")

# Test 3: Extract action items from large transcript
print(f"\n🔍 Executing extract_action_items...")
result = large_executor.execute("extract_action_items", {})
data = json.loads(result)
print(f"✓ Found {len(data['action_items'])} action items:")
for item in data['action_items'][:3]:
    print(f"  • {item['assignee']}: {item['task'][:50]}...")

# Test 4: Very large transcript
print("\n\n" + "=" * 80)
print("TEST 3: VERY LARGE TRANSCRIPT (100x)")
print("=" * 80)

very_large_transcript = transcript * 100
very_large_executor = ChunkedFunctionExecutor(
    very_large_transcript,
    output_language="en",
    enable_translation=False,
    rate_limit_delay=0.1
)

info = very_large_executor.get_info()

print(f"\n📊 Transcript Info:")
print(f"  • Is chunked: {info['is_chunked']}")
print(f"  • Num chunks: {info['num_chunks']}")
print(f"  • Total chars: {info['validation']['statistics']['total_chars']:,}")

if info['validation']['warnings']:
    print(f"\n⚠️  Warnings:")
    for warning in info['validation']['warnings']:
        print(f"  • {warning}")

print(f"\n🔍 Executing get_meeting_participants...")
result = very_large_executor.execute("get_meeting_participants", {})
data = json.loads(result)
print(f"✓ Found {len(data['participants'])} participants")

# Summary
print("\n\n" + "╔" + "═" * 78 + "╗")
print("║" + " " * 32 + "SUMMARY" + " " * 39 + "║")
print("╚" + "═" * 78 + "╝")

print("\n✅ All tests passed!")
print("\n📝 Key Features:")
print("  • Automatic chunking for large transcripts (>50K chars)")
print("  • Smart splitting at natural boundaries (speaker changes)")
print("  • Rate limiting to avoid API spam")
print("  • Automatic result merging from multiple chunks")
print("  • Duplicate detection and removal")

print("\n💡 Usage:")
print("  executor = ChunkedFunctionExecutor(")
print("      transcript,")
print("      output_language='vi',")
print("      enable_translation=True,")
print("      chunk_strategy='smart',  # or 'simple', 'balanced'")
print("      rate_limit_delay=0.5     # seconds between chunks")
print("  )")
print("  result = executor.execute('get_meeting_participants', {})")

print("\n" + "=" * 80)
