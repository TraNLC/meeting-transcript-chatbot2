"""Create realistic meeting audio for testing.

Tạo file audio cuộc họp thực tế bằng gTTS.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

print("=" * 70)
print("TẠO AUDIO CUỘC HỌP MẪU")
print("=" * 70)
print()

# Meeting transcript (realistic Vietnamese meeting)
meeting_transcript = """
Xin chào mọi người, chúng ta bắt đầu cuộc họp nhé.

Hôm nay là ngày 29 tháng 11 năm 2024, chúng ta sẽ thảo luận về dự án Meeting Analyzer.

Trước tiên, anh Trí báo cáo tiến độ phát triển tính năng ghi âm.

Dạ, em đã hoàn thành module ghi âm và tích hợp Whisper để transcribe tự động. 
Hiện tại hỗ trợ 5 ngôn ngữ là Tiếng Việt, English, Japanese, Korean và Chinese.

Tốt lắm. Còn anh Khang, phần ChromaDB thế nào rồi?

Dạ em đã tích hợp xong ChromaDB để lưu trữ vector embeddings. 
Tính năng semantic search đã hoạt động tốt, có thể tìm kiếm theo nội dung thay vì chỉ tên file.

Rất tốt. Vậy chị Dung, phần testing đã kiểm tra những gì?

Dạ em đã tạo 28 test cases cho tất cả 7 tabs. 
Kết quả là 100% pass, không có lỗi nào.

Xuất sắc! Vậy chúng ta đã hoàn thành Sprint 3.

Các action items cho tuần tới:
- Anh Trí: Optimize transcription speed
- Anh Khang: Improve search ranking algorithm  
- Chị Dung: Prepare demo for presentation

Deadline là ngày 5 tháng 12.

Quyết định quan trọng: Chúng ta sẽ deploy lên production vào cuối tuần này.

Có câu hỏi gì không? Không có thì kết thúc cuộc họp. Cảm ơn mọi người!
"""

print("📝 Nội dung cuộc họp:")
print("-" * 70)
print(meeting_transcript)
print("-" * 70)
print()

try:
    from gtts import gTTS
    import os
    
    print("🔄 Đang tạo audio bằng gTTS...")
    
    # Create audio
    tts = gTTS(text=meeting_transcript, lang='vi', slow=False)
    
    # Save to file
    output_dir = Path("data/test_samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "meeting_sample_vi.mp3"
    tts.save(str(output_file))
    
    file_size = output_file.stat().st_size / 1024  # KB
    
    print(f"✅ Đã tạo file audio: {output_file}")
    print(f"   Kích thước: {file_size:.2f} KB")
    print()
    
    # Also create English version
    print("🔄 Đang tạo phiên bản tiếng Anh...")
    
    meeting_en = """
    Hello everyone, let's start the meeting.

    Today is November 29, 2024. We will discuss the Meeting Analyzer project.

    First, Tri will report on the audio recording feature development.

    Yes, I have completed the recording module and integrated Whisper for automatic transcription.
    Currently supporting 5 languages: Vietnamese, English, Japanese, Korean, and Chinese.

    Great. And Khang, how is the ChromaDB part?

    I have completed the ChromaDB integration for storing vector embeddings.
    The semantic search feature is working well, can search by content instead of just file names.

    Very good. So Dung, what have you tested?

    I have created 28 test cases for all 7 tabs.
    The result is 100% pass, no errors.

    Excellent! So we have completed Sprint 3.

    Action items for next week:
    - Tri: Optimize transcription speed
    - Khang: Improve search ranking algorithm
    - Dung: Prepare demo for presentation

    Deadline is December 5.

    Important decision: We will deploy to production this weekend.

    Any questions? If not, meeting adjourned. Thank you everyone!
    """
    
    tts_en = gTTS(text=meeting_en, lang='en', slow=False)
    output_file_en = output_dir / "meeting_sample_en.mp3"
    tts_en.save(str(output_file_en))
    
    file_size_en = output_file_en.stat().st_size / 1024
    
    print(f"✅ Đã tạo file audio: {output_file_en}")
    print(f"   Kích thước: {file_size_en:.2f} KB")
    print()
    
    print("=" * 70)
    print("✅ HOÀN THÀNH!")
    print("=" * 70)
    print()
    print("📁 Files đã tạo:")
    print(f"  1. {output_file}")
    print(f"  2. {output_file_en}")
    print()
    print("🧪 Để test transcription, chạy:")
    print(f"  python tests/test_transcription.py")
    print()
    
except ImportError:
    print("❌ Lỗi: Chưa cài gTTS")
    print()
    print("💡 Cài đặt:")
    print("  pip install gTTS")
    print()
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
