# 🚀 Sprint Planning - Meeting Transcript Chatbot

Dự án được chia thành 4 sprints tương ứng với 4 workshop trong khóa học AI Engineering.

---

## 📋 Sprint Overview

| Sprint | Session | Workshop | Công nghệ chính | Branch | Timeline | Status |
|--------|---------|----------|-----------------|--------|----------|--------|
| Sprint 1 | Session 1 | Workshop 1 (6h) | Python & OpenAI API | `sprint-1` | Nov 16 | 🔄 60% Complete |
| Sprint 2 | Session 2 | Workshop 2 (8h) | OpenAI API & Llama 3 | `sprint-2` | Nov 23 | 📅 Planned |
| Sprint 3 | Session 3 | Workshop 3 (6h) | ChromaDB & HuggingFace TTS | `sprint-3` | Nov 30 | 📅 Planned |
| Sprint 4 | Session 4 | Workshop 4 (1h) | LangChain & RAG | `sprint-4` | Dec 7 | 📅 Planned |

---

## Sprint 1: Python & OpenAI API Basics
**Session 1 - Python & OpenAI API**  
**Workshop 1 - Building Real-World AI-Powered Apps Using Python and OpenAI API**

**�  Timeline**: November 10-14, 2025 (5 days)  
**� Woorkshop**: Saturday, Nov 15 (1.5 hours)  
**👥 Team**: 7 members  
**📊 Progress**: 60% Complete

### 🎯 Learning Objectives (từ khóa học)
**Python Fundamentals:**
- Comments, Calculations, Data types
- Variables, Lists, Dictionaries, Sets, Tuples
- Comparison operators, Conditional statements
- For loops, While loops

**OpenAI API:**
- OpenAI models overview
- API authentication & basics
- Sending requests in Python
- Handling responses
- Text generation & Prompt design
- Chat completions
- Real-world use cases

### 🎯 Project Goals
- Thiết lập môi trường Python cơ bản
- Tích hợp OpenAI/Gemini API
- Xây dựng Meeting Summarizer chatbot
- Prompt engineering cho extraction tasks
- Tạo giao diện Gradio

### ✅ Deliverables
- [x] Cấu hình project với virtual environment
- [x] Tích hợp Gemini API (tương đương OpenAI)
- [x] Xây dựng module xử lý transcript
- [x] Prompt templates cho summary/extraction
- [x] Tạo UI Gradio đơn giản
- [ ] Unit tests cơ bản
- [ ] Complete Assignment 03 equivalent

### 📝 Related Assignments (Reference)
- Assignment 01: Command-Line Task Manager (Python basics)
- Assignment 02: Automotive Prompt-Driven Agent
- **Assignment 03: AI-Powered Meeting Summarizer** ⭐ (Our project!)

### 🎓 Assessment
- Quiz 01: Python & OpenAI (15 mins)
- Mock Interview 1: Python & OpenAI concepts (10-15 mins)

### 🛠️ Tech Stack
- Python 3.11+
- Google Gemini API
- Gradio
- python-docx

### 📂 Code Structure
```
src/
├── config/settings.py      # API configuration
├── llm/chat_model.py       # Gemini integration
├── llm/prompts.py          # Prompt templates
├── data/loader.py          # File loading
├── data/preprocessor.py    # Text preprocessing
└── ui/gradio_app.py        # Gradio interface
```

### 🔗 Branch
```bash
git checkout sprint-1
```

### 👥 Team Assignments
See detailed task breakdown: [TEAM_TASKS.md](TEAM_TASKS.md)

---

## Sprint 2: Advanced LLM Integration
**Session 2 - OpenAI API & Llama 3**  
**Workshop 2 - Building Chatbot Systems Using Azure OpenAI API**

**📅 Preparation**: November 17-22, 2025 (6 days)  
**📅 Workshop Day**: Saturday, Nov 23, 2025 (8 hours) - Virtual via MS Teams  
**👥 Team**: 7 members (5 active participants during workshop)

