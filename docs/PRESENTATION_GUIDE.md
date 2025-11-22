# 🎤 Hướng Dẫn Thuyết Trình - Meeting Transcript Chatbot

**Team**: Team 3 - Akatsuki  
**Dự án**: Chatbot Phân Tích Biên Bản Cuộc Họp  
**Thời lượng**: 10-15 phút  
**Số slide**: 15 slides

---

## 📊 Danh Sách Slides

### Slide 1: Trang Bìa
### Slide 2: Giới Thiệu Team
### Slide 3: Tổng Quan Dự Án
### Slide 4: Vấn Đề Cần Giải Quyết
### Slide 5: Kiến Trúc Giải Pháp
### Slide 6: Lộ Trình 4 Sprint
### Slide 7: Sprint 1 - Nền Tảng
### Slide 8: Sprint 2 - Multi-LLM
### Slide 9: Sprint 3 - Vector DB & TTS
### Slide 10: Sprint 4 - RAG & LangChain
### Slide 11: Cách Chatbot Hoạt Động
### Slide 12: Demo Trực Tiếp
### Slide 13: Công Nghệ Sử Dụng
### Slide 14: Bài Học Kinh Nghiệm
### Slide 15: Hỏi Đáp

---

## 📝 Nội Dung Chi Tiết Từng Slide

---

### Slide 1: Trang Bìa

**Bố cục**: Căn giữa, thiết kế sạch đẹp

**Nội dung**:
```
🔥 Team 3 - Akatsuki

Chatbot Phân Tích Biên Bản Cuộc Họp
Hệ Thống Phân Tích Meeting Tự Động Bằng AI

AI Application Engineer Learning Path
Tháng 11/2025
```

**Hình ảnh**: 
- Logo team
- Icon chatbot + meeting
- Background gradient (tím/xanh)

**Lời thuyết trình**:
"Xin chào mọi người. Chúng em là Team Akatsuki, hôm nay chúng em xin trình bày dự án Chatbot Phân Tích Biên Bản Cuộc Họp."

---

### Slide 2: Giới Thiệu Team

**Tiêu đề**: 👥 Team Akatsuki - 7 Thành Viên

**Nội dung**:
```
🔥 Team 3 - Akatsuki

┌─────────────────────────────────────────────┐
│ Khang Vo Duy                                │
│ 🤖 Chuyên Gia Tích Hợp LLM                 │
│ • Tích hợp OpenAI/Gemini API                │
│ • Thiết kế prompts                          │
│ • Tối ưu hóa responses                      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Hoang Le Viet                               │
│ 📊 Kỹ Sư Xử Lý Dữ Liệu                     │
│ • Load & xử lý file (TXT/DOCX)              │
│ • Tiền xử lý văn bản                        │
│ • Validation dữ liệu                        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Hoang Pham Minh                             │
│ 🧠 Kỹ Sư RAG & Logic Chatbot (Lead)       │
│ • Kiến trúc chatbot                         │
│ • Trích xuất thông tin                      │
│ • Tổng hợp & phân tích                      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Tri Nguyen Quoc                             │
│ 🧠 Kỹ Sư RAG & Logic Chatbot (Support)    │
│ • Các tính năng trích xuất                  │
│ • Xử lý JSON                                │
│ • Error handling                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Huy Bui Ngoc Phuc                           │
│ 🎨 Lập Trình Viên UI/UX                    │
│ • Thiết kế giao diện Gradio                 │
│ • Trải nghiệm người dùng                    │
│ • Export kết quả                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Dung Nguyen Thi                             │
│ 🧪 Kỹ Sư QA & Kiểm Thử                     │
│ • Kiểm thử chất lượng                       │
│ • Theo dõi bugs                             │
│ • Đảm bảo chất lượng sản phẩm               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ [Team Lead]                                 │
│ 📊 Trưởng Nhóm & Thuyết Trình              │
│ • Điều phối dự án                           │
│ • Tài liệu hóa                              │
│ • Thuyết trình & demo                       │
└─────────────────────────────────────────────┘
```

**Hình ảnh**:
- Ảnh các thành viên (nếu có)
- Icon cho từng vai trò
- Khung màu phân biệt

**Lời thuyết trình**:
"Team chúng em gồm 7 thành viên với vai trò chuyên môn rõ ràng. Khang phụ trách tích hợp LLM, Hoang Le Viet xử lý dữ liệu, Hoang Pham Minh và Tri phát triển logic chatbot, Huy thiết kế giao diện, Dung đảm bảo chất lượng, và em điều phối dự án."

