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

### 3. Run Application

```bash
python src/ui/gradio_app.py
```

Browser will automatically open at: **http://localhost:7861**

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

### Technology Stack
- **MUST USE**: Python 3.8+, Google Gemini SDK, Gradio
- **NEVER USE**: LangChain, Vector databases

### Architecture Principles
```
Upload → Clean → Truncate → Prompt → API → Response
```

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
