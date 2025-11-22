# 📁 Sprints Directory Structure

This directory contains code organized by sprint, with each sprint building upon previous features.

---

## 🗂️ Directory Structure

```
sprints/
├── sprint1/          # Sprint 1: Meeting Transcript Analyzer
│   ├── src/          # Source code for Sprint 1
│   ├── tests/        # Tests for Sprint 1
│   └── README.md     # Sprint 1 documentation
│
├── sprint2/          # Sprint 2: Multi-turn Chatbot
│   ├── src/          # Source code for Sprint 2
│   ├── tests/        # Tests for Sprint 2
│   └── README.md     # Sprint 2 documentation
│
├── sprint3/          # Sprint 3: TTS Chatbot with ChromaDB
│   ├── src/          # Source code for Sprint 3
│   ├── tests/        # Tests for Sprint 3
│   └── README.md     # Sprint 3 documentation
│
└── sprint4/          # Sprint 4: RAG + LangChain + Hackathon
    ├── src/          # Source code for Sprint 4
    ├── tests/        # Tests for Sprint 4
    └── README.md     # Sprint 4 documentation
```

---

## 🚀 Sprint Overview

### Sprint 1: Meeting Transcript Analyzer
**Workshop**: Nov 16, 2025 (6 hours)

**Features**:
- File upload (TXT/DOCX)
- LLM integration (Gemini/OpenAI)
- Meeting summarization
- Action items extraction
- Decisions extraction
- Topics extraction
- Gradio UI
- Export (TXT/DOCX)

**Tech Stack**:
- Python 3.11+
- Google Gemini API / OpenAI API
- Gradio
- python-docx

---

### Sprint 2: Multi-turn Chatbot
**Workshop**: Nov 23, 2025 (8 hours)

**Features**:
- Multi-LLM support (OpenAI, Gemini, Llama)
- Conversation management
- Function calling
- Batching & retry logic
- Few-shot prompting
- Chain-of-thought reasoning
- Streaming responses

**Tech Stack**:
- OpenAI SDK
- Llama 3 (Ollama/Groq)
- Advanced prompting techniques

---

### Sprint 3: TTS Chatbot with ChromaDB
**Workshop**: Nov 30, 2025 (6 hours)

**Features**:
- ChromaDB vector database
- Knowledge base storage & retrieval
- OpenAI SDK integration
- HuggingFace Text-to-Speech (VITS)
- Audio responses
- Multi-turn conversations

**Tech Stack**:
- ChromaDB
- OpenAI SDK
- HuggingFace Transformers
- TTS (VITS model)

---

### Sprint 4: RAG + LangChain + Hackathon
**Workshop**: Dec 7, 2025 (1 hour)  
**Hackathon**: Dec 13, 2025 (8 hours)

**Features**:
- FAISS/Pinecone vector store
- LangChain RAG pipeline
- Advanced retrieval strategies
- Function calling
- LangGraph workflows (optional)
- Production-ready deployment

**Tech Stack**:
- LangChain
- FAISS / Pinecone
- LangGraph
- Production tools

---

## 📝 Development Guidelines

### Code Organization
Each sprint should:
- Build upon previous sprint features
- Maintain backward compatibility when possible
- Have its own tests
- Be independently runnable

### Sprint Structure
```
sprintX/
├── src/
│   ├── config/       # Configuration
│   ├── data/         # Data processing
│   ├── llm/          # LLM integration
│   ├── rag/          # RAG logic
│   ├── ui/           # User interface
│   └── utils/        # Utilities
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── data/
│   └── samples/      # Sample data
├── requirements.txt  # Dependencies
└── README.md         # Sprint documentation
```

### Running a Sprint
```bash
# Navigate to sprint directory
cd sprints/sprint1

# Install dependencies
pip install -r requirements.txt

# Run application
python src/ui/app.py
```

---

## 🔄 Migration Between Sprints

When moving to a new sprint:
1. Copy relevant code from previous sprint
2. Refactor as needed for new features
3. Update dependencies
4. Add new tests
5. Update documentation

---

## 📊 Progress Tracking

| Sprint | Status | Completion | Workshop Date |
|--------|--------|------------|---------------|
| Sprint 1 | 🔄 In Progress | 60% | Nov 16 |
| Sprint 2 | 📅 Planned | 0% | Nov 23 |
| Sprint 3 | 📅 Planned | 0% | Nov 30 |
| Sprint 4 | 📅 Planned | 0% | Dec 7-13 |

---

**Last Updated**: November 10, 2025  
**Team**: Team 3 - Akatsuki 🔥
