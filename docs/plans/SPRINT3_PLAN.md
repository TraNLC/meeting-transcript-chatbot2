# 🚀 Sprint 3 Plan - Text-to-Speech Chatbot with Vector DB

**Workshop Date**: Saturday, November 30, 2025  
**Duration**: 6 hours (Offline at sites)  
**Format**: Offline (HN: Hoa Lac, DN: F-Complex, HCM: F-Town)  
**Team**: Team 3 - Akatsuki

---

## 📋 Workshop 3 Requirements

### 🎯 Goal
Build complete chatbot system that:
- Stores & retrieves knowledge using **ChromaDB** (vector database)
- Uses **OpenAI SDK** for natural language responses
- Converts text to speech using **HuggingFace TTS** (VITS model)

### ✅ Deliverables (6 hours)
1. **ChromaDB** storing mock data (queries, FAQs, knowledge base)
2. **OpenAI SDK** generating natural language responses
3. **HuggingFace TTS** converting responses to spoken audio
4. **Working codebase** with simple interface (CLI or web)
5. **Tested conversation logs** demonstrating multi-turn interaction
6. **Demo presentation** showing capabilities & insights

---

## ⏰ Workshop Schedule (6 Hours)

### Hour 1 (9:00-10:00 AM): Setup & Design
- [ ] Team introduction & role assignment (15 mins)
- [ ] Problem definition & use case selection (20 mins)
- [ ] Design system architecture (25 mins)

### Hour 2 (10:00-11:00 AM): ChromaDB Setup
- [ ] Install ChromaDB (10 mins)
- [ ] Design data schema (20 mins)
- [ ] Create & populate mock data (30 mins)

### Hour 3 (11:00 AM-12:00 PM): Vector Search
- [ ] Implement embeddings (20 mins)
- [ ] Build search functionality (30 mins)
- [ ] Test retrieval accuracy (10 mins)

**Lunch Break**: 12:00-1:00 PM

### Hour 4 (1:00-2:00 PM): OpenAI Integration
- [ ] Setup OpenAI SDK (10 mins)
- [ ] Integrate with ChromaDB retrieval (30 mins)
- [ ] Test response generation (20 mins)

### Hour 5 (2:00-3:00 PM): Text-to-Speech
- [ ] Setup HuggingFace TTS (VITS) (20 mins)
- [ ] Implement audio conversion (25 mins)
- [ ] Test audio output (15 mins)

### Hour 6 (3:00-4:00 PM): Testing & Demo
- [ ] End-to-end testing (20 mins)
- [ ] Prepare demo (20 mins)
- [ ] Team presentation (20 mins)

---

## 📅 Pre-Workshop Prep (Nov 24-29)

### Technical Setup
- [ ] Install ChromaDB: `pip install chromadb`
- [ ] Install HuggingFace: `pip install transformers`
- [ ] Install TTS libraries: `pip install TTS`
- [ ] Test OpenAI SDK
- [ ] Prepare development environment

### Knowledge Prep
- [ ] Study ChromaDB documentation
- [ ] Learn vector embeddings basics
- [ ] Review HuggingFace TTS models
- [ ] Understand RAG concepts

### Mock Data
- [ ] Prepare FAQ dataset
- [ ] Create knowledge base content
- [ ] Sample user queries
- [ ] Test data schema

---

## 💻 Key Technical Components

### 1. ChromaDB Setup
```python
import chromadb

# Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection("knowledge_base")

# Add documents
collection.add(
    documents=["FAQ 1", "FAQ 2"],
    metadatas=[{"type": "faq"}, {"type": "faq"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["user question"],
    n_results=3
)
```

### 2. OpenAI + ChromaDB
```python
# Retrieve context
context = collection.query(query_texts=[user_query])

# Generate response
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Context: {context}"},
        {"role": "user", "content": user_query}
    ]
)
```

### 3. HuggingFace TTS
```python
from TTS.api import TTS

# Initialize TTS
tts = TTS(model_name="tts_models/en/vctk/vits")

# Convert text to speech
tts.tts_to_file(
    text="Response text",
    file_path="output.wav"
)
```

---

## 🎯 Use Case Ideas

### Option 1: Customer Support Bot
- Knowledge base: Product FAQs, troubleshooting guides
- Voice responses for accessibility

### Option 2: Educational Assistant
- Knowledge base: Course materials, Q&A
- Audio explanations for learning

### Option 3: Company Knowledge Bot
- Knowledge base: Internal docs, policies
- Voice interface for hands-free access

---

## 👥 Team Roles (5 members)

### Role 1: Team Lead
- Coordinate activities
- Time management
- Final presentation

### Role 2: Data Engineer
- ChromaDB setup
- Mock data creation
- Vector search implementation

### Role 3: AI Engineer
- OpenAI integration
- RAG pipeline
- Response generation

### Role 4: Audio Engineer
- HuggingFace TTS setup
- Audio conversion
- Quality testing

### Role 5: QA & Documentation
- Testing
- Conversation logs
- Demo preparation

---

## ✅ Success Criteria

### Technical
- [ ] ChromaDB storing & retrieving data
- [ ] OpenAI generating relevant responses
- [ ] TTS producing clear audio
- [ ] Multi-turn conversation working
- [ ] Simple interface (CLI/web)

### Presentation
- [ ] Clear problem definition
- [ ] Live demo successful
- [ ] Audio output demonstrated
- [ ] Insights shared

---

## 💡 Tips

- 🎯 Keep it simple - focus on core features
- 🔊 Test audio quality early
- 📊 Prepare good mock data
- ⏰ Timebox each phase
- 🤝 Collaborate actively

## 🚨 Avoid

- ❌ Complex data schemas
- ❌ Too much mock data
- ❌ Poor audio quality
- ❌ Over-engineering

---

**Workshop**: Saturday, Nov 30, 2025 | 9 AM - 4 PM | Offline  
**Location**: HN: Hoa Lac | DN: F-Complex | HCM: F-Town  
**Team**: Team 3 - Akatsuki 🔥
