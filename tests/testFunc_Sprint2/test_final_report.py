"""Final comprehensive test report."""

from src.rag.function_executor import FunctionExecutor
import json

# Read the sample meeting transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

executor = FunctionExecutor(transcript)

print("╔" + "═" * 68 + "╗")
print("║" + " " * 15 + "FINAL TEST REPORT - ALL FUNCTIONS" + " " * 20 + "║")
print("╚" + "═" * 68 + "╝")

test_results = []

# Test 1: get_meeting_participants
print("\n[TEST 1] get_meeting_participants()")
print("-" * 70)
try:
    result = executor.execute("get_meeting_participants", {})
    data = json.loads(result)
    participants = data['participants']
    
    # Verify all expected participants are found
    expected_names = {"Hiếu", "Mai", "Tuấn", "Linh"}
    found_names = {p['name'] for p in participants}
    
    # Verify roles are extracted
    has_roles = all(p['role'] != "Participant" for p in participants)
    
    # Verify contribution counts
    has_contributions = all('Spoke' in p['contribution'] for p in participants)
    
    status = "✓ PASS" if (found_names == expected_names and has_roles and has_contributions) else "✗ FAIL"
    test_results.append(("get_meeting_participants", status == "✓ PASS"))
    
    print(f"Status: {status}")
    print(f"  • Found {len(participants)} participants (expected 4)")
    print(f"  • All names correct: {found_names == expected_names}")
    print(f"  • Roles extracted: {has_roles}")
    print(f"  • Contributions counted: {has_contributions}")
    
except Exception as e:
    print(f"Status: ✗ FAIL - {str(e)}")
    test_results.append(("get_meeting_participants", False))

# Test 2: extract_action_items
print("\n[TEST 2] extract_action_items()")
print("-" * 70)
try:
    result = executor.execute("extract_action_items", {})
    data = json.loads(result)
    action_items = data['action_items']
    
    # Verify action items are found
    has_items = len(action_items) > 0
    
    # Verify assignees are real participants (not "em", "ta", etc.)
    valid_assignees = all(p['assignee'] in {"Hiếu", "Mai", "Tuấn", "Linh"} for p in action_items)
    
    # Verify structure
    has_structure = all('task' in p and 'assignee' in p and 'deadline' in p for p in action_items)
    
    # Test filtering by assignee
    result_filtered = executor.execute("extract_action_items", {"assignee": "Mai"})
    data_filtered = json.loads(result_filtered)
    filtered_correct = all(p['assignee'] == "Mai" for p in data_filtered['action_items'])
    
    status = "✓ PASS" if (has_items and valid_assignees and has_structure and filtered_correct) else "✗ FAIL"
    test_results.append(("extract_action_items", status == "✓ PASS"))
    
    print(f"Status: {status}")
    print(f"  • Found {len(action_items)} action items")
    print(f"  • Valid assignees only: {valid_assignees}")
    print(f"  • Correct structure: {has_structure}")
    print(f"  • Filtering works: {filtered_correct}")
    
except Exception as e:
    print(f"Status: ✗ FAIL - {str(e)}")
    test_results.append(("extract_action_items", False))

# Test 3: search_transcript
print("\n[TEST 3] search_transcript()")
print("-" * 70)
try:
    result = executor.execute("search_transcript", {"keyword": "design", "context_lines": 1})
    data = json.loads(result)
    
    # Verify search finds matches
    has_matches = data['total_matches'] > 0
    
    # Verify structure
    has_structure = all('line_number' in r and 'matched_line' in r for r in data['results'])
    
    # Verify keyword is in matched lines
    keyword_in_matches = all('design' in r['matched_line'].lower() for r in data['results'])
    
    # Test case insensitive
    result2 = executor.execute("search_transcript", {"keyword": "DESIGN"})
    data2 = json.loads(result2)
    case_insensitive = data2['total_matches'] == data['total_matches']
    
    status = "✓ PASS" if (has_matches and has_structure and keyword_in_matches and case_insensitive) else "✗ FAIL"
    test_results.append(("search_transcript", status == "✓ PASS"))
    
    print(f"Status: {status}")
    print(f"  • Found {data['total_matches']} matches")
    print(f"  • Correct structure: {has_structure}")
    print(f"  • Keyword in results: {keyword_in_matches}")
    print(f"  • Case insensitive: {case_insensitive}")
    
except Exception as e:
    print(f"Status: ✗ FAIL - {str(e)}")
    test_results.append(("search_transcript", False))

# Test 4: extract_decisions
print("\n[TEST 4] extract_decisions()")
print("-" * 70)
try:
    result = executor.execute("extract_decisions", {})
    data = json.loads(result)
    decisions = data['decisions']
    
    # Verify decisions are found
    has_decisions = len(decisions) > 0
    
    # Verify structure
    has_structure = all('decision' in d for d in decisions)
    
    # Verify decisions are meaningful (not empty)
    meaningful = all(len(d['decision'].strip()) > 5 for d in decisions)
    
    status = "✓ PASS" if (has_decisions and has_structure and meaningful) else "✗ FAIL"
    test_results.append(("extract_decisions", status == "✓ PASS"))
    
    print(f"Status: {status}")
    print(f"  • Found {len(decisions)} decisions")
    print(f"  • Correct structure: {has_structure}")
    print(f"  • Meaningful content: {meaningful}")
    
except Exception as e:
    print(f"Status: ✗ FAIL - {str(e)}")
    test_results.append(("extract_decisions", False))

# Summary
print("\n" + "═" * 70)
print("SUMMARY")
print("═" * 70)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for func_name, result in test_results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"  {status}  {func_name}")

print(f"\nTotal: {passed}/{total} tests passed")

if passed == total:
    print("\n🎉 ALL TESTS PASSED! Functions are working correctly.")
else:
    print(f"\n⚠️  {total - passed} test(s) failed. Please review.")

print("═" * 70)
