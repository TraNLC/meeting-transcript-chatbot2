"""
Generate Workshop and Interview Meeting Data

Creates realistic:
- Design workshops (Design thinking, UX, Product)
- Training workshops (Agile, Leadership, Technical)
- Interviews (Candidate, User research, Exit)
"""

import json
import os
from datetime import datetime, timedelta
import random
from pathlib import Path

# Workshop scenarios
WORKSHOPS = [
    {
        "type": "workshop",
        "title": "Design Thinking Workshop - Customer Journey Mapping",
        "duration": "3:30:00",
        "participants": ["Sarah Chen", "Mike Johnson", "Lisa Park", "David Kim", "Emma Wilson"],
        "topics": ["Customer journey mapping", "Pain points analysis", "Empathy mapping", "Ideation sessions"],
        "summary": "Comprehensive design thinking workshop focused on mapping customer journey for new mobile app. Team identified 5 major pain points and generated 12 potential solutions through collaborative ideation.",
        "key_decisions": [
            "Focus on mobile-first approach for Q1 2025",
            "Prioritize checkout flow optimization",
            "Schedule follow-up validation workshop in 2 weeks"
        ],
        "action_items": [
            {"assignee": "Sarah Chen", "task": "Create detailed customer personas based on workshop insights"},
            {"assignee": "Mike Johnson", "task": "Build prototype of new checkout flow"},
            {"assignee": "Lisa Park", "task": "Schedule user testing sessions"}
        ]
    },
    {
        "type": "workshop",
        "title": "Agile Scrum Master Training - Sprint Planning Best Practices",
        "duration": "4:00:00",
        "participants": ["John Smith", "Maria Garcia", "Alex Wong", "Rachel Lee", "Tom Brown"],
        "topics": ["Sprint planning", "Story estimation", "Velocity tracking", "Retrospectives"],
        "summary": "Full-day Agile training covering Scrum fundamentals and advanced sprint planning techniques. Participants practiced story point estimation and learned how to run effective retrospectives.",
        "key_decisions": [
            "Adopt planning poker for story estimation",
            "Implement bi-weekly retrospectives",
            "Use JIRA for sprint tracking"
        ],
        "action_items": [
            {"assignee": "John Smith", "task": "Set up JIRA boards for all teams"},
            {"assignee": "Maria Garcia", "task": "Create sprint planning template"},
            {"assignee": "Alex Wong", "task": "Schedule team onboarding sessions"}
        ]
    },
    {
        "type": "workshop",
        "title": "Product Discovery Workshop - Q1 2025 Roadmap",
        "duration": "2:45:00",
        "participants": ["Emily Davis", "Chris Anderson", "Nina Patel", "Robert Taylor"],
        "topics": ["Product roadmap", "Feature prioritization", "Market analysis", "Competitive landscape"],
        "summary": "Strategic product planning session for Q1 2025. Team analyzed market trends, competitor features, and customer feedback to shape roadmap priorities.",
        "key_decisions": [
            "Launch AI-powered search feature in January",
            "Delay mobile app redesign to Q2",
            "Invest in analytics infrastructure"
        ],
        "action_items": [
            {"assignee": "Emily Davis", "task": "Draft detailed product requirements for AI search"},
            {"assignee": "Chris Anderson", "task": "Conduct competitive analysis deep-dive"},
            {"assignee": "Nina Patel", "task": "Create user survey for feature validation"}
        ]
    }
]

