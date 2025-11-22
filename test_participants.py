"""Test participant extraction."""

from src.rag.function_executor import FunctionExecutor
import json

# Read test transcript
with open('test_transcript.txt', encoding='utf-8') as f:
    transcript = f.read()

# Create executor
executor = FunctionExecutor(transcript)

# Test get_meeting_participants
result = executor.execute('get_meeting_participants', {})
data = json.loads(result)

print(f"Found {len(data['participants'])} participants:")
print()
for p in data['participants']:
    print(f"  ✓ {p['name']}")
    print(f"    Role: {p['role']}")
    print(f"    {p['contribution']}")
    print()

print("\nExpected: Alice, Bob, Charlie, Diana (4 people)")
