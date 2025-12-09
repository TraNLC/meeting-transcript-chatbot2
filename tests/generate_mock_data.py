"""
Generate Mock Data for Testing (Normal & Abnormal)

Generates diverse meeting history files in `data/history` for comprehensive testing.
Includes:
1. Normal scenarios (VI/EN, diverse types)
2. Abnormal scenarios (Edge cases, missing data, huge content, unicode)

Run: python tests/generate_mock_data.py
"""

import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# Use absolute path based on execution context or relative to script if run from root
HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# --- HELPER DATA ---

NORMAL_TITLES_VI = [
    "Họp giao ban tuần", "Phỏng vấn ứng viên Senior Dev", "Review dự án ChatBot",
    "Brainstorming tính năng mới", "Họp với khách hàng Nhật Bản", "Đào tạo nhân sự mới",
    "Gặp gỡ đối tác chiến lược", "Báo cáo tài chính Q4"
]

NORMAL_TITLES_EN = [
    "Weekly Sync", "Candidate Interview - John Doe", "Project Kickoff",
    "Design Review", "Client Feedback Session", "All-Hands Meeting",
    "Architecture Discussion", "Sprint Planning"
]

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50

# --- DATA GENERATORS ---

def generate_normal_meeting_vi(index):
    """Generate a standard Vietnamese meeting."""
    date = datetime.now() - timedelta(days=random.randint(0, 30))
    meeting_id = f"{date.strftime('%Y%m%d')}_vi_normal_{index}"
    title = random.choice(NORMAL_TITLES_VI)
    
    return {
        "id": meeting_id,
        "original_file": f"{title}.mp3",
        "timestamp": date.isoformat(),
        "summary": f"Tóm tắt cuộc họp '{title}'. Mọi người đã thảo luận về tiến độ và các vấn đề tồn đọng. Team thống nhất sẽ đẩy nhanh tiến độ trong tuần tới.",
        "topics": [
            {"topic": "Tiến độ dự án", "description": "Dự án đang chậm 2 ngày so với kế hoạch."},
            {"topic": "Nhân sự", "description": "Cần tuyển thêm 1 Backend Dev."}
        ],
        "action_items": [
            {"task": "Gửi báo cáo tuần", "assignee": "Nguyễn Văn A", "deadline": "2023-12-15"},
            {"task": "Đăng tin tuyển dụng", "assignee": "Tran Thi B", "deadline": "2023-12-20"}
        ],
        "decisions": [
            {"decision": "Dời ngày release", "context": "Do chưa fix xong bug nghiêm trọng."}
        ],
        "metadata": {
            "meeting_type": random.choice(["meeting", "interview", "brainstorm"]),
            "language": "vi",
            "duration": 3600
        }
    }

def generate_normal_meeting_en(index):
    """Generate a standard English meeting."""
    date = datetime.now() - timedelta(days=random.randint(0, 30))
    meeting_id = f"{date.strftime('%Y%m%d')}_en_normal_{index}"
    title = random.choice(NORMAL_TITLES_EN)
    
    return {
        "id": meeting_id,
        "original_file": f"{title}.wav",
        "timestamp": date.isoformat(),
        "summary": f"Summary for '{title}'. The team discussed key milestones and deliverables. Everyone agreed on the new roadmap.",
        "topics": [
            {"topic": "Q4 Roadmap", "description": "Reviewed quarter goals."},
            {"topic": "Budget", "description": "Budget approval pending for new tools."}
        ],
        "action_items": [
            {"task": "Update documentation", "assignee": "John Smith", "deadline": "2023-12-18"},
            {"task": "Schedule follow-up", "assignee": "Sarah", "deadline": "2023-12-12"}
        ],
        "decisions": [
            {"decision": "Adopt new framework", "context": "Better performance benchmarks."}
        ],
        "metadata": {
            "meeting_type": random.choice(["meeting", "presentation"]),
            "language": "en",
            "duration": 1800
        }
    }