---

Tôi sẽ tiếp tục với file append để không vượt quá giới hạn...


### Slide 3: Tổng Quan Dự Án

**Tiêu đề**: 💬 Chatbot Phân Tích Biên Bản Cuộc Họp

**Nội dung**:
```
📋 Dự án là gì?
Hệ thống AI tự động phân tích biên bản cuộc họp 
và trích xuất thông tin quan trọng

🎯 Tính năng chính:
✅ Tóm tắt cuộc họp tự động
✅ Trích xuất action items (công việc, người phụ trách, deadline)
✅ Nhận diện quyết định quan trọng
✅ Xác định chủ đề chính
✅ Hỗ trợ 5 ngôn ngữ
✅ Xuất kết quả (TXT/DOCX)

🚀 Công nghệ:
• Google Gemini AI / OpenAI
• Python 3.11+
• Giao diện Gradio
• LangChain (Sprint 4)

⏱️ Thời gian xử lý: 30-60 giây
```

**Hình ảnh**:
- Screenshot ứng dụng
- Icon các tính năng
- Logo công nghệ

**Lời thuyết trình**:
"Chatbot của chúng em sử dụng AI để tự động phân tích biên bản cuộc họp, tạo tóm tắt, trích xuất action items với người phụ trách và deadline, nhận diện quyết định quan trọng và các chủ đề chính được thảo luận."

---

### Slide 4: Vấn Đề Cần Giải Quyết

**Tiêu đề**: 🤔 Vấn Đề Hiện Tại

**Nội dung**:
```
❌ Thách thức hiện nay:

1. ⏰ Tốn Thời Gian
   • Ghi chép thủ công mất 30-60 phút
   • Đọc lại biên bản dài rất mệt mỏi
   • Khó tìm kiếm thông tin cũ

2. 😰 Mất Thông Tin
   • Action items quan trọng bị bỏ sót
   • Quyết định không được ghi chép rõ ràng
   • Quên follow-up công việc

3. 📊 Không Hiệu Quả
   • Khó tìm kiếm trong các cuộc họp cũ
   • Không có format chuẩn
   • Khó theo dõi tiến độ

💡 Giải pháp của chúng em:
Tự động hóa toàn bộ quy trình bằng AI!

📈 Lợi ích:
• Tiết kiệm 80% thời gian
• Không bỏ sót thông tin
• Dễ dàng tìm kiếm & theo dõi
```

**Hình ảnh**:
- So sánh Trước/Sau
- Icon các pain points
- Biểu đồ tiết kiệm thời gian

**Lời thuyết trình**:
"Hiện tại, các team phải mất 30-60 phút để ghi chép và đọc lại biên bản họp. Action items quan trọng thường bị bỏ sót, quyết định không được ghi chép rõ ràng. Giải pháp của chúng em tự động hóa toàn bộ quy trình này bằng AI, tiết kiệm 80% thời gian."

---

### Slide 5: Kiến Trúc Giải Pháp

**Tiêu đề**: 🏗️ Kiến Trúc Hệ Thống

**Nội dung**:
```
┌─────────────┐
│  Người dùng │
│  (Upload)   │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────┐
│   Tầng Xử Lý File                   │
│  • Load TXT/DOCX                    │
│  • Tiền xử lý văn bản               │
│  • Validation                       │
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│   Tầng Xử Lý AI                     │
│  • Tích hợp LLM (Gemini/OpenAI)     │
│  • Prompt Engineering               │
│  • Trích xuất thông tin             │
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│   Tầng Phân Tích                    │
│  • Tạo tóm tắt                      │
│  • Trích xuất Action Items          │
│  • Nhận diện Topics                 │
│  • Xác định Decisions               │
└──────┬──────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────┐
│   Tầng Hiển Thị                     │
│  • Giao diện Gradio                 │
│  • Export TXT/DOCX                  │
└─────────────────────────────────────┘
```

**Hình ảnh**:
- Sơ đồ kiến trúc với mũi tên
- Các khối component có icon
- Luồng dữ liệu trực quan

**Lời thuyết trình**:
"Hệ thống của chúng em có 4 tầng chính: Tầng Xử Lý File nhận và tiền xử lý dữ liệu, Tầng AI sử dụng LLM để phân tích, Tầng Phân Tích trích xuất thông tin cụ thể, và Tầng Hiển Thị xuất kết quả cho người dùng."

---
