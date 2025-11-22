# 🛠️ Development Guide - Sprint-based Development

## 📁 Recommended Structure

```
meeting-transcript-chatbot/
├── src/                    # Main codebase (incremental)
│   ├── config/
│   ├── data/
│   ├── llm/
│   ├── rag/
│   ├── vectorstore/       # Added in Sprint 3
│   ├── tts/               # Added in Sprint 3
│   └── ui/
│
├── sprints/               # Sprint snapshots (for reference)
│   ├── sprint1/
│   │   └── snapshot/      # Code snapshot after Sprint 1
│   ├── sprint2/
│   │   └── snapshot/      # Code snapshot after Sprint 2
│   ├── sprint3/
│   │   └── snapshot/
│   └── sprint4/
│       └── snapshot/
│
├── tests/                 # Tests for current code
├── docs/
└── data/
```

---

## 🚀 Development Workflow

### Sprint 1 (Nov 16)
**Goal**: Build foundation

```bash
# Work in main src/
src/
├── config/settings.py
├── data/
│   ├── loader.py          # NEW
│   └── preprocessor.py    # NEW
├── llm/
│   ├── gemini_model.py    # NEW
│   └── prompts.py         # NEW
├── rag/
│   └── chatbot.py         # NEW
└── ui/
    └── gradio_app.py      # NEW
```

**After Sprint 1**:
```bash
# Create snapshot
git tag sprint1-complete
cp -r src/ sprints/sprint1/snapshot/
```

---

### Sprint 2 (Nov 23)
**Goal**: Add multi-LLM & conversation

```bash
# Continue in src/, add new files
src/
├── llm/
│   ├── base.py            # NEW - Abstract interface
│   ├── gemini_model.py    # MODIFY
│   ├── openai_model.py    # NEW
│   ├── llama_model.py     # NEW
│   └── factory.py         # NEW
├── rag/
│   ├── chatbot.py         # MODIFY - Add conversation
│   └── conversation.py    # NEW
└── functions/             # NEW
    ├── registry.py
    └── meeting_functions.py
```

**Key**: Use feature flags for backward compatibility
```python
# In chatbot.py
class Chatbot:
    def __init__(self, llm_manager, use_conversation=False):
        self.llm_manager = llm_manager
        self.use_conversation = use_conversation  # Sprint 2 feature
        if use_conversation:
            self.conversation = ConversationManager()
```

**After Sprint 2**:
```bash
git tag sprint2-complete
cp -r src/ sprints/sprint2/snapshot/
```

---

### Sprint 3 (Nov 30)
**Goal**: Add ChromaDB & TTS

```bash
# Add new modules
src/
├── vectorstore/           # NEW
│   ├── __init__.py
│   ├── chromadb_store.py
│   └── base.py
├── tts/                   # NEW
│   ├── __init__.py
│   └── huggingface_tts.py
└── rag/
    └── chatbot.py         # MODIFY - Add vector search option
```

**Feature flag approach**:
```python
class Chatbot:
    def __init__(self, llm_manager, 
                 use_conversation=False,
                 use_vectorstore=False):  # Sprint 3 feature
        self.llm_manager = llm_manager
        self.use_conversation = use_conversation
        self.use_vectorstore = use_vectorstore
        if use_vectorstore:
            self.vectorstore = ChromaDBStore()
```

---

### Sprint 4 (Dec 7)
**Goal**: Add LangChain RAG

```bash
# Add LangChain integration
src/
├── vectorstore/
│   ├── chromadb_store.py  # KEEP
│   └── faiss_store.py     # NEW
├── rag/
│   ├── chatbot.py         # KEEP - Basic version
│   ├── langchain_rag.py   # NEW - LangChain version
│   └── retrieval.py       # NEW
└── ui/
    └── gradio_app.py      # MODIFY - Add RAG toggle
```

**Approach**: Keep both versions
```python
# In UI
use_langchain = gr.Checkbox(label="Use LangChain RAG")

if use_langchain:
    chatbot = LangChainRAGChatbot(...)
else:
    chatbot = Chatbot(...)  # Original version
```

---

## 🔧 Best Practices

### 1. Use Feature Flags
```python
# config/settings.py
class Settings:
    # Sprint 1
    ENABLE_BASIC_CHATBOT = True
    
    # Sprint 2
    ENABLE_MULTI_LLM = True
    ENABLE_CONVERSATION = True
    
    # Sprint 3
    ENABLE_VECTORSTORE = True
    ENABLE_TTS = True
    
    # Sprint 4
    ENABLE_LANGCHAIN_RAG = True
```

