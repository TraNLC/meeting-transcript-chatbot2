# 💬 Meeting Note Summarization Chat bot

An intelligent meeting analysis system using **Google Gemini AI** to generate summaries and extract important information from meeting transcripts.

> 📚 **Course Project**: This project is developed through 5 sprints following the AI Application Engineer Learning Path.

**Current Status**: Sprint 3 Complete (Nov 29) ✅ Recording + ChromaDB + Modern UI

**Quick Links:**
- 📊 [**Dashboard**](dashboard.html) - Live progress tracking (Open in browser) ⭐
- 📋 [Course Overview](COURSE_OVERVIEW.md) - Full learning path timeline
- 🚀 [Sprint Planning](SPRINTS.md) - All sprints overview

**Documentation:**
- 📁 [Plans](docs/plans/) - Sprint plans & task breakdown
- 📁 [Reports](docs/reports/) - Weekly effort reports
- 📁 [Sprints](sprints/) - Sprint code snapshots
- 📖 [Development Guide](docs/DEVELOPMENT_GUIDE.md) - How to develop across sprints ⭐

**Sprint Plans:**
- 📝 [Sprint 1](docs/plans/SPRINT1_PLAN.md) - Meeting Analyzer (Nov 16, 6h)
- 📝 [Sprint 2](docs/plans/SPRINT2_PLAN.md) - Multi-turn Chatbot (Nov 23, 8h)
- 📝 [Sprint 3](docs/plans/SPRINT3_PLAN.md) - TTS + ChromaDB (Nov 30, 6h)
- 📝 [Sprint 4](docs/plans/SPRINT4_PLAN.md) - RAG + LangChain (Dec 7, 1h)

**Weekly Reports:**
- 📊 [Week 1](docs/reports/WEEK1_REPORT.md) - Nov 10-16 (Workshop 1)

**Team Management:**
- 👥 [Team Tasks](TEAM_TASKS.md) - Task assignments
- 📝 [Daily Log](DAILY_LOG.md) - Work log & mentor review

## ✨ Features

### Sprint 3 Complete Features ✅ NEW!

#### 🎙️ Audio Recording & Transcription
- **Browser Recording**: Record directly with microphone
- **Auto-Transcribe**: OpenAI Whisper (Local, 50+ languages)
- **Recording History**: Manage and playback recordings
- **Multi-language**: Vietnamese, English, Japanese, Korean, Chinese

#### 🔍 Semantic Search (ChromaDB)
- **AI Search**: Search by meaning, not just keywords
- **Smart Filters**: By meeting type, language, date
- **Find Similar**: Discover related meetings
- **Analytics**: Database statistics and insights

#### ✅ Checklist Management
- **Task Tracking**: Create and manage action items
- **Assignees & Deadlines**: Track who does what and when
- **Priority Levels**: High, Medium, Low
- **Import from Analysis**: Auto-create tasks from meetings

#### 📊 Modern 7-Tab Interface
- **Tab 1**: 🎙️ Ghi Âm (Recording)
- **Tab 2**: 📤 Upload & Phân Tích (Upload & Analysis)
- **Tab 3**: 💬 Chat với AI (Chat with AI)
- **Tab 4**: 📊 Lịch Sử Phân Tích (Analysis History)
- **Tab 5**: 🎙️ Lịch Sử Ghi Âm (Recording History)
- **Tab 6**: 🔍 Tìm Kiếm & Xuất (Search & Export)
- **Tab 7**: ✅ Checklist

#### 📤 Export & Integration
- **Export Formats**: TXT, DOCX (Word)
- **Professional Layout**: Headers, bullets, formatting
- **Save to History**: Auto-save analysis results
- **Vector Storage**: ChromaDB for semantic search

### Sprint 2 Features ✅
- 📝 **Automatic Summarization**: Generate concise summaries
- ✅ **Action Items Extraction**: Find tasks, assignees, and deadlines
- 🎯 **Decision Detection**: Identify important decisions
- 📌 **Topic Recognition**: Extract main topics discussed
- 🌍 **Multi-language Support**: 20+ languages
- 🎭 **Meeting Types**: Meetings, workshops, brainstorming



## 🛠️ Technology Stack

- **Python 3.11+**
- **AI Models**: 
  - Google Gemini 2.5 Flash (Analysis)
  - OpenAI Whisper (Transcription, Local)
  - sentence-transformers (Embeddings)
- **Vector Database**: ChromaDB
- **UI Framework**: Gradio 4.x
- **Audio Processing**: ffmpeg
- **Document**: python-docx

---

## 🚀 Quick Setup (5 minutes)

### 1. Clone and Install