### 🎯 Learning Objectives (từ khóa học)
**Developing AI Systems with OpenAI:**
- Best practices for OpenAI API
- Moderation & Validation
- Testing & Safety practices
- Function calling
- Connecting external systems and APIs
- Production-ready application design

**Llama 3:**
- Llama 3 setup
- Running Llama locally
- Prompt adjustment
- Contextual conversations
- Output adaptation
- Structured data generation
- Response refinement

### 🎯 Workshop 2 Requirements (IMPORTANT!)
**Coverage**: Multi-turn chatbot systems with advanced features

**Deliverables by end of workshop:**
1. ✅ **Real-world problem definition** + mock data schema
2. ✅ **Prompt templates** using few-shot & chain-of-thought techniques
3. ✅ **Complete OpenAI SDK chatbot** implementing:
   - Chat completion
   - Function calling
   - Batching
   - Message management (conversation history)
4. ✅ **Tested conversation logs** showing multi-turn dialogue with context
5. ✅ **Team presentation** with demo, insights, lessons learned

**Key Features to Implement:**
- 🔄 Multi-turn conversation with context retention
- 🛠️ Function calling for external data/APIs
- 📦 Batching for efficient API usage
- 💬 Conversation message management
- 🎯 Few-shot prompting examples
- 🧠 Chain-of-thought reasoning
- 📊 Mock data generation and usage

### 🎯 Project Goals for Sprint 2

**Pre-Workshop Preparation (Nov 17-22):**
- Setup OpenAI SDK and Azure credentials
- Study OpenAI API documentation
- Prepare conversation management framework
- Create function calling templates
- Prepare mock data examples
- Setup demo environment

**Workshop Day (Nov 23 - 8 hours):**
- Hour 1-2: Problem definition & design
- Hour 3-4: Prompt engineering & setup
- Hour 5-6: Core implementation (chat + conversation)
- Hour 7: Function calling implementation
- Hour 8: Testing & presentation

### 📋 Key Tasks

**Pre-Workshop (Nov 17-22)**:
- [ ] Setup OpenAI SDK & credentials
- [ ] Study OpenAI documentation
- [ ] Prepare conversation framework
- [ ] Create function calling templates
- [ ] Prepare mock data & scenarios

**Workshop Day (Nov 23 - 8 hours)**:
- [ ] Define problem & mock data
- [ ] Design prompt templates
- [ ] Implement chat completion
- [ ] Add conversation management
- [ ] Implement function calling
- [ ] Test & document
- [ ] Team presentation

### 📝 Related Assignments (Reference)
- **Assignment 04**: Efficient API Usage with Function Calling & Batching ⭐
- **Assignment 05**: Resume Generation Using LLaMA3
- **Assignment 06**: Logistics Delay Classification

### 🎓 Assessment
- Quiz 02: OpenAI API & Llama3 (15 mins)
- Mock Interview 2: Advanced API concepts (10-15 mins)
- **Workshop 2**: Team presentation with working demo



### 🛠️ Tech Stack
- OpenAI API (GPT-3.5/4)
- Llama 3 (Ollama hoặc Groq API)
- Google Gemini API
- Gradio với chat interface

### 📂 New Modules
```
src/
├── llm/
│   ├── base.py             # Abstract LLM class
│   ├── openai_model.py     # OpenAI integration
│   ├── llama_model.py      # Llama 3 integration
│   └── gemini_model.py     # Gemini integration
└── memory/
    └── conversation.py     # Chat history management
```

### 🔗 Branch
```bash
git checkout sprint-2
```

---

## Sprint 3: Embeddings & Semantic Search
**Session 3 - Hugging Face & Embeddings with OpenAI**  
**Workshop 3 - Building a Text-to-Speech Chatbot Using OpenAI SDK + Hugging Face TTS**

**📅 Timeline**: November 24-28, 2025 (5 days)  
**📅 Workshop**: Saturday, Nov 29 (1.5 hours)  
**👥 Team**: 7 members

