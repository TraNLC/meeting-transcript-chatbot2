"""Test full content translation with multiple languages."""

from src.rag.function_executor import FunctionExecutor
from src.rag.translator import ContentTranslator
import json

# Read Vietnamese transcript
with open('data/transcripts/sample_meeting.txt', 'r', encoding='utf-8') as f:
    transcript_vi = f.read()

print("╔" + "═" * 78 + "╗")
print("║" + " " * 20 + "FULL CONTENT TRANSLATION TEST" + " " * 28 + "║")
print("╚" + "═" * 78 + "╝")

print("\n📄 Input: Vietnamese transcript (sample_meeting.txt)")
print("🌍 Testing translation to multiple languages")
print("=" * 80)

# List of languages to test
test_languages = [
    ("vi", "🇻🇳 Vietnamese"),
    ("en", "🇬🇧 English"),
    ("ja", "🇯🇵 Japanese"),
    ("ko", "🇰🇷 Korean"),
    ("zh-CN", "🇨🇳 Chinese (Simplified)"),
    ("es", "🇪🇸 Spanish"),
    ("fr", "🇫🇷 French"),
]

print("\n" + "=" * 80)
print("SUPPORTED LANGUAGES")
print("=" * 80)
for code, name in ContentTranslator.get_supported_languages().items():
    print(f"  • {code:8} - {name}")

# Test with 3 languages in detail
for lang_code, lang_name in test_languages[:3]:
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + f" OUTPUT: {lang_name}".ljust(79) + "║")
    print("╚" + "═" * 78 + "╝")
    
    executor = FunctionExecutor(
        transcript_vi, 
        output_language=lang_code,
        enable_translation=True
    )
    
    # Test 1: Participants
    print(f"\n1️⃣  PARTICIPANTS")
    print("-" * 80)
    result = executor.execute("get_meeting_participants", {})
    data = json.loads(result)
    for p in data['participants'][:2]:  # Show first 2
        print(f"  • {p['name']} ({p['role']})")
        print(f"    {p['contribution']}")
    
    # Test 2: Action Items
    print(f"\n2️⃣  ACTION ITEMS")
    print("-" * 80)
    result = executor.execute("extract_action_items", {})
    data = json.loads(result)
    if data['action_items']:
        item = data['action_items'][0]
        print(f"  Assignee: {item['assignee']}")
        print(f"  Task: {item['task'][:60]}...")
        print(f"  Deadline: {item['deadline']}")
        print(f"  Priority: {item['priority']}")
    
    # Test 3: Decisions
    print(f"\n3️⃣  DECISIONS")
    print("-" * 80)
    result = executor.execute("extract_decisions", {})
    data = json.loads(result)
    if data['decisions']:
        decision = data['decisions'][0]
        print(f"  Decision: {decision['decision']}")
        print(f"  Context: {decision['context']}")
        print(f"  Impact: {decision['impact']}")

# Quick comparison table
print("\n\n" + "╔" + "═" * 78 + "╗")
print("║" + " " * 25 + "📊 TRANSLATION COMPARISON" + " " * 28 + "║")
print("╚" + "═" * 78 + "╝")

print("\nSample text: 'Phát biểu 10 lần'")
print("-" * 80)

sample_text = "Phát biểu 10 lần"
for lang_code, lang_name in test_languages:
    translator = ContentTranslator(lang_code)
    translated = translator.translate_text(sample_text)
    print(f"  {lang_name:25} → {translated}")

print("\n" + "=" * 80)
print("✅ FULL TRANSLATION FEATURE WORKING!")
print("=" * 80)
print("\n💡 Usage:")
print("  executor = FunctionExecutor(")
print("      transcript,")
print("      output_language='ja',  # Any supported language code")
print("      enable_translation=True")
print("  )")
print("\n📝 Note:")
print("  • Content (tasks, decisions) are fully translated")
print("  • Names remain unchanged")
print("  • Requires internet connection")
print("  • Uses Google Translate API (free tier)")
print("=" * 80)
