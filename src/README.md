# 📁 Source Code Structure

## 🗂️ Directory Organization

```
src/
├── config/              # Configuration
│   └── settings.py      # App settings & environment variables
│
├── data/                # Data processing (Sprint 1)
│   ├── loader.py        # File loading (TXT/DOCX)
│   └── preprocessor.py  # Text preprocessing
│
├── llm/                 # LLM integration
│   ├── base.py          # Sprint 2: Abstract base class
│   ├── gemini_model.py  # Sprint 1: Gemini implementation
│   ├── chat_model.py    # Sprint 1: Original (backward compatible)
│   ├── factory.py       # Sprint 2: LLM factory
│   └── prompts.py       # Prompt templates
│
├── rag/                 # RAG & Chatbot logic
│   ├── chatbot.py       # Sprint 1: Basic chatbot
│   └── conversation.py  # Sprint 2: Conversation management
│
├── ui/                  # User interface
│   ├── gradio_app.py    # Sprint 1: Gradio interface
│   └── app.py           # Alternative UI
│
├── vectorstore/         # Sprint 3: Vector databases
│   └── (empty - will add in Sprint 3)
│
└── tts/                 # Sprint 3: Text-to-Speech
    └── (empty - will add in Sprint 3)
```

---

## 🚀 Sprint Evolution

### Sprint 1 (Current)
**Files**:
- `data/loader.py` - File loading
- `data/preprocessor.py` - Text preprocessing
- `llm/chat_model.py` - Gemini integration
- `llm/prompts.py` - Prompt templates
- `rag/chatbot.py` - Basic chatbot
- `ui/gradio_app.py` - Gradio UI

**Features**:
- File upload (TXT/DOCX)
- Gemini API integration
- Summary generation
- Action items extraction
- Topics & decisions extraction
- Export (TXT/DOCX)

---

### Sprint 2 (Prepared)
**New Files**:
- `llm/base.py` - Abstract LLM interface
- `llm/gemini_model.py` - Refactored Gemini
- `llm/factory.py` - LLM factory pattern
- `rag/conversation.py` - Conversation manager

**To Add in Workshop**:
- `llm/openai_model.py` - OpenAI integration
- `llm/llama_model.py` - Llama 3 integration
- `functions/` - Function calling

**Features**:
- Multi-LLM support (Gemini, OpenAI, Llama)
- Conversation management
- Function calling
- Batching & retry logic

---

### Sprint 3 (Future)
**To Add**:
- `vectorstore/chromadb_store.py` - ChromaDB integration
- `tts/huggingface_tts.py` - Text-to-Speech

**Features**:
- Vector database for knowledge storage
- Semantic search
- Audio responses

---

### Sprint 4 (Future)
**To Add**:
- `vectorstore/faiss_store.py` - FAISS integration
- `rag/langchain_rag.py` - LangChain RAG
- `rag/retrieval.py` - Advanced retrieval

**Features**:
- LangChain RAG pipeline
- Advanced retrieval strategies
- Production-ready RAG

---

## 💻 Usage Examples

### Sprint 1 (Current - Backward Compatible)
```python
from src.llm import LLMManager
from src.rag import Chatbot

# Original way (still works)
llm_manager = LLMManager(
    provider="gemini",
    model_name="gemini-2.5-flash",
    api_key="your-api-key"
)

chatbot = Chatbot(llm_manager=llm_manager, transcript="...")
summary = chatbot.generate_summary()
```

### Sprint 2 (New Architecture)
```python
from src.llm import LLMFactory, LLMManager
from src.rag import Chatbot, ConversationManager

# New way - using factory
llm = LLMFactory.create(
    provider="gemini",  # or "openai", "llama"
    api_key="your-api-key",
    model="gemini-2.5-flash"
)

# Or use LLMManager (backward compatible)
llm_manager = LLMManager(
    provider="gemini",
    api_key="your-api-key"
)

# With conversation management
conversation = ConversationManager()
conversation.add_system_message("You are a helpful assistant")
conversation.add_user_message("Hello!")

# Chat completion
response = llm_manager.chat_completion(conversation.get_messages())
conversation.add_assistant_message(response)
```

---

## 🔧 Development Guidelines

### Adding New LLM Provider (Sprint 2)

1. **Create provider file**: `src/llm/provider_model.py`
```python
from .base import BaseLLM

class ProviderModel(BaseLLM):
    def generate(self, prompt, system_message="", **kwargs):
        # Implementation
        pass
    
    def chat_completion(self, messages, **kwargs):
        # Implementation
        pass
```

2. **Update factory**: `src/llm/factory.py`
```python
from .provider_model import ProviderModel

# In LLMFactory.create()
elif provider == "provider":
    return ProviderModel(api_key=api_key, model=model, **kwargs)
```

3. **Update exports**: `src/llm/__init__.py`
```python
from .provider_model import ProviderModel

__all__ = [..., "ProviderModel"]
```

---

## 🧪 Testing

```bash
# Test Sprint 1 features
pytest tests/sprint1/

# Test Sprint 2 features
pytest tests/sprint2/

# Test all
pytest tests/
```

---

## 📝 Notes

- **Backward Compatibility**: Sprint 1 code still works with Sprint 2 architecture
- **Feature Flags**: Use config to enable/disable features
- **Incremental**: Each sprint builds on previous work
- **Clean**: Old code is refactored, not duplicated

---

**Last Updated**: November 10, 2025  
**Current Sprint**: Sprint 1 (60% complete)  
**Next Sprint**: Sprint 2 (Nov 23)