### 🎯 Learning Objectives (từ khóa học)
**Hugging Face:**
- Hugging Face Hub
- Model selection & Dataset selection
- Hugging Face API
- Model search by task/author/popularity
- Pipelines
- Text classification & summarization
- Document-based conversation

**Embeddings:**
- Text embeddings
- Semantic meaning encoding
- OpenAI Embeddings API
- Creating embeddings from text
- Semantic search
- Recommendation engines
- Vector databases
- Storing & querying embeddings
- Production-ready applications

### 🎯 Project Goals
- Tích hợp Hugging Face models
- Implement embeddings cho transcript
- Xây dựng semantic search
- Custom RAG pipeline (no frameworks)
- Cải thiện context retrieval

### 📋 Tasks
- [ ] Tích hợp Hugging Face Transformers
- [ ] Setup sentence-transformers (e.g., all-MiniLM-L6-v2)
- [ ] Implement text chunking strategies
- [ ] Tạo embeddings cho transcript chunks
- [ ] Build in-memory vector store (NumPy arrays)
- [ ] Implement cosine similarity search
- [ ] Xây dựng context retrieval & ranking
- [ ] Thêm semantic search UI
- [ ] Optimize embedding performance
- [ ] Compare semantic vs keyword search

### 📝 Related Assignments (Reference)
- Assignment 07: Clone & Inference with HF Text-to-Speech
- Assignment 08: Semantic Search Engine for Clothing Products
- Assignment 09: Laptop Consultant Chatbot

### 🎓 Assessment
- Quiz 03: Hugging Face & Embeddings (15 mins)
- Mock Interview 3: Embeddings concepts (10-15 mins)

### 🛠️ Tech Stack
- Hugging Face Transformers
- sentence-transformers (e.g., all-MiniLM-L6-v2)
- NumPy (vector operations)
- **NO LangChain** - tự build để hiểu!
- **NO Pinecone** - dùng in-memory store

### 🎯 Key Learning Points
- Hiểu embeddings là gì và cách hoạt động
- Tự implement vector similarity
- Document chunking strategies
- Trade-offs: accuracy vs speed vs memory

### 📂 New Modules
```
src/
├── embeddings/
│   ├── encoder.py          # Text to embeddings
│   └── similarity.py       # Similarity calculations
├── retrieval/
│   ├── chunker.py          # Text chunking
│   └── searcher.py         # Semantic search
└── vectorstore/
    └── memory_store.py     # In-memory vector storage
```

### 🔗 Branch
```bash
git checkout sprint-3
```

---

## Sprint 4: RAG with Vector Database
**Session 4 - Pinecone & LangChain**  
**Workshop 4 - Building Chatbot RAG Systems with Vector Store, LangChain & Function Calling**

**📅 Timeline**: December 1-5, 2025 (5 days)  
**📅 Workshop**: Saturday, Dec 6 (1.5 hours)  
**👥 Team**: 7 members

### 🎯 Learning Objectives (từ khóa học)
**Pinecone:**
- Vector ingestion & manipulation
- Vector querying
- Pinecone indexes
- Retrieval Augmented Generation (RAG)
- Semantic search
- Context-aware chatbots
- Database performance tuning
- Storage optimization
- Query latency optimization

**LangChain:**
- LangChain overview
- LLM integration
- Data source integration
- Prompt management
- Application workflow design
- Multi-provider integration
- Building dynamic applications
- Intelligent application development

### 🎯 Project Goals
- Tích hợp Pinecone vector database
- Migrate từ custom RAG sang LangChain
- Production-ready RAG system
- Advanced retrieval strategies
- Monitoring & optimization

### 📋 Tasks
- [ ] Setup Pinecone database & indexes
- [ ] Migrate embeddings to Pinecone
- [ ] Implement LangChain RAG pipeline
- [ ] Compare performance: Custom (Sprint 3) vs LangChain
- [ ] Advanced retrieval strategies (MMR, reranking)
- [ ] Add citation/source tracking
- [ ] Implement caching layer
- [ ] Add monitoring & logging (LangSmith)
- [ ] Function calling integration
- [ ] Cost optimization
- [ ] Production deployment guide

