# 💬 Meeting Note Summarization Chat bot

An intelligent meeting analysis system using **Google Gemini AI** to generate summaries and extract important information from meeting transcripts.

## ✨ Features

- 📝 **Automatic Summarization**: Generate concise summaries in Vietnamese
- ✅ **Action Items Extraction**: Find all tasks, assignees, and deadlines
- 🎯 **Decision Detection**: Identify important decisions
- 📌 **Topic Recognition**: Extract main topics discussed
- 💾 **Export Results**: Save analysis to TXT or DOCX files

## 🛠️ Technology

- **Python 3.11+**
- **Google Gemini 2.5 Flash**: Free AI model
- **Gradio**: User interface
- **python-docx**: Word file processing

---

## 🚀 Cài đặt nhanh (5 phút)

### 1. Clone và cài đặt

```bash
# Clone repository
git clone <repository-url>
cd meeting-transcript-chatbot

# Tạo virtual environment
python -m venv venv

# Kích hoạt
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Cấu hình API Key

```bash
# Tạo file .env
copy .env.example .env         # Windows
cp .env.example .env           # Linux/Mac
```

**Lấy Gemini API Key (MIỄN PHÍ):**
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google
3. Nhấn "Create API Key"
4. Copy API key

**Mở file `.env` và dán API key:**

```env
# API Key
GEMINI_API_KEY=your-gemini-api-key-here

# Cấu hình (Đã cố định)
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash
TEMPERATURE=0.7
MAX_TOKENS=4000
OUTPUT_LANGUAGE=vi
```

### 3. Chạy ứng dụng

```bash
python src/ui/gradio_app.py
```

Trình duyệt sẽ tự động mở tại: **http://localhost:7861**

### 4. Sử dụng

1. **Upload** file transcript (TXT hoặc DOCX)
2. **Nhấn** "🚀 Xử lý Transcript"
3. **Đợi** 30-60 giây (có loading indicator)
4. **Xem** kết quả phân tích:
   - 📝 Tóm tắt cuộc họp
   - 🎯 Chủ đề chính
   - ✅ Action Items
   - 🎯 Quyết định quan trọng
5. **Xuất** kết quả:
   - 📄 Xuất file TXT
   - 📝 Xuất file DOCX

---

## 📁 Cấu trúc Project

```
meeting-transcript-chatbot/
├── src/
│   ├── config/          # Cấu hình
│   ├── data/            # Load & xử lý dữ liệu
│   ├── llm/             # Tích hợp Gemini
│   ├── rag/             # Logic chatbot
│   └── ui/              # Giao diện Gradio
├── data/
│   └── transcripts/     # File transcript mẫu
├── tests/               # Unit tests
├── .env.example         # Template cấu hình
├── requirements.txt     # Thư viện cần thiết
└── README.md           # File này
```

---
## 📖 Hướng dẫn chi tiết

### File transcript mẫu

Sử dụng file: `data/transcripts/sample_meeting.txt`

### Câu hỏi mẫu (nếu có tính năng Q&A)

```
- Ai phụ trách phần thiết kế?
- Deadline của tích hợp thanh toán là khi nào?
- Ngân sách marketing là bao nhiêu?
- Ngày ra mắt chính thức là khi nào?
```

### Quy trình xử lý

```
1. Upload Transcript (TXT/DOCX)
   ↓
2. Tiền xử lý: Làm sạch → Cắt ngắn → Lưu vào bộ nhớ
   ↓
3. Tạo Prompt (System + User)
   ↓
4. Gửi → Gemini API
   ↓
5. AI tạo phản hồi
   ↓
6. Hiển thị kết quả
   ↓
7. Xuất file (TXT/DOCX)
```

---

## ❌ Xử lý lỗi

### "GEMINI_API_KEY not found"
```bash
# Kiểm tra file .env tồn tại
# Đảm bảo có dòng: GEMINI_API_KEY=...
# Khởi động lại ứng dụng
```

### "Module not found"
```bash
# Kích hoạt virtual environment
venv\Scripts\activate
# Cài lại thư viện
pip install -r requirements.txt
```

### "Port 7861 already in use"
```bash
# Đóng ứng dụng Gradio khác
# Hoặc đổi port trong src/ui/gradio_app.py
```

### "Rate limit exceeded"
```bash
# Gemini: Đợi 1 phút (giới hạn 15 requests/phút)
# Kiểm tra usage: https://ai.dev/usage?tab=rate-limit
```

---

## 🧪 Testing

```bash
# Chạy tất cả tests
pytest tests/

# Chạy với coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 💡 Best Practices

### Transcript tốt nhất
- Độ dài: 500-15,000 ký tự
- Đ
## 📚 Documentation

### User Guides
- **README.md** - Overview and basic guide (this file)

## 🎯 Development Guidelines

### Code Quality
- Always use type hints
- Write comprehensive docstrings (Google style)
- Implement error handling
- Follow PEP 8
- Write unit tests
- Never hardcode API keys
- Validate user input

### Technology Stack
- **MUST USE**: Python 3.8+, Google Gemini SDK, Gradio
- **NEVER USE**: LangChain, Vector databases

### Architecture Principles
```
Upload → Clean → Truncate → Prompt → API → Response
```

See `INSTRUCTIONS/` folder for detailed development guidelines.

---

## 🤝 Contributing

### Branch Strategy
- `main`: Production code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes

### Commit Convention
```
<type>(<scope>): <description>

Examples:
feat(llm): add GPT-4 integration
fix(ui): resolve upload file error
docs(readme): update installation instructions
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make changes with proper commits
3. Write/update tests
4. Submit PR with description
5. Get approval from code owner
6. Merge after all checks pass

---

## 🎉 Quick Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# Run
python src/ui/gradio_app.py