### 2. Backward Compatibility
```python
# Old code still works
chatbot = Chatbot(llm_manager)  # Sprint 1 style

# New code with features
chatbot = Chatbot(
    llm_manager,
    use_conversation=True,      # Sprint 2
    use_vectorstore=True,       # Sprint 3
    use_langchain=True          # Sprint 4
)
```

### 3. Version Tags
```bash
# After each sprint
git tag sprint1-complete -m "Sprint 1: Basic chatbot"
git tag sprint2-complete -m "Sprint 2: Multi-LLM"
git tag sprint3-complete -m "Sprint 3: ChromaDB + TTS"
git tag sprint4-complete -m "Sprint 4: LangChain RAG"

# View history
git tag -l
```

### 4. Snapshot for Reference
```bash
# After each sprint workshop
./scripts/create_sprint_snapshot.sh sprint1
```

**create_sprint_snapshot.sh**:
```bash
#!/bin/bash
SPRINT=$1
mkdir -p sprints/$SPRINT/snapshot
cp -r src/ sprints/$SPRINT/snapshot/
cp requirements.txt sprints/$SPRINT/snapshot/
echo "Snapshot created for $SPRINT"
```

---

## 🧪 Testing Strategy

### Test Organization
```
tests/
├── sprint1/           # Tests for Sprint 1 features
│   ├── test_loader.py
│   └── test_chatbot.py
├── sprint2/           # Tests for Sprint 2 features
│   ├── test_conversation.py
│   └── test_multi_llm.py
├── sprint3/           # Tests for Sprint 3 features
│   └── test_vectorstore.py
└── sprint4/           # Tests for Sprint 4 features
    └── test_langchain_rag.py
```

### Run Tests by Sprint
```bash
# Test all
pytest tests/

# Test specific sprint
pytest tests/sprint1/
pytest tests/sprint2/

# Regression test (all previous sprints)
pytest tests/sprint1/ tests/sprint2/
```

---

## 🔄 Migration Between Sprints

### Example: Sprint 1 → Sprint 2

**Sprint 1 Code**:
```python
# src/llm/gemini_model.py
class GeminiModel:
    def generate(self, prompt):
        return self.client.generate(prompt)
```

**Sprint 2 Refactor**:
```python
# src/llm/base.py (NEW)
class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt):
        pass

# src/llm/gemini_model.py (MODIFY)
class GeminiModel(BaseLLM):  # Inherit from base
    def generate(self, prompt):
        return self.client.generate(prompt)

# src/llm/openai_model.py (NEW)
class OpenAIModel(BaseLLM):
    def generate(self, prompt):
        return self.client.chat.completions.create(...)
```

**Key**: Old code still works!
```python
# Sprint 1 style - still works
gemini = GeminiModel(api_key)
response = gemini.generate(prompt)

# Sprint 2 style - new way
llm = LLMFactory.create("gemini", api_key)
response = llm.generate(prompt)
```

---

## 📊 Sprint Progress Tracking

### requirements.txt Evolution
```
# Sprint 1
google-generativeai==0.3.0
gradio==4.0.0
python-docx==1.0.0

# Sprint 2 (add)
openai==1.0.0
# ollama (for Llama 3)

# Sprint 3 (add)
chromadb==0.4.0
transformers==4.35.0
TTS==0.20.0

# Sprint 4 (add)
langchain==0.1.0
faiss-cpu==1.7.4
```

### Feature Matrix
| Feature | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|---------|----------|----------|----------|----------|
| File Upload | ✅ | ✅ | ✅ | ✅ |
| Gemini API | ✅ | ✅ | ✅ | ✅ |
| Summary | ✅ | ✅ | ✅ | ✅ |
| Extraction | ✅ | ✅ | ✅ | ✅ |
| Multi-LLM | - | ✅ | ✅ | ✅ |
| Conversation | - | ✅ | ✅ | ✅ |
| Function Calling | - | ✅ | ✅ | ✅ |
| ChromaDB | - | - | ✅ | ✅ |
| TTS | - | - | ✅ | ✅ |
| LangChain RAG | - | - | - | ✅ |

---

## 🎯 Summary

**Recommended Approach**:
1. ✅ **Main codebase** in `src/` - incremental development
2. ✅ **Feature flags** for backward compatibility
3. ✅ **Git tags** after each sprint
4. ✅ **Snapshots** in `sprints/sprintX/snapshot/` for reference
5. ✅ **Tests** organized by sprint
6. ✅ **Keep old code working** while adding new features

**Benefits**:
- Clean, maintainable codebase
- Easy to demo any sprint version
- No code duplication
- Clear feature evolution
- Safe to experiment

---

**Last Updated**: November 10, 2025  
**Team**: Team 3 - Akatsuki 🔥