### 📝 Related Assignments (Reference)
- Assignment 10: Using Pinecone to Retrieve Top 3 Similar Products
- Assignment 11: Build AI Agent for Weather & Search Queries
- Assignment 12: Aviation Satellite Image Cloud Detection

### 🎓 Assessment
- Quiz 04: Pinecone & LangChain (15 mins)
- Mock Interview 4: Vector DB & RAG concepts (10-15 mins)

### 🛠️ Tech Stack
- **LangChain** - RAG framework
- **Pinecone** - Managed vector database
- **LangSmith** - Monitoring & debugging
- Keep custom RAG code for comparison

### 🎯 Key Learning Points
- Khi nào nên dùng framework vs tự build
- Trade-offs: flexibility vs speed of development
- Production considerations: scaling, monitoring, costs
- Best practices từ LangChain ecosystem

### 📊 Comparison Matrix
| Feature | Custom (Sprint 3) | LangChain (Sprint 4) |
|---------|-------------------|----------------------|
| Setup time | Longer | Faster |
| Control | Full | Limited |
| Maintenance | More code | Less code |
| Debugging | Easier (you wrote it) | Harder (black box) |
| Features | Custom | Rich ecosystem |
| Production | DIY | Built-in patterns |

### 📂 New Modules
```
src/
├── vectorstore/
│   └── pinecone_store.py   # Pinecone integration
├── rag/
│   ├── pipeline.py         # RAG pipeline
│   ├── retriever.py        # Advanced retrieval
│   └── chain.py            # LangChain chains
└── monitoring/
    └── logger.py           # Logging & metrics
```

### 🔗 Branch
```bash
git checkout sprint-4
```

---

## Sprint 5: Advanced RAG & LangGraph
**Session 5 - RAG & LangGraph**  
**Hackathon - Building Advanced AI Applications**

**📅 Preparation**: December 8-12, 2025 (5 days)  
**📅 Hackathon**: Saturday, Dec 13, 2025 (8 hours)  
**👥 Team**: 7 members

### 🎯 Learning Objectives
**RAG with LangChain:**
- RAG fundamentals & patterns
- External data integration
- Vector databases (Pinecone, FAISS)
- LLM integration (GPT-4o-Mini)
- Graph RAG with knowledge graphs

**LangGraph & Agentic Systems:**
- Stateful graph execution
- Node branching & tool use
- Async flow management
- Multi-agent coordination
- Complex task automation

### 🎯 Hackathon Goals (8 hours)
Build production-ready AI application with:
- Advanced RAG implementation
- LangGraph workflows
- Multi-agent systems (optional)
- Real-world problem solving

### 📋 Key Tasks

**Pre-Hackathon (Dec 8-12)**:
- [ ] Study RAG & LangGraph concepts
- [ ] Review LangChain documentation
- [ ] Prepare project ideas
- [ ] Setup development environment
- [ ] Form team & assign roles

**Hackathon Day (Dec 13 - 8 hours)**:
- [ ] Define problem & architecture
- [ ] Implement RAG pipeline
- [ ] Build LangGraph workflows
- [ ] Integrate tools & agents
- [ ] Test & optimize
- [ ] Prepare presentation
- [ ] Demo & Q&A

### 📝 Related Assignments
- Assignment 13: Patient Information Chatbot Agent
- Assignment 14: Retail RAG Chatbot

### 🎓 Assessment
- Quiz 05: RAG & LangGraph (15 mins)
- Final Mock Interview: All concepts (30 mins)
- **Hackathon**: 8 hours project
- Post-Assessment: 70 mins

### 🔗 Branch
```bash
git checkout sprint-5
```

---

## 🔄 Sprint Workflow

