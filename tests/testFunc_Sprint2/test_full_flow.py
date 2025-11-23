"""Test full flow with UniversalMeetingExecutor."""

from src.rag.universal_executor import UniversalMeetingExecutor
import json

# Read sample meeting 2
with open('data/transcripts/sample_meeting2.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

print("=" * 80)
print("TESTING FULL FLOW - ENGLISH OUTPUT")
print("=" * 80)

# Create executor with English output
executor = UniversalMeetingExecutor(
    transcript=transcript,
    meeting_type="meeting",
    output_language="en",
    enable_translation=True
)

print("\n📊 Executor Info:")
info = executor.get_info()
print(f"  Meeting type: {info['meeting_type']}")
print(f"  Available functions: {info['available_functions']}")
print(f"  Is chunked: {info['is_chunked']}")

print("\n" + "=" * 80)
print("TEST 1: GET PARTICIPANTS")
print("=" * 80)

result = executor.execute("get_meeting_participants", {})
data = json.loads(result)

print(f"\nFound {len(data['participants'])} participants:\n")
for p in data['participants']:
    print(f"  Name: {p['name']}")
    print(f"  Role: {p['role']}")
    print(f"  Contribution: {p['contribution']}")
    print()

# Check if output is in English
print("Checking translation:")
sample_contribution = data['participants'][0]['contribution'] if data['participants'] else ""
if "Spoke" in sample_contribution:
    print("  ✅ English detected")
elif "Phát biểu" in sample_contribution:
    print("  ❌ Vietnamese detected - Translation not working!")
else:
    print(f"  ⚠️  Unknown format: {sample_contribution}")

print("\n" + "=" * 80)
print("TEST 2: EXTRACT DECISIONS")
print("=" * 80)

result = executor.execute("extract_decisions", {})
data = json.loads(result)

print(f"\nFound {len(data['decisions'])} decisions:\n")
for i, d in enumerate(data['decisions'][:2], 1):
    print(f"{i}. Decision: {d['decision']}")
    print(f"   Context: {d['context']}")
    print(f"   Impact: {d['impact']}")
    print()

# Check translation
if data['decisions']:
    sample_context = data['decisions'][0]['context']
    if "Mentioned in meeting discussion" in sample_context:
        print("  ✅ English context detected")
    elif "Được đề cập" in sample_context:
        print("  ❌ Vietnamese context - Translation not working!")

print("\n" + "=" * 80)
