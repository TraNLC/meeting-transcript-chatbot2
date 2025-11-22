# 🎤 Hướng Dẫn Thuyết Trình - Phần 2

**Tiếp theo từ Slide 6**

---

### Slide 6: Lộ Trình 4 Sprint

**Tiêu đề**: 🗓️ Lộ Trình Phát Triển (4 Sprint)

**Nội dung**:
```
Sprint 1: Nền Tảng (16/11 - 6 giờ)
├─ ✅ Chatbot cơ bản với Gemini API
├─ ✅ Upload & xử lý file
├─ ✅ Tóm tắt & trích xuất thông tin
├─ ✅ Giao diện Gradio & export
└─ 📊 Tiến độ: 60%

Sprint 2: Multi-LLM (23/11 - 8 giờ)
├─ 🔄 Tích hợp OpenAI & Llama 3
├─ 🔄 Quản lý hội thoại
├─ 🔄 Function calling
└─ 🔄 Advanced prompting

Sprint 3: Vector DB & TTS (30/11 - 6 giờ)
├─ 📅 Tích hợp ChromaDB
├─ 📅 Tìm kiếm ngữ nghĩa
├─ 📅 Text-to-Speech (HuggingFace)
└─ 📅 Phản hồi bằng giọng nói

Sprint 4: RAG & LangChain (7/12 - 1 giờ)
├─ 📅 LangChain RAG pipeline
├─ 📅 FAISS/Pinecone vector store
├─ 📅 Retrieval nâng cao
└─ 📅 Production-ready

⏱️ Tổng thời gian: 21 giờ workshop
```

**Hình ảnh**:
- Timeline với các mốc thời gian
- Progress bar cho mỗi sprint
- Icon cho từng tính năng
- Màu sắc phân biệt sprint

**Lời thuyết trình**:
"Dự án được phát triển qua 4 sprint. Sprint 1 xây dựng nền tảng với các tính năng cơ bản. Sprint 2 thêm hỗ trợ nhiều LLM. Sprint 3 tích hợp vector database và text-to-speech. Sprint 4 triển khai RAG production-ready với LangChain."

---

### Slide 7: Sprint 1 - Nền Tảng

**Tiêu đề**: 🚀 Sprint 1: Xây Dựng Nền Tảng

**Nội dung**:
```
📅 Workshop: 16/11/2025 (6 giờ)
📊 Tiến độ: 60% hoàn thành

✅ Tính năng đã hoàn thành:

1. 📁 Xử Lý File
   • Upload file TXT/DOCX
   • Làm sạch văn bản
   • Validation định dạng
   • Giới hạn 15,000 ký tự

2. 🤖 Tích Hợp AI
   • Google Gemini API
   • Thiết kế prompts chuyên biệt
   • Xử lý lỗi
   • Retry logic

3. 📊 Trích Xuất Thông Tin
   • Tóm tắt cuộc họp (3-5 câu)
   • Action items (công việc, người phụ trách, deadline)
   • Chủ đề chính (3-5 topics)
   • Quyết định quan trọng

4. 🎨 Giao Diện Người Dùng
   • Giao diện Gradio sạch đẹp
   • Xử lý real-time
   • Export TXT/DOCX
   • Hỗ trợ 5 ngôn ngữ

💪 Điểm mạnh:
• Nhanh (30-60 giây)
• Chính xác (85%+)
• Dễ sử dụng
• Miễn phí (Gemini API)
```

**Hình ảnh**:
- Screenshots các tính năng
- Ví dụ input/output
- Biểu đồ tiến độ
- Demo GIF

**Lời thuyết trình**:
"Trong Sprint 1, chúng em đã xây dựng nền tảng với xử lý file, tích hợp Gemini API, các tính năng trích xuất thông tin, và giao diện Gradio. Hiện tại đã hoàn thành 60% và sẵn sàng cho workshop."

---

### Slide 8: Sprint 2 - Multi-LLM

**Tiêu đề**: 🔄 Sprint 2: Kiến Trúc Multi-LLM

