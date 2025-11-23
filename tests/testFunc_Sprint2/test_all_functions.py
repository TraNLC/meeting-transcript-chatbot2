"""Test all functions with Vietnamese transcript."""

from src.rag.function_executor import FunctionExecutor
import json

# Read the sample meeting transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

# Create executor
executor = FunctionExecutor(transcript)

print("=" * 60)
print("TESTING ALL FUNCTIONS WITH VIETNAMESE TRANSCRIPT")
print("=" * 60)

# Test 1: Get participants
print("\n1. GET MEETING PARTICIPANTS")
print("-" * 60)
result = executor.execute("get_meeting_participants", {})
data = json.loads(result)
print(f"Found {len(data['participants'])} participants:")
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']}): {p['contribution']}")

# Test 2: Extract action items
print("\n2. EXTRACT ACTION ITEMS")
print("-" * 60)
result = executor.execute("extract_action_items", {})
data = json.loads(result)
print(f"Found {len(data['action_items'])} action items:")
for item in data['action_items']:
    print(f"  • {item['assignee']}: {item['task']}")
    print(f"    Deadline: {item['deadline']}")

# Test 3: Extract decisions
print("\n3. EXTRACT DECISIONS")
print("-" * 60)
result = executor.execute("extract_decisions", {})
data = json.loads(result)
print(f"Found {len(data['decisions'])} decisions:")
for decision in data['decisions']:
    print(f"  • {decision['decision']}")

# Test 4: Search transcript
print("\n4. SEARCH TRANSCRIPT (keyword: 'design')")
print("-" * 60)
result = executor.execute("search_transcript", {"keyword": "design", "context_lines": 1})
data = json.loads(result)
print(f"Found {data['total_matches']} matches for '{data['keyword']}'")
for i, match in enumerate(data['results'][:3], 1):  # Show first 3
    print(f"\n  Match {i} (line {match['line_number']}):")
    print(f"  {match['matched_line']}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