INTERVIEWS = [
    {
        "type": "interview",
        "title": "Senior Frontend Developer Interview - Candidate: Alex Thompson",
        "duration": "1:15:00",
        "participants": ["Hiring Manager - Sarah Chen", "Tech Lead - Mike Johnson", "Candidate - Alex Thompson"],
        "topics": ["React expertise", "System design", "Team collaboration", "Problem-solving"],
        "summary": "Technical interview for Senior Frontend Developer position. Candidate demonstrated strong React skills, excellent system design thinking, and great cultural fit. Successfully completed live coding challenge.",
        "key_decisions": [
            "Move candidate to final round",
            "Schedule culture fit interview with CEO",
            "Prepare offer pending final approval"
        ],
        "action_items": [
            {"assignee": "Sarah Chen", "task": "Schedule final interview within 3 days"},
            {"assignee": "Mike Johnson", "task": "Prepare technical assessment feedback"},
            {"assignee": "HR Team", "task": "Conduct reference checks"}
        ]
    },
    {
        "type": "interview",
        "title": "User Research Interview - Mobile App Pain Points",
        "duration": "0:45:00",
        "participants": ["UX Researcher - Lisa Park", "Product Manager - Emily Davis", "User - Customer A"],
        "topics": ["App usability", "Feature requests", "Navigation issues", "Performance feedback"],
        "summary": "One-on-one user interview revealed significant friction in checkout process. User struggled with payment method selection and expressed frustration with slow load times.",
        "key_decisions": [
            "Prioritize checkout flow optimization",
            "Investigate performance bottlenecks",
            "Conduct 5 more user interviews this week"
        ],
        "action_items": [
            {"assignee": "Lisa Park", "task": "Synthesize findings from all user interviews"},
            {"assignee": "Emily Davis", "task": "Update product backlog with UX improvements"},
            {"assignee": "Engineering", "task": "Performance audit of mobile app"}
        ]
    }
]

def generate_meeting_file(data, index):
    """Generate a single meeting JSON file"""
    
    # Random date within last 30 days
    days_ago = random.randint(1, 30)
    meeting_date = datetime.now() - timedelta(days=days_ago)
    
    meeting_data = {
        "id": f"{data['type']}_{index}_{meeting_date.strftime('%Y%m%d')}",
        "timestamp": meeting_date.isoformat(),
        "original_file": f"{data['title'].lower().replace(' ', '_')[:40]}.mp3",
        "summary": data["summary"],
        "topics": data["topics"],
        "action_items": data["action_items"],
        "decisions": data["key_decisions"],
        "metadata": {
            "duration": data["duration"],
            "participants": data["participants"],
            "meeting_type": data["type"],
            "language": "en",
            "transcript": f"[{data['type'].upper()}] {data['title']}\n\nParticipants: {', '.join(data['participants'])}\n\nDiscussion covered: {', '.join(data['topics'])}\n\n{data['summary']}"
        }
    }
    
    return meeting_data

def main():
    print("=" * 70)
    print("WORKSHOP & INTERVIEW DATA GENERATOR")
    print("=" * 70)
    
    # Create data/history if not exists
    history_dir = Path("data/history")
    history_dir.mkdir(parents=True, exist_ok=True)
    
    generated = []
    
    # Generate workshops
    print(f"\nGenerating {len(WORKSHOPS)} workshops...")
    for i, workshop in enumerate(WORKSHOPS):
        meeting = generate_meeting_file(workshop, i)
        filename = history_dir / f"{meeting['id']}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meeting, f, indent=2, ensure_ascii=False)
        
        print(f"  OK: {workshop['title'][:50]}...")
        generated.append(filename)
    
    # Generate interviews
    print(f"\nGenerating {len(INTERVIEWS)} interviews...")
    for i, interview in enumerate(INTERVIEWS):
        meeting = generate_meeting_file(interview, i)
        filename = history_dir / f"{meeting['id']}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meeting, f, indent=2, ensure_ascii=False)
        
        print(f"  OK: {interview['title'][:50]}...")
        generated.append(filename)
    
    print(f"\nTotal generated: {len(generated)} files")
    
    # Trigger reindex
    print("\nTriggering ChromaDB re-index...")
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from backend.data.history_searcher import HistorySearcher
        
        searcher = HistorySearcher()
        count = searcher.index_all_meetings(force_reindex=True)
        print(f"OK: Indexed {count} meetings successfully!")
        
    except Exception as e:
        print(f"⚠ Auto-index failed: {e}")
        print("Please run: python tests/reindex_history.py")
    
    print("\n" + "=" * 70)
    print("✓ COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
