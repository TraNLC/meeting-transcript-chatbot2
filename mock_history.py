import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.data.history_manager import HistoryManager
from src.rag.advanced_rag import get_rag_instance

def create_mock_history():
    manager = HistoryManager()
    print(f"Creating mock history in {manager.history_dir.absolute()}")
    
    # Initialize RAG
    try:
        rag = get_rag_instance(vector_store="chroma")
    except Exception as e:
        print(f"Warning: Could not init RAG: {e}")
        rag = None

    # Helper to add to RAG
    def add_to_rag(id, filename, summary, topics, meeting_type, language):
        if not rag: return
        
        # Create a rich text representation for RAG
        rag_text = f"Meeting: {filename}\nType: {meeting_type}\n\nSummary:\n{summary}\n\nTopics:\n"
        for t in topics:
            rag_text += f"- {t['topic']}: {t['description']}\n"
            
        metadata = {
            "meeting_type": meeting_type,
            "language": language,
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            rag.add_meeting(id, rag_text, metadata)
            print(f"Added {id} to RAG")
        except Exception as e:
            print(f"Failed to add {id} to RAG: {e}")

    # Mock Data 1: Today - Project Kickoff
    id1 = manager.save_analysis(
        filename="Project_Kickoff_Meeting.mp3",
        summary="## Tóm tắt cuộc họp\nCuộc họp khởi động dự án phát triển ứng dụng AI. Team đã thống nhất về công nghệ sử dụng (Python, Flask, React) và lộ trình phát triển trong 3 tháng tới.\n\n## Điểm chính\n- Sử dụng mô hình Agile/Scrum\n- Daily meeting vào 9:00 sáng\n- Demo sản phẩm mỗi 2 tuần",
        topics=[
            {"topic": "Tech Stack", "description": "Thống nhất sử dụng Python, Flask cho backend và React cho frontend."},
            {"topic": "Timeline", "description": "Dự án kéo dài 3 tháng, chia làm 6 sprint."}
        ],
        action_items=[
            {"task": "Setup Git repository", "assignee": "DevOps Team", "deadline": "Today"},
            {"task": "Draft database schema", "assignee": "Backend Lead", "deadline": "Tomorrow"}
        ],
        decisions=[
            {"decision": "Chọn Pinecone làm Vector DB", "context": "Hiệu năng tốt, dễ scale"},
            {"decision": "Sử dụng Gemini 1.5 Flash", "context": "Cân bằng giữa tốc độ và chi phí"}
        ],
        metadata={
            "language": "vi",
            "meeting_type": "meeting",
            "file_type": "audio",
            "speaker_diarization": True
        }
    )
    add_to_rag(id1, "Project_Kickoff_Meeting.mp3", "Cuộc họp khởi động dự án...", [{"topic": "Tech Stack", "description": "Python, Flask, React"}], "meeting", "vi")
    print("Created: Project Kickoff Meeting (Today)")

    # Mock Data 2: Yesterday - Marketing Strategy
    id2 = manager.save_analysis(
        filename="Marketing_Q4_Strategy.docx",
        summary="## Tổng quan\nChiến dịch Marketing Q4 sẽ tập trung vào social media và influencer marketing. Mục tiêu tăng 200% traffic và 50% conversion rate.\n\n## Ngân sách\nDự kiến chi 500 triệu VND cho quảng cáo Facebook và TikTok.",
        topics=[
            {"topic": "Social Media", "description": "Tăng cường bài viết trên Fanpage và LinkedIn"},
            {"topic": "KOLs", "description": "Hợp tác với 5 micro-influencers trong ngành tech"}
        ],
        action_items=[
            {"task": "Liên hệ KOLs", "assignee": "Marketing Manager", "deadline": "Next Week"},
            {"task": "Thiết kế banner", "assignee": "Design Team", "deadline": "Friday"}
        ],
        decisions=[
            {"decision": "Tăng ngân sách Ads", "context": "Cần đẩy mạnh doanh số cuối năm"}
        ],
        metadata={
            "language": "vi",
            "meeting_type": "brainstorming",
            "file_type": "text",
            "speaker_diarization": False
        }
    )
    add_to_rag(id2, "Marketing_Q4_Strategy.docx", "Chiến dịch Marketing Q4...", [{"topic": "Social Media", "description": "Tăng cường bài viết"}], "brainstorming", "vi")
    
    # Modify mtime to yesterday
    file2 = manager.history_dir / f"{id2}.json"
    yesterday_ts = (datetime.now() - timedelta(days=1)).timestamp()
    os.utime(file2, (yesterday_ts, yesterday_ts))
    print("Created: Marketing Strategy (Yesterday)")

    # Mock Data 3: Last Week - Product Review
    id3 = manager.save_analysis(
        filename="Product_Review_v1.wav",
        summary="## Review sản phẩm\nPhiên bản v1.0 hoạt động ổn định nhưng còn một số bug nhỏ ở tính năng Search. UI cần cải thiện thêm về trải nghiệm người dùng trên mobile.\n\n## Feedback\n- Search chậm khi dữ liệu lớn\n- Nút bấm trên mobile hơi nhỏ",
        topics=[
            {"topic": "Bug Report", "description": "Lỗi search và hiển thị trên mobile"},
            {"topic": "UX Improvement", "description": "Cần làm lại giao diện mobile responsive hơn"}
        ],
        action_items=[
            {"task": "Fix bug search", "assignee": "Backend Team", "deadline": "ASAP"},
            {"task": "Redesign Mobile UI", "assignee": "Frontend Team", "deadline": "Next Sprint"}
        ],
        decisions=[
            {"decision": "Delay release v1.1", "context": "Để fix hết bug tồn đọng"}
        ],
        metadata={
            "language": "vi",
            "meeting_type": "meeting",
            "file_type": "audio",
            "speaker_diarization": True
        }
    )
    add_to_rag(id3, "Product_Review_v1.wav", "Review sản phẩm v1.0...", [{"topic": "Bug Report", "description": "Lỗi search"}], "meeting", "vi")
    
    # Modify mtime to 7 days ago
    file3 = manager.history_dir / f"{id3}.json"
    last_week_ts = (datetime.now() - timedelta(days=7)).timestamp()
    os.utime(file3, (last_week_ts, last_week_ts))
    print("Created: Product Review (Last Week)")
    
    # Mock Data 4: Last Month - Monthly Report
    id4 = manager.save_analysis(
        filename="Monthly_Report_Nov.pdf",
        summary="## Báo cáo tháng 11\nDoanh thu đạt 120% kế hoạch. Nhân sự ổn định. Đã hoàn thành 90% các hạng mục công việc đề ra.\n\n## Khó khăn\n- Server thỉnh thoảng bị quá tải\n- Thiếu nhân sự tester",
        topics=[
            {"topic": "Revenue", "description": "Vượt chỉ tiêu 20%"},
            {"topic": "HR", "description": "Cần tuyển thêm 2 Tester"}
        ],
        action_items=[
            {"task": "Upgrade Server", "assignee": "DevOps", "deadline": "Next Month"},
            {"task": "Post job description", "assignee": "HR", "deadline": "Today"}
        ],
        decisions=[
            {"decision": "Thưởng nóng team Sales", "context": "Đạt KPI xuất sắc"}
        ],
        metadata={
            "language": "vi",
            "meeting_type": "meeting",
            "file_type": "text",
            "speaker_diarization": False
        }
    )
    add_to_rag(id4, "Monthly_Report_Nov.pdf", "Báo cáo tháng 11...", [{"topic": "Revenue", "description": "Vượt chỉ tiêu"}], "meeting", "vi")
    
    # Modify mtime to 35 days ago
    file4 = manager.history_dir / f"{id4}.json"
    last_month_ts = (datetime.now() - timedelta(days=35)).timestamp()
    os.utime(file4, (last_month_ts, last_month_ts))
    print("Created: Monthly Report (Last Month)")

if __name__ == "__main__":
    create_mock_history()