def generate_abnormal_empty(index):
    """Generate a meeting with minimal/empty content."""
    date = datetime.now() - timedelta(days=random.randint(0, 60))
    meeting_id = f"abnormal_empty_{index}"
    
    return {
        "id": meeting_id,
        "original_file": "empty_recording.mp3",
        "timestamp": date.isoformat(),
        "summary": "",
        "topics": [],
        "action_items": [],
        "decisions": [],
        "metadata": {
            "meeting_type": "meeting",
            "language": "en"
        }
    }

def generate_abnormal_huge(index):
    """Generate a meeting with massive content."""
    date = datetime.now()
    meeting_id = f"abnormal_huge_{index}"
    
    huge_summary = LOREM_IPSUM * 100  # Very long summary
    huge_topics = [{"topic": f"Topic {i}", "description": LOREM_IPSUM} for i in range(50)]
    
    return {
        "id": meeting_id,
        "original_file": "huge_log_dump.txt",
        "timestamp": date.isoformat(),
        "summary": huge_summary,
        "topics": huge_topics,
        "action_items": [],
        "decisions": [],
        "metadata": {
            "meeting_type": "brainstorm"
        }
    }

def generate_abnormal_unicode(index):
    """Generate content with complex Unicode/Emojis."""
    date = datetime.now()
    meeting_id = f"abnormal_unicode_{index}"
    
    return {
        "id": meeting_id,
        "original_file": "🦄🌈_weird_names_عربي_中文.mp3",
        "timestamp": date.isoformat(),
        "summary": "Meeting about 🆘 critical issues! 🚀 Launch succeeded but server 🔥 caught fire. Test chars: Ã, Ñ, Ā, 😺, 😹, 😻.",
        "topics": [
            {"topic": "Unicode Stress Test 🧪", "description": "Testing: ﷽, 🏳️‍🌈, 👨‍👩‍👧‍👦"}
        ],
        "action_items": [],
        "decisions": [],
        "metadata": {
            "meeting_type": "meeting",
            "language": "vi"
        }
    }

def generate_abnormal_future(index):
    """Generate a meeting with a future date."""
    date = datetime.now() + timedelta(days=3650) # 10 years later
    meeting_id = f"abnormal_future_{index}"
    
    return {
        "id": meeting_id,
        "original_file": "future_prediction.wav",
        "timestamp": date.isoformat(),
        "summary": "This meeting shouldn't exist yet.",
        "metadata": {"meeting_type": "meeting"}
    }

def generate_abnormal_missing_fields(index):
    """Generate structure with missing key fields."""
    date = datetime.now()
    meeting_id = f"abnormal_broken_{index}"
    
    return {
        # Missing 'id', 'original_file' is mostly used but we'll include minimal valid JSON
        "summary": "This file is missing ID and Timestamp.",
        "topics": [{"topic": "Unknown"}]
        # No metadata
    }

# --- MAIN GENERATOR ---

def generate_data():
    print(f"Generating mock data in: {HISTORY_DIR.absolute()}")
    
    files_created = 0
    
    # 1. Normal Data (20 files)
    print("- Generating Normal Data (VN/EN)...")
    for i in range(10):
        data = generate_normal_meeting_vi(i)
        with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        files_created += 1
        
        data = generate_normal_meeting_en(i)
        with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        files_created += 1

    # 2. Abnormal Data (10 files)
    print("- Generating Abnormal Data...")
    
    # Empty
    data = generate_abnormal_empty(1)
    with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    files_created += 1
    
    # Huge
    data = generate_abnormal_huge(1)
    with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    files_created += 1
    
    # Unicode
    data = generate_abnormal_unicode(1)
    with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    files_created += 1
    
    # Future
    data = generate_abnormal_future(1)
    with open(HISTORY_DIR / f"{data['id']}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    files_created += 1
    
    # Missing Fields (Might break strict readers, but good for testing robustness)
    data = generate_abnormal_missing_fields(1)
    # We name it with a UUID so it doesn't conflict, but it lacks an internal ID
    with open(HISTORY_DIR / f"broken_{uuid.uuid4()}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    files_created += 1

    print(f"DONE! Created {files_created} mock history files.")

if __name__ == "__main__":
    generate_data()