### Bắt đầu Sprint mới
```bash
# Checkout sprint branch
git checkout -b sprint-X

# Cài đặt dependencies mới (nếu có)
pip install -r requirements.txt

# Chạy tests
pytest tests/
```

### Kết thúc Sprint
```bash
# Commit changes
git add .
git commit -m "feat(sprint-X): complete sprint X deliverables"

# Merge vào main
git checkout main
git merge sprint-X

# Push lên GitHub
git push origin main
git push origin sprint-X
```

---

## 📊 Progress Tracking

### Sprint 1: 🔄 60% Complete (Nov 10-14)
**Status**: IN PROGRESS - Day 1/5

**Completed** ✅:
- [x] Project setup & configuration
- [x] Gemini API integration
- [x] Basic chatbot logic
- [x] Gradio UI foundation
- [x] Export functionality (TXT/DOCX)
- [x] Prompt templates (5 languages)

**In Progress** 🔄:
- [ ] Error handling & validation
- [ ] Response optimization
- [ ] JSON parsing improvements
- [ ] UI/UX enhancements

**Remaining** 📋:
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Documentation completion
- [ ] Demo preparation
- [ ] Quiz 01 & Mock Interview 1

**Blockers**: None  
**Next Milestone**: Complete IN PROGRESS tasks by Nov 11

---

### Sprint 2: 📅 Not Started (Nov 17-21)
**Status**: PLANNED

**Key Tasks**:
- [ ] Abstract LLM interface
- [ ] OpenAI API integration
- [ ] Llama 3 integration (Ollama/Groq)
- [ ] Function calling
- [ ] Conversation memory
- [ ] Batching & retry mechanisms
- [ ] Streaming responses

**Dependencies**: Sprint 1 completion  
**Preparation**: Review OpenAI & Llama 3 docs

---

### Sprint 3: 📅 Not Started (Nov 24-28)
**Status**: PLANNED

**Key Tasks**:
- [ ] Hugging Face setup
- [ ] Sentence transformers integration
- [ ] Text chunking strategies
- [ ] In-memory vector store (NumPy)
- [ ] Cosine similarity search
- [ ] Context retrieval & ranking
- [ ] Semantic search UI
- [ ] **Build everything from scratch!**

**Dependencies**: Sprint 2 completion  
**Preparation**: Study embeddings concepts

---

### Sprint 4: 📅 Not Started (Dec 1-5)
**Status**: PLANNED

**Key Tasks**:
- [ ] Pinecone setup & indexes
- [ ] Migrate to Pinecone
- [ ] LangChain RAG pipeline
- [ ] Performance comparison (Custom vs LangChain)
- [ ] Advanced retrieval (MMR, reranking)
- [ ] Citation tracking
- [ ] Monitoring (LangSmith)
- [ ] Production deployment

**Dependencies**: Sprint 3 completion  
**Preparation**: Setup Pinecone account, study LangChain

---

### Sprint 5: 📅 Not Started (Dec 8-12)
**Status**: PLANNED

**Key Tasks**:
- [ ] Advanced RAG patterns
- [ ] Graph RAG implementation
- [ ] LangGraph workflows
- [ ] Multi-agent systems
- [ ] Agentic tool integration
- [ ] Hackathon project
- [ ] Final optimization
- [ ] Final assessment prep

**Dependencies**: Sprint 4 completion  
**Preparation**: Study LangGraph & agentic systems

---

## 📊 Overall Project Progress

| Sprint | Timeline | Status | Progress | Key Deliverable |
|--------|----------|--------|----------|-----------------|
| Sprint 1 | Nov 10-14 | 🔄 Active | 60% | Meeting Summarizer |
| Sprint 2 | Nov 17-21 | 📅 Planned | 0% | Multi-LLM System |
| Sprint 3 | Nov 24-28 | 📅 Planned | 0% | Custom RAG |
| Sprint 4 | Dec 1-5 | 📅 Planned | 0% | LangChain RAG |
| Sprint 5 | Dec 8-12 | 📅 Planned | 0% | Agentic System |
| **TOTAL** | **5 weeks** | | **12%** | **Production AI App** |

