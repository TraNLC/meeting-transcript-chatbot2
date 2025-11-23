"""Test edge cases for all functions."""

from src.rag.function_executor import FunctionExecutor
import json

# Read the sample meeting transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

executor = FunctionExecutor(transcript)

print("=" * 70)
print("TESTING EDGE CASES")
print("=" * 70)

# Test 1: Filter action items by specific assignee
print("\n1. FILTER ACTION ITEMS BY ASSIGNEE (Mai)")
print("-" * 70)
result = executor.execute("extract_action_items", {"assignee": "Mai"})
data = json.loads(result)
print(f"Found {len(data['action_items'])} action items for Mai:")
for item in data['action_items']:
    print(f"  • {item['task']}")
    print(f"    Deadline: {item['deadline']}")

# Test 2: Filter action items by another assignee
print("\n2. FILTER ACTION ITEMS BY ASSIGNEE (Tuấn)")
print("-" * 70)
result = executor.execute("extract_action_items", {"assignee": "Tuấn"})
data = json.loads(result)
print(f"Found {len(data['action_items'])} action items for Tuấn:")
for item in data['action_items']:
    print(f"  • {item['task']}")

# Test 3: Search with different keywords
print("\n3. SEARCH TRANSCRIPT (keyword: 'payment')")
print("-" * 70)
result = executor.execute("search_transcript", {"keyword": "payment", "context_lines": 1})
data = json.loads(result)
print(f"Found {data['total_matches']} matches")
for match in data['results']:
    print(f"  Line {match['line_number']}: {match['matched_line'][:80]}...")

# Test 4: Search Vietnamese keyword
print("\n4. SEARCH TRANSCRIPT (keyword: 'ngân sách' / 'budget')")
print("-" * 70)
result = executor.execute("search_transcript", {"keyword": "budget", "context_lines": 0})
data = json.loads(result)
print(f"Found {data['total_matches']} matches for 'budget'")

# Test 5: Verify participant roles are correct
print("\n5. VERIFY PARTICIPANT ROLES")
print("-" * 70)
result = executor.execute("get_meeting_participants", {})
data = json.loads(result)
expected_roles = {
    "Hiếu": "Project Manager",
    "Mai": "Designer", 
    "Tuấn": "Developer",
    "Linh": "Marketing"
}
all_correct = True
for p in data['participants']:
    expected = expected_roles.get(p['name'])
    actual = p['role']
    status = "✓" if expected == actual else "✗"
    print(f"  {status} {p['name']}: Expected '{expected}', Got '{actual}'")
    if expected != actual:
        all_correct = False

print(f"\n  Result: {'All roles correct!' if all_correct else 'Some roles incorrect!'}")

# Test 6: Check if decisions are meaningful
print("\n6. VERIFY DECISIONS QUALITY")
print("-" * 70)
result = executor.execute("extract_decisions", {})
data = json.loads(result)
print(f"Found {len(data['decisions'])} decisions:")
for i, decision in enumerate(data['decisions'], 1):
    print(f"  {i}. {decision['decision']}")

print("\n" + "=" * 70)
print("EDGE CASE TESTING COMPLETED")
print("=" * 70)