**Nội dung**:
```
📅 Workshop: 23/11/2025 (8 giờ)

🎯 Mục tiêu:

1. 🤖 Hỗ Trợ Nhiều LLM
   • OpenAI (GPT-3.5/4)
   • Llama 3 (Ollama/Groq)
   • Gemini (hiện tại)
   • Factory pattern
   • Dễ dàng thêm provider mới

2. 💬 Quản Lý Hội Thoại
   • Hội thoại nhiều lượt
   • Giữ ngữ cảnh
   • Lịch sử tin nhắn
   • Export conversations
   • Context window management

3. 🛠️ Function Calling
   • Tìm kiếm trong transcript
   • Lấy action items theo người
   • Trích xuất thông tin cụ thể
   • Truy vấn động
   • Kết nối external APIs

4. 🎯 Tính Năng Nâng Cao
   • Few-shot prompting
   • Chain-of-thought reasoning
   • Batching requests
   • Retry logic
   • Streaming responses

🔧 Kiến trúc:
Abstract Interface → Factory → Providers
                                ├─ Gemini
                                ├─ OpenAI
                                └─ Llama
```

**Hình ảnh**:
- Sơ đồ kiến trúc multi-LLM
- Luồng conversation
- Ví dụ function calling
- So sánh các LLM

**Lời thuyết trình**:
"Sprint 2 tập trung vào kiến trúc multi-LLM, cho phép người dùng chọn giữa OpenAI, Llama 3 hoặc Gemini. Chúng em sẽ thêm quản lý hội thoại cho các cuộc trò chuyện nhiều lượt và function calling để truy vấn động."

---

### Slide 9: Sprint 3 - Vector DB & TTS

**Tiêu đề**: 🗄️ Sprint 3: Vector Database & Text-to-Speech

**Nội dung**:
```
📅 Workshop: 30/11/2025 (6 giờ)

🎯 Mục tiêu:

1. 🗄️ Tích Hợp ChromaDB
   • Lưu trữ biên bản họp
   • Vector embeddings
   • Tìm kiếm ngữ nghĩa
   • Knowledge base

2. 🔍 Tìm Kiếm Ngữ Nghĩa
   • Tìm cuộc họp tương tự
   • Retrieval theo ngữ cảnh
   • Độ chính xác cao hơn
   • Truy vấn nhanh hơn

3. 🔊 Text-to-Speech
   • HuggingFace TTS (VITS)
   • Phản hồi bằng giọng nói
   • Tăng khả năng tiếp cận
   • Hỗ trợ nhiều ngôn ngữ

4. 💬 Chatbot Nâng Cao
   • Q&A trên nhiều transcript
   • Phản hồi bằng giọng nói
   • Hiểu ngữ cảnh tốt hơn
   • Tìm kiếm thông minh

📊 Lợi ích:
• Tìm kiếm nhanh hơn 10x
• Chính xác hơn 20%
• Hỗ trợ người khuyết tật
• Trải nghiệm tốt hơn
```

**Hình ảnh**:
- Sơ đồ vector database
- Visualization tìm kiếm ngữ nghĩa
- Workflow TTS
- Audio waveform
- So sánh keyword vs semantic search

**Lời thuyết trình**:
"Sprint 3 thêm ChromaDB để lưu trữ transcript dưới dạng vectors, cho phép tìm kiếm ngữ nghĩa trên nhiều cuộc họp. Chúng em cũng tích hợp HuggingFace Text-to-Speech để chatbot có thể phản hồi bằng giọng nói, tăng khả năng tiếp cận."

---

### Slide 10: Sprint 4 - RAG & LangChain

**Tiêu đề**: 🎓 Sprint 4: Production RAG

**Nội dung**:
```
📅 Workshop: 7/12/2025 (1 giờ)

🎯 Mục tiêu:

1. 🔗 Tích Hợp LangChain
   • RAG pipeline
   • Retrieval chains
   • Quản lý prompts
   • Chain composition

2. 📊 Vector Stores
   • FAISS (local, nhanh)
   • Pinecone (cloud, scalable)
   • Retrieval hiệu quả
   • Khả năng mở rộng

3. 🎯 Retrieval Nâng Cao
   • MMR (Maximal Marginal Relevance)
   • Reranking
   • Source citation
   • Context optimization

4. 🚀 Production Ready
   • Error handling toàn diện
   • Monitoring & logging
   • Performance optimization
   • Deployment guide
   • Cost optimization

🏆 Kết quả:
• Hệ thống production-ready
• Scalable & maintainable
• Best practices
• Sẵn sàng deploy
```

**Hình ảnh**:
- Sơ đồ kiến trúc RAG
- LangChain workflow
- Performance metrics
- Deployment pipeline
- Before/After comparison

**Lời thuyết trình**:
"Sprint 4 triển khai RAG production-ready sử dụng LangChain. Chúng em tích hợp FAISS hoặc Pinecone cho vector storage, thêm các chiến lược retrieval nâng cao, và chuẩn bị hệ thống cho production deployment."