```bash
# Clone repository
git clone <repository-url>
cd meeting-transcript-chatbot

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Create .env file
copy .env.example .env         # Windows
cp .env.example .env           # Linux/Mac
```

**Get Gemini API Key (FREE):**
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy API key

**Open `.env` file and paste API key:**

```env
# API Key
GEMINI_API_KEY=your-gemini-api-key-here

# Configuration (Fixed)
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash
TEMPERATURE=0.7
MAX_TOKENS=4000
OUTPUT_LANGUAGE=vi
```

### 3. Install ffmpeg (Required for Recording)

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Extract to C:\ffmpeg and add to PATH
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 4. Run Application

```bash
# Modern 7-tab interface (Recommended)
python src/ui/app_v2.py

# Or original interface
python src/ui/gradio_app_final.py
```

Browser will automatically open at: **http://localhost:7779**

### 4. Usage

1. **Upload** transcript file (TXT or DOCX)
2. **Click** "🚀 Process Transcript"
3. **Wait** 30-60 seconds (loading indicator shown)
4. **View** analysis results:
   - 📝 Meeting summary
   - 🎯 Main topics
   - ✅ Action Items
   - 🎯 Important decisions
5. **Export** results:
   - 📄 Export TXT file
   - 📝 Export DOCX file

---

## 📁 Project Structure

```
meeting-transcript-chatbot/
├── src/
│   ├── config/          # Configuration
│   ├── data/            # Data loading & processing
│   ├── llm/             # Gemini integration
│   ├── rag/             # Chatbot logic
│   └── ui/              # Gradio interface
├── data/
│   └── transcripts/     # Sample transcript files
├── tests/               # Unit tests
├── .env.example         # Configuration template
├── requirements.txt     # Required dependencies
└── README.md           # This file
```

---
## 📖 Detailed Guide

### Sample Transcript File

Use file: `data/transcripts/sample_meeting.txt`

### Sample Questions (if Q&A feature available)

```
- Who is responsible for the design part?
- When is the payment integration deadline?
- What is the marketing budget?
- When is the official launch date?
```

### Processing Flow

```
1. Upload Transcript (TXT/DOCX)
   ↓
2. Preprocessing: Clean → Truncate → Store in memory
   ↓
3. Create Prompt (System + User)
   ↓
4. Send → Gemini API
   ↓
5. AI generates response
   ↓
6. Display results
   ↓
7. Export file (TXT/DOCX)
```

---

## ❌ Error Handling

### "GEMINI_API_KEY not found"
```bash
# Check that .env file exists
# Ensure it contains: GEMINI_API_KEY=...
# Restart the application
```

### "Module not found"
```bash
# Activate virtual environment
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

### "Port 7861 already in use"
```bash
# Close other Gradio applications
# Or change port in src/ui/gradio_app.py
```

### "Rate limit exceeded"
```bash
# Gemini: Wait 1 minute (limit: 15 requests/minute)
# Check usage: https://ai.dev/usage?tab=rate-limit
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

### Best Transcript Format
- Length: 500-15,000 characters
- Format: Clear speaker labels and timestamps
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

### Technology Stack Evolution

**Current (Sprint 1-2):**
- Python 3.11+, Gemini/OpenAI API, Gradio
- Build from scratch - no frameworks yet

**Future (Sprint 3):**
- Add: Hugging Face, custom RAG implementation
- Still no LangChain - learn by building!

**Future (Sprint 4):**
- Add: LangChain, Pinecone
- Compare custom vs framework approaches

### Architecture Evolution
```
Sprint 1-2: Upload → Clean → Prompt → LLM → Response

Sprint 3:   Upload → Chunk → Embed → Vector Store
                                    ↓
            Query → Embed → Search → Context → LLM → Response

Sprint 4:   Same as Sprint 3 but with LangChain + Pinecone
```

---

## 📅 Sprint Development

This project follows a 4-sprint development cycle:

- **Sprint 1** (🔄 60%): Nov 16 - Meeting Analyzer (Workshop 6h)
- **Sprint 2** (📅 Planned): Nov 23 - Multi-turn Chatbot (Workshop 8h)
- **Sprint 3** (📅 Planned): Nov 30 - TTS + ChromaDB (Workshop 6h)
- **Sprint 4** (📅 Planned): Dec 7 - RAG + LangChain (Workshop 1h)

See [SPRINTS.md](SPRINTS.md) for detailed sprint planning and tasks.

## 🤝 Contributing

### Branch Strategy
- `main`: Production code (merged sprint code)
- `sprint-1`, `sprint-2`, `sprint-3`, `sprint-4`: Sprint development branches
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
