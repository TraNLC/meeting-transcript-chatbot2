"""Test script for get_meeting_participants function."""

from src.rag.function_executor import FunctionExecutor

# Read the sample meeting transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

# Create executor
executor = FunctionExecutor(transcript)

# Test get_meeting_participants
print("=== Testing get_meeting_participants() ===\n")
result = executor.execute("get_meeting_participants", {})
print(result)

print("\n=== Summary ===")
import json
data = json.loads(result)
print(f"Total participants found: {len(data['participants'])}")
for p in data['participants']:
    print(f"  - {p['name']} ({p['role']}): {p['contribution']}")
