"""
Generate Synthetic Meeting History using LLM.

Uses the project's LLMFactory to generate realistic, detailed meeting transcripts
and analysis (summary, action items, etc.) for testing RAG.
"""

import os
import sys
import json
import random
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure we can import from backend
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.llm.factory import LLMFactory

# Load environment variables
load_dotenv()

HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# Topics to prompt the LLM with
SCENARIOS = [
    "A heated debate about choosing between AWS and Google Cloud for the new infrastructure",
    "A quarterly all-hands meeting discussing Q4 goals and announcing a new 'Remote First' policy",
    "A post-mortem of a recent production outage involving the payment gateway",
    "A design critique of the new mobile app UI, focusing on accessibility and dark mode",
    "A salary review committee discussing compensation bands for next year",
    "A brainstorming session for a new AI feature in the product called 'Magic Assist'",
    "A client meeting with 'MegaCorp' negotiating a contract renewal",
    "A 1:1 performance review between a manager and a junior developer",
    "A marketing workshop planning the launch campaign for 'Version 2.0'",
    "A code review session discussing a complex refactor of the authentication service"
]

def get_llm():
    """Get LLM instance from factory."""
    # Try Gemini first, then OpenAI
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if gemini_key:
        print("Using Gemini for generation...")
        return LLMFactory.create("gemini", api_key=gemini_key)
    elif openai_key:
        print("Using OpenAI for generation...")
        return LLMFactory.create("openai", api_key=openai_key)
    else:
        raise ValueError("No API Key found! Please set GEMINI_API_KEY or OPENAI_API_KEY in .env")

def generate_meeting_content(llm, scenario):
    """Generate full meeting JSON using LLM."""
    
    prompt = f"""
    You are a data generator. Generate a realistic JSON object representing a meeting analysis based on this scenario: "{scenario}".
    
    The output must be VALID JSON with this structure:
    {{
        "title": "A catchy title matching the scenario",
        "summary": "A 3-sentence summary of the meeting",
        "topics": [
            {{"topic": "Main Topic 1", "description": "Details..."}},
            {{"topic": "Main Topic 2", "description": "Details..."}}
        ],
        "action_items": [
            {{"task": "Task description", "assignee": "Person Name", "deadline": "YYYY-MM-DD"}}
        ],
        "decisions": [
            {{"decision": "The final decision made", "context": "Reasoning..."}}
        ],
        "metadata": {{
            "meeting_type": "meeting",
            "language": "en"
        }},
        "transcript_preview": "A 200-word snippet of the dialogue..."
    }}
    
    Make it sound realistic, professional but natural.
    RETURN ONLY THE JSON. NO MARKDOWN.
    """
    
    response = llm.generate(prompt)
    
    # Clean up response (remove markdown code blocks if any)
    clean_json = response.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

def main():
    print("Initializing Synthetic Data Generator...")
    try:
        llm = get_llm()
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return

    print(f"Generating {len(SCENARIOS)} meetings...")
    
    for i, scenario in enumerate(SCENARIOS):
        try:
            print(f"Generating [{i+1}/{len(SCENARIOS)}]: {scenario[:40]}...")
            data = generate_meeting_content(llm, scenario)
            
            # Add system fields
            data["id"] = f"synthetic_{int(time.time())}_{i}"
            data["timestamp"] = (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            data["original_file"] = f"{data['title'].lower().replace(' ', '_')}.mp3"
            
            # Save
            path = HISTORY_DIR / f"{data['id']}.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"  Saved to {path.name}")
            
            # Sleep to avoid rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"  Failed to generate: {e}")

    print("\nGeneration Complete.")
    
    # Trigger Reindex
    try:
        from backend.data.history_searcher import HistorySearcher
        print("Triggering ChromaDB Re-index...")
        searcher = HistorySearcher()
        searcher.index_all_meetings(force_reindex=True)
        print("Re-index verified.")
    except Exception as e:
        print(f"Re-index failed: {e}")

if __name__ == "__main__":
    from datetime import datetime, timedelta
    main()
