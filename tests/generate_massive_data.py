"""
Generate Massive Mock Data for Semantic Search Testing.

Generates 50+ diverse meeting files to test semantic search capabilities.
Categories:
- Technology (Cloud, AI, Bugs)
- HR (Interviews, Culture)
- Business (Sales, Budget)
- Marketing (Campaigns, Branding)
"""

import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Ensure backend imports work
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.data.history_searcher import HistorySearcher
    HAS_SEARCHER = True
except ImportError:
    HAS_SEARCHER = False
    print("Warning: HistorySearcher/ChromaDB not found. Data will be generated but not indexed.")

HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# --- TEMPLATES ---

TEMPLATES = {
    "tech": {
        "titles": ["System Architecture Review", "Cloud Migration Strategy", "Critical Bug Post-mortem", "AI Integration Sync", "Weekly Dev Standoff"],
        "topics": [
            {"topic": "Kubernetes", "description": "Scaling issues in production"},
            {"topic": "Database", "description": "Migration to PostgreSQL"},
            {"topic": "Security", "description": "Vulnerability assessment report"},
            {"topic": "Frontend", "description": "React performance optimization"}
        ],
        "summary_fmt": "Technical discussion about {topic}. The team agreed to {decision}."
    },
    "hr": {
        "titles": ["Candidate Interview", "Quarterly Performance Review", "Team Culture Workshop", "Hiring Plan Q1", "Onboarding Process"],
        "topics": [
            {"topic": "Recruitment", "description": "Sourcing senior candidates"},
            {"topic": "Retention", "description": "Employee satisfaction survey results"},
            {"topic": "Training", "description": "Leadership workshop planning"}
        ],
        "summary_fmt": "HR meeting regarding {topic}. Action items assigned to improve {topic}."
    },
    "business": {
        "titles": ["Q3 Budget Planning", "Sales Strategy Kickoff", "Investor Update", "Market Analysis", "Revenue Forecast"],
        "topics": [
            {"topic": "Budget", "description": "Cost cutting measures for Q4"},
            {"topic": "Revenue", "description": "Exceeded targets by 15%"},
            {"topic": "Partnership", "description": "New deal with Enterprise client"}
        ],
        "summary_fmt": "Business sync covering {topic}. Financial outlook is {adjective}."
    }
}

ADJECTIVES = ["positive", "concerning", "stable", "uncertain", "optimistic"]

def generate_meeting(category, index):
    """Generate a single meeting entry."""
    template = TEMPLATES[category]
    date = datetime.now() - timedelta(days=random.randint(0, 100))
    
    title = random.choice(template["titles"]) + f" #{index}"
    topic_data = random.choice(template["topics"])
    summary = template["summary_fmt"].format(
        topic=topic_data["topic"], 
        decision="upgrade infrastructure", 
        adjective=random.choice(ADJECTIVES)
    )
    
    meeting = {
        "id": f"2025_{category}_{index}_{int(time.time())}",
        "original_file": f"{title.replace(' ', '_').lower()}.mp3",
        "timestamp": date.isoformat(),
        "summary": summary,
        "topics": [topic_data],
        "action_items": [
            {"task": f"Follow up on {topic_data['topic']}", "assignee": "Staff", "deadline": "2025-12-30"}
        ],
        "decisions": [
            {"decision": "Approved plan", "context": "Unanimous vote"}
        ],
        "metadata": {
            "meeting_type": "meeting",
            "language": "en" if random.random() > 0.5 else "vi",
            "category": category
        }
    }
    return meeting

def main():
    print(f"Generating massive data in {HISTORY_DIR.absolute()}...")
    
    count = 0
    categories = ["tech", "hr", "business"]
    
    # Generate 20 meetings per category
    for cat in categories:
        for i in range(20):
            data = generate_meeting(cat, i)
            with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            count += 1
            
    print(f"Generated {count} meetings.")
    
    if HAS_SEARCHER:
        print("\nTriggering Re-indexing...")
        try:
            searcher = HistorySearcher()
            num_indexed = searcher.index_all_meetings(force_reindex=True)
            print(f"Successfully indexed {num_indexed} meetings into ChromaDB.")
        except Exception as e:
            print(f"Indexing failed: {e}")
    else:
        print("Skipping indexing (dependencies missing).")

if __name__ == "__main__":
    main()
