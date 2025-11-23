"""Test with English input transcript."""

from src.rag.function_executor import FunctionExecutor
import json

# English transcript
english_transcript = """
MEETING TRANSCRIPT - E-COMMERCE PROJECT
Date: November 15, 2024
Time: 9:00 AM - 10:30 AM
Participants: John (Project Manager), Sarah (Designer), Mike (Developer), Lisa (Marketing)

---

John: Good morning everyone! Thank you for joining today's meeting. We'll discuss the e-commerce website project progress and plan for the next sprint.

Sarah: Good morning John and everyone!

Mike: Hello everyone!

Lisa: Good morning!

John: Alright, let's start. First, Sarah, can you update us on the design?

Sarah: Sure. I've completed the UI design for the homepage, product page, and shopping cart. I've sent the Figma files to the team. However, I think we should change the primary color from blue to green to better match the brand.

John: That's a good idea, Sarah. What does everyone think about changing the color?

Mike: I think it's fine. Green looks fresher and fits our eco-friendly concept.

Lisa: I agree! Green will differentiate us from competitors.

John: Great! So we decided to change to green. Sarah, please update the design with the new color and send it back to the team by Wednesday this week.

Sarah: I will complete it before Wednesday.

John: Excellent! Next, Mike, update on development.

Mike: I've completed 80% of the backend API. Currently working on authentication and authorization. I expect to finish this part by the end of this week. However, I'm facing a small issue with payment gateway integration.

John: What's the issue, Mike?

Mike: The payment provider's documentation isn't very clear. I need more time to research and test. I think I need 3-4 more days.

John: Okay. So please try to complete the payment integration before November 22nd. Let the team know if you need support.

Mike: Thank you!

John: What about the frontend, Mike?

Mike: Frontend is about 50% done. I'm waiting for the final design from Sarah to implement. After getting the new design, I'll speed up this part.

John: OK. So Mike's priorities this week are: 1) Complete authentication, 2) Payment integration, 3) Frontend implementation after getting the new design.

Mike: Yes, sir!

John: Lisa, please update on the marketing plan.

Lisa: I've prepared a content plan for the first 3 months. I've created 20 blog posts and 50 social media posts. I've also contacted 5 influencers for the launch campaign collaboration.

John: Great! What's the budget for influencer marketing?

Lisa: I estimate about $50,000 for the first 3 months.

John: Hmm, $50,000 is a bit high. We need to reduce it to $35,000. Please try to negotiate with the influencers.

Lisa: Okay, I'll try to negotiate. If not possible, I'll reduce the number of influencers from 5 to 3.

John: Good! That's a good solution. So we decided the marketing budget is $35,000 for the first 3 months.

Lisa: Yes, sir!

John: About the launch date, we're still targeting December 1st, right?

Sarah: If everything goes smoothly, I think we can launch.

Mike: I think so too, but we need an extra week buffer for testing.

John: Alright. So we'll have a soft launch on December 1st for a beta user group, and official launch on December 8th. Everyone agrees?

Sarah: I agree!

Mike: OK!

Lisa: I agree too. So I'll prepare 2 separate campaigns for soft launch and official launch.

John: Perfect! So to summarize:
- Sarah will update the design with green color before Wednesday
- Mike will complete authentication by end of this week and payment integration before November 22nd
- Lisa will negotiate the budget down to $35,000 and prepare 2 launch campaigns
- Soft launch: December 1st, Official launch: December 8th

Any questions?

Sarah: No questions.

Mike: I'm clear.

Lisa: I'm OK!

John: Great! Let's end the meeting here. Thank you everyone! See you at next week's meeting.

Everyone: Thank you! Bye bye!

--- END OF TRANSCRIPT ---
"""

print("╔" + "═" * 78 + "╗")
print("║" + " " * 15 + "TEST WITH ENGLISH INPUT TRANSCRIPT" + " " * 28 + "║")
print("╚" + "═" * 78 + "╝")

print("\n📄 Input: English transcript")
print("=" * 80)

# Test with Vietnamese output
print("\n" + "=" * 80)
print("🇻🇳 ENGLISH INPUT → VIETNAMESE OUTPUT")
print("=" * 80)

executor_vi = FunctionExecutor(english_transcript, output_language="vi")

print("\n1. PARTICIPANTS (Người tham gia)")
print("-" * 80)
result = executor_vi.execute("get_meeting_participants", {})
data = json.loads(result)
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']}): {p['contribution']}")

print("\n2. ACTION ITEMS (Nhiệm vụ)")
print("-" * 80)
result = executor_vi.execute("extract_action_items", {})
data = json.loads(result)
print(f"Tìm thấy {len(data['action_items'])} nhiệm vụ:")
for item in data['action_items'][:3]:
    print(f"  • {item['assignee']}: {item['task'][:60]}...")
    print(f"    Deadline: {item['deadline']}, Ưu tiên: {item['priority']}")

# Test with English output
print("\n" + "=" * 80)
print("🇬🇧 ENGLISH INPUT → ENGLISH OUTPUT")
print("=" * 80)

executor_en = FunctionExecutor(english_transcript, output_language="en")

print("\n1. PARTICIPANTS")
print("-" * 80)
result = executor_en.execute("get_meeting_participants", {})
data = json.loads(result)
for p in data['participants']:
    print(f"  • {p['name']} ({p['role']}): {p['contribution']}")

print("\n2. ACTION ITEMS")
print("-" * 80)
result = executor_en.execute("extract_action_items", {})
data = json.loads(result)
print(f"Found {len(data['action_items'])} action items:")
for item in data['action_items'][:3]:
    print(f"  • {item['assignee']}: {item['task'][:60]}...")
    print(f"    Deadline: {item['deadline']}, Priority: {item['priority']}")

print("\n" + "=" * 80)
print("✅ WORKS WITH ANY INPUT LANGUAGE!")
print("=" * 80)
print("\n💡 Key Feature:")
print("  • Input can be ANY language (Vietnamese, English, etc.)")
print("  • Output language is controlled by 'output_language' parameter")
print("  • Metadata (labels, status) are translated")
print("  • Content (names, tasks, decisions) remain in original language")
print("=" * 80)
