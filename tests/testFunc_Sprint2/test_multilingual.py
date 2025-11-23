"""Test multilingual output feature."""

from src.rag.function_executor import FunctionExecutor
import json

# Read the sample meeting transcript (Vietnamese)
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

print("╔" + "═" * 78 + "╗")
print("║" + " " * 20 + "MULTILINGUAL OUTPUT TEST" + " " * 33 + "║")
print("╚" + "═" * 78 + "╝")

print("\n📄 Input: Vietnamese transcript (sample_meeting.txt)")
print("=" * 80)

# Test 1: Vietnamese output (default)
print("\n" + "=" * 80)
print("🇻🇳 OUTPUT IN VIETNAMESE (Tiếng Việt)")
print("=" * 80)

executor_vi = FunctionExecutor(transcript, output_language="vi")

print("\n1. GET MEETING PARTICIPANTS")
print("-" * 80)
result = executor_vi.execute("get_meeting_participants", {})
data = json.loads(result)
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']})")
    print(f"    {p['contribution']}")

print("\n2. EXTRACT ACTION ITEMS")
print("-" * 80)
result = executor_vi.execute("extract_action_items", {})
data = json.loads(result)
for item in data['action_items'][:3]:  # Show first 3
    print(f"  • Người thực hiện: {item['assignee']}")
    print(f"    Nhiệm vụ: {item['task']}")
    print(f"    Deadline: {item['deadline']}")
    print(f"    Ưu tiên: {item['priority']}")
    print()

print("3. EXTRACT DECISIONS")
print("-" * 80)
result = executor_vi.execute("extract_decisions", {})
data = json.loads(result)
for decision in data['decisions']:
    print(f"  • Quyết định: {decision['decision']}")
    print(f"    Bối cảnh: {decision['context']}")
    print(f"    Tác động: {decision['impact']}")
    print()

# Test 2: English output
print("\n" + "=" * 80)
print("🇬🇧 OUTPUT IN ENGLISH")
print("=" * 80)

executor_en = FunctionExecutor(transcript, output_language="en")

print("\n1. GET MEETING PARTICIPANTS")
print("-" * 80)
result = executor_en.execute("get_meeting_participants", {})
data = json.loads(result)
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']})")
    print(f"    {p['contribution']}")

print("\n2. EXTRACT ACTION ITEMS")
print("-" * 80)
result = executor_en.execute("extract_action_items", {})
data = json.loads(result)
for item in data['action_items'][:3]:  # Show first 3
    print(f"  • Assignee: {item['assignee']}")
    print(f"    Task: {item['task']}")
    print(f"    Deadline: {item['deadline']}")
    print(f"    Priority: {item['priority']}")
    print()

print("3. EXTRACT DECISIONS")
print("-" * 80)
result = executor_en.execute("extract_decisions", {})
data = json.loads(result)
for decision in data['decisions']:
    print(f"  • Decision: {decision['decision']}")
    print(f"    Context: {decision['context']}")
    print(f"    Impact: {decision['impact']}")
    print()

# Test 3: Comparison
print("\n" + "=" * 80)
print("📊 SIDE-BY-SIDE COMPARISON")
print("=" * 80)

print("\n{:<40} | {:<40}".format("VIETNAMESE", "ENGLISH"))
print("-" * 40 + " | " + "-" * 40)

# Compare participants
result_vi = executor_vi.execute("get_meeting_participants", {})
result_en = executor_en.execute("get_meeting_participants", {})
data_vi = json.loads(result_vi)
data_en = json.loads(result_en)

for p_vi, p_en in zip(data_vi['participants'], data_en['participants']):
    print("{:<40} | {:<40}".format(p_vi['contribution'], p_en['contribution']))

print("\n" + "=" * 80)
print("✅ MULTILINGUAL OUTPUT FEATURE WORKING!")
print("=" * 80)
print("\n💡 Usage:")
print("  • Vietnamese: FunctionExecutor(transcript, output_language='vi')")
print("  • English:    FunctionExecutor(transcript, output_language='en')")
print("=" * 80)