---


### Slide 11: Cách Chatbot Hoạt Động

**Tiêu đề**: ⚙️ Chatbot Hoạt Động Như Thế Nào?

**Nội dung**:
```
Quy Trình 5 Bước:

1️⃣ Upload Transcript
   📄 Người dùng upload file meeting (TXT/DOCX)
   ↓

2️⃣ Tiền Xử Lý
   • Làm sạch văn bản (xóa khoảng trắng thừa)
   • Kiểm tra định dạng
   • Cắt ngắn nếu quá dài (max 15k ký tự)
   • Chuẩn hóa encoding
   ↓

3️⃣ Phân Tích AI
   • Gửi đến LLM (Gemini/OpenAI)
   • Sử dụng prompts chuyên biệt cho từng task
   • Trích xuất thông tin có cấu trúc
   • Parse JSON response
   ↓

4️⃣ Trích Xuất Thông Tin
   ┌──────────────────────────────────┐
   │ 📝 Tóm tắt: Overview 3-5 câu     │
   │ 🎯 Topics: Các chủ đề chính      │
   │ ✅ Actions: Công việc + deadline │
   │ 🎯 Decisions: Quyết định quan trọng│
   └──────────────────────────────────┘
   ↓

5️⃣ Hiển Thị & Export
   • Hiển thị kết quả trên UI
   • Export sang TXT/DOCX
   • Lưu để tham khảo sau

⏱️ Thời gian: 30-60 giây
🎯 Độ chính xác: 85%+
```

**Hình ảnh**:
- Flowchart với icons
- Ví dụ input/output thực tế
- Animation xử lý
- Chỉ số thời gian

**Lời thuyết trình**:
"Chatbot hoạt động qua 5 bước: Upload transcript, tiền xử lý văn bản, gửi đến AI để phân tích, trích xuất thông tin có cấu trúc bằng prompts chuyên biệt, và hiển thị kết quả với tùy chọn export. Toàn bộ quá trình mất 30-60 giây với độ chính xác trên 85%."

---

### Slide 12: Demo Trực Tiếp

**Tiêu đề**: 🎬 Demo Trực Tiếp

**Nội dung**:
```
Kịch bản Demo:
Cuộc họp lập kế hoạch ra mắt sản phẩm

📥 Input:
• Biên bản họp (500 từ)
• Người tham gia: Alice (PM), Bob (Dev), Charlie (Marketing)
• Nội dung: Timeline, tính năng, ngân sách

📤 Kết quả mong đợi:

✅ Tóm tắt:
   "Cuộc họp bàn về kế hoạch ra mắt sản phẩm 
   vào ngày 1/12/2025. Các chủ đề chính: timeline, 
   payment integration, marketing campaign, và ngân sách."

✅ Action Items:
   • Bob: Hoàn thành payment integration (20/11)
   • Charlie: Chuẩn bị marketing campaign (25/11)

✅ Topics:
   • Timeline ra mắt sản phẩm
   • Tích hợp thanh toán
   • Chiến dịch marketing
   • Thảo luận ngân sách

✅ Decisions:
   • Ngày ra mắt: 1/12/2025
   • Ngân sách marketing: $5000 được phê duyệt

[DEMO TRỰC TIẾP TRÊN MÀN HÌNH]
```

**Hình ảnh**:
- Split screen: Input bên trái | Output bên phải
- Highlight thông tin quan trọng
- Loading indicator
- Kết quả xuất hiện từng phần

**Lời thuyết trình**:
"Bây giờ em xin demo trực tiếp. Em sẽ upload một biên bản họp mẫu về kế hoạch ra mắt sản phẩm. Các bạn sẽ thấy chatbot tự động trích xuất tóm tắt, topics, action items và decisions trong thời gian thực."

**Các bước demo**:
1. Mở http://localhost:7861
2. Upload file sample_meeting.txt
3. Click "🚀 Xử lý Transcript"
4. Chờ 30-60 giây
5. Giải thích từng phần kết quả
6. Click "📝 Xuất file DOCX"
7. Mở file vừa export
8. Kết thúc demo

---

### Slide 13: Công Nghệ Sử Dụng

**Tiêu đề**: 🛠️ Tech Stack & Công Nghệ