**Last Updated**: November 10, 2025  
**Current Focus**: Sprint 1 - Foundation  
**Next Milestone**: Sprint 1 completion (Nov 14)

---

## 🎓 Learning Philosophy & Outcomes

### 📚 Progressive Learning Approach

**Phase 1: Foundation (Sprint 1-2)**
- ✋ **Build from scratch** - Không dùng frameworks phức tạp
- 🎯 **Goal**: Hiểu core concepts của LLM applications
- 🛠️ **Tools**: Pure Python, API clients, Gradio

**Phase 2: Advanced Concepts (Sprint 3)**
- 🔨 **Custom RAG** - Tự implement retrieval system
- 🎯 **Goal**: Hiểu embeddings, vector search, semantic retrieval
- 🛠️ **Tools**: Hugging Face, NumPy, custom vector store

**Phase 3: Production Ready (Sprint 4)**
- 🚀 **Frameworks & Services** - LangChain, Pinecone
- 🎯 **Goal**: So sánh approaches, production deployment
- 🛠️ **Tools**: LangChain, Pinecone, monitoring tools

### 💡 Why This Approach?
✅ Hiểu sâu internal workings trước khi dùng frameworks  
✅ Debug & troubleshoot hiệu quả hơn  
✅ Biết khi nào nên tự build vs dùng framework  
✅ Tự tin customize cho use cases đặc biệt  

---

## 🎯 Learning Outcomes by Sprint

### Sprint 1: LLM Basics
**Skills:**
- Python environment & dependency management
- API integration (OpenAI/Gemini)
- Prompt engineering fundamentals
- Basic UI with Gradio
- Error handling & validation

**Deliverables:**
- Working chatbot với 1 LLM provider
- Clean code structure
- Basic tests

---

### Sprint 2: Multi-LLM Architecture
**Skills:**
- Abstract interfaces & polymorphism
- Multi-provider architecture
- Conversation state management
- Streaming responses
- Advanced prompt techniques

**Deliverables:**
- Support 3+ LLM providers
- Conversation memory
- Improved UX với streaming

---

### Sprint 3: RAG from Scratch
**Skills:**
- Text embeddings & vector representations
- Cosine similarity & semantic search
- Document chunking strategies
- Context retrieval & ranking
- Performance optimization

**Deliverables:**
- Custom RAG pipeline
- Semantic search functionality
- Efficient vector operations
- **NO LangChain/Pinecone yet** - tự build để học!

**Key Concepts:**
```
Document → Chunks → Embeddings → Vector Store
                                      ↓
Query → Embedding → Similarity Search → Top-K Chunks
                                      ↓
                            Context + Query → LLM → Answer
```

---

### Sprint 4: Production RAG
**Skills:**
- LangChain framework
- Managed vector databases (Pinecone)
- RAG best practices
- Production deployment
- Monitoring & observability
- Cost optimization

**Deliverables:**
- LangChain-based RAG
- Pinecone integration
- Side-by-side comparison: Custom vs Framework
- Production-ready deployment
- Monitoring dashboard

**Architecture Comparison:**
```
Custom RAG (Sprint 3):
├── Full control
├── Lightweight
├── Custom optimizations
└── More code to maintain

LangChain RAG (Sprint 4):
├── Quick to build
├── Best practices built-in
├── Rich ecosystem
└── Less control over internals
```

---

## 📚 Resources

### Sprint 1
- [Gemini API Docs](https://ai.google.dev/docs)
- [Gradio Documentation](https://gradio.app/docs)

### Sprint 2
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Llama 3 Guide](https://llama.meta.com/)
- [Ollama Documentation](https://ollama.ai/)

### Sprint 3
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS Documentation](https://faiss.ai/)

### Sprint 4
- [Pinecone Docs](https://docs.pinecone.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
