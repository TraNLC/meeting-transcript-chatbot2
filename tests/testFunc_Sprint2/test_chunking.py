"""Test transcript chunking with large files."""

from src.rag.transcript_processor import TranscriptProcessor

# Read sample transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

print("╔" + "═" * 78 + "╗")
print("║" + " " * 25 + "CHUNKING TEST" + " " * 40 + "║")
print("╚" + "═" * 78 + "╝")

# Test 1: Normal size
print("\n" + "=" * 80)
print("TEST 1: NORMAL TRANSCRIPT")
print("=" * 80)

processor = TranscriptProcessor(transcript)
print(processor.get_summary())

# Test 2: Large transcript (50x)
print("\n" + "=" * 80)
print("TEST 2: LARGE TRANSCRIPT (50x original)")
print("=" * 80)

large_transcript = transcript * 50
large_processor = TranscriptProcessor(large_transcript)
print(large_processor.get_summary())

validation = large_processor.validate()
if validation['needs_chunking']:
    print("\n📦 CHUNKING STRATEGIES COMPARISON")
    print("-" * 80)
    
    strategies = ["simple", "smart", "balanced"]
    
    for strategy in strategies:
        chunks = large_processor.split_into_chunks(strategy=strategy)
        print(f"\n{strategy.upper()} Strategy:")
        print(f"  Total chunks: {len(chunks)}")
        
        # Show first 3 chunks
        for chunk in chunks[:3]:
            print(f"    Chunk {chunk.index}: {chunk.char_count:,} chars, "
                  f"{chunk.word_count:,} words, lines {chunk.start_line}-{chunk.end_line}")
        
        if len(chunks) > 3:
            print(f"    ... and {len(chunks) - 3} more chunks")
        
        # Calculate balance (std deviation of chunk sizes)
        sizes = [c.char_count for c in chunks]
        avg_size = sum(sizes) / len(sizes)
        variance = sum((s - avg_size) ** 2 for s in sizes) / len(sizes)
        std_dev = variance ** 0.5
        balance_score = (std_dev / avg_size) * 100
        
        print(f"    Average size: {avg_size:,.0f} chars")
        print(f"    Balance score: {balance_score:.1f}% (lower is better)")

# Test 3: Very large transcript (100x)
print("\n\n" + "=" * 80)
print("TEST 3: VERY LARGE TRANSCRIPT (100x original)")
print("=" * 80)

very_large_transcript = transcript * 100
very_large_processor = TranscriptProcessor(very_large_transcript)
print(very_large_processor.get_summary())

validation = very_large_processor.validate()
if validation['needs_chunking']:
    chunks = very_large_processor.split_into_chunks(strategy="smart")
    print(f"\n📊 Chunk Distribution:")
    print("-" * 80)
    
    for i, chunk in enumerate(chunks):
        bar_length = int((chunk.char_count / 50000) * 40)
        bar = "█" * bar_length
        print(f"  Chunk {i:2d}: {bar} {chunk.char_count:,} chars")

# Test 4: Rate limiting check
print("\n\n" + "=" * 80)
print("TEST 4: RATE LIMITING CHECK")
print("=" * 80)

test_sizes = [1, 10, 50, 100, 200]
for size in test_sizes:
    test_transcript = transcript * size
    test_processor = TranscriptProcessor(test_transcript)
    validation = test_processor.validate()
    stats = validation['statistics']
    
    status = "✅ OK" if stats['estimated_chunks'] <= 10 else "⚠️  WARNING"
    print(f"  {size:3d}x: {stats['total_chars']:>8,} chars → "
          f"{stats['estimated_chunks']:2d} chunks {status}")

print("\n" + "=" * 80)
print("✅ CHUNKING TESTS COMPLETED")
print("=" * 80)
print("\n💡 Recommendations:")
print("  • Use 'smart' strategy for best results")
print("  • Keep transcripts under 500K characters for optimal performance")
print("  • Chunks are split at natural boundaries (speaker changes)")
print("=" * 80)