**Nội dung**:
```
Backend & AI:
├─ 🐍 Python 3.11+
│  └─ Ngôn ngữ chính, dễ phát triển AI
├─ 🤖 Google Gemini API
│  └─ LLM miễn phí, nhanh, chính xác
├─ 🤖 OpenAI API (Sprint 2)
│  └─ GPT-3.5/4 cho độ chính xác cao
└─ 🦙 Llama 3 (Sprint 2)
   └─ Open-source, chạy local

Frontend & UI:
├─ 🎨 Gradio 4.0+
│  └─ Tạo UI nhanh, đẹp, responsive
└─ 📱 Responsive Design
   └─ Hoạt động trên mọi thiết bị

Data Processing:
├─ 📄 python-docx
│  └─ Xử lý file Word
├─ 🧹 Text Preprocessing
│  └─ Làm sạch & chuẩn hóa
└─ 📊 JSON Parsing
   └─ Trích xuất dữ liệu có cấu trúc

AI/ML Techniques:
├─ 🎯 Prompt Engineering
│  └─ Thiết kế prompts hiệu quả
├─ 📚 Few-shot Learning
│  └─ Học từ ví dụ
├─ 🧠 Chain-of-thought
│  └─ Suy luận từng bước
└─ 🔍 RAG (Sprint 4)
   └─ Retrieval Augmented Generation

Database & Storage:
├─ 🗄️ ChromaDB (Sprint 3)
│  └─ Vector database
├─ 📊 FAISS (Sprint 4)
│  └─ Fast similarity search
└─ ☁️ Pinecone (Sprint 4)
   └─ Cloud vector database

Framework:
└─ 🔗 LangChain (Sprint 4)
   └─ RAG framework, chain management

Development Tools:
├─ 🔧 Git & GitHub
├─ 🧪 pytest (Testing)
├─ 📝 Markdown (Documentation)
└─ 🐳 Docker (Future)
```

**Hình ảnh**:
- Logo các công nghệ
- Sơ đồ tích hợp
- Tech stack layers
- Version numbers

**Lời thuyết trình**:
"Tech stack của chúng em bao gồm Python 3.11+ với Gemini/OpenAI APIs, Gradio cho UI, LangChain cho RAG, và ChromaDB cho vector storage. Chúng em sử dụng các kỹ thuật AI hiện đại như prompt engineering, few-shot learning, và RAG."

---

### Slide 14: Bài Học & Kinh Nghiệm

**Tiêu đề**: 💡 Bài Học Kinh Nghiệm

**Nội dung**:
```
✅ Những gì làm tốt:

1. 👥 Làm Việc Nhóm
   • Phân chia vai trò rõ ràng
   • Giao tiếp hiệu quả
   • Hỗ trợ lẫn nhau
   • Daily standup meetings

2. 🔧 Quyết Định Kỹ Thuật
   • Gemini API: Nhanh & miễn phí
   • Gradio: Dễ sử dụng, UI đẹp
   • Kiến trúc modular: Dễ mở rộng
   • Git workflow: Quản lý code tốt

3. 📈 Quy Trình Phát Triển
   • Sprint-based: Tập trung từng giai đoạn
   • Incremental: Phát triển dần dần
   • Testing thường xuyên
   • Documentation đầy đủ

⚠️ Thách thức gặp phải:

1. 🚫 API Rate Limits
   • Vấn đề: Gemini giới hạn 15 requests/phút
   • Giải pháp: Caching & retry logic

2. 📊 JSON Parsing từ LLM
   • Vấn đề: LLM không luôn trả về đúng format
   • Giải pháp: Robust parsing, fallback logic

3. ⏰ Thời Gian Hạn Chế
   • Vấn đề: 6-8 giờ workshop không nhiều
   • Giải pháp: Focus vào core features

4. 🔗 Tích Hợp Phức Tạp
   • Vấn đề: Nhiều components cần tích hợp
   • Giải pháp: Abstract interfaces, testing

🎯 Bài học quan trọng:
✓ Bắt đầu đơn giản, iterate nhanh
✓ Test sớm và thường xuyên
✓ Document trong khi code
✓ Backward compatibility quan trọng
✓ Communication là chìa khóa
✓ Chuẩn bị kỹ trước workshop
```

**Hình ảnh**:
- Icon success/challenge
- Timeline bài học
- Ảnh team collaboration
- Biểu đồ giải quyết vấn đề

**Lời thuyết trình**:
"Chúng em học được tầm quan trọng của phân chia vai trò rõ ràng và giao tiếp tốt. Gặp thách thức về API rate limits và JSON parsing, nhưng đã giải quyết bằng caching và error handling. Bài học quan trọng: bắt đầu đơn giản và iterate nhanh."

---
