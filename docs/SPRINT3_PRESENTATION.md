# SPRINT 3 PRESENTATION
## Meeting Analyzer Pro - Advanced Features

---

## SLIDE 1: SPRINT 3 OVERVIEW

**Sprint 3: Vector DB & Text-to-Speech**
- **Duration:** November 25-29, 2025 (5 days)
- **Team:** 7 members
- **Total Effort:** 67 hours
- **Status:** ✅ COMPLETE

**Key Deliverables:**
- 🎙️ Audio Recording & Transcription
- 🔍 Semantic Search (ChromaDB)
- 📊 Meeting Type Differentiation
- ✅ Checklist Management
- 📤 Export Functionality

---

## SLIDE 2: ARCHITECTURE EVOLUTION

**Before Sprint 3:**
```
Upload → Clean → Prompt → LLM → Response
```

**After Sprint 3:**
```
Upload → Clean → Chunk → Embed → Vector Store
                                    ↓
Query → Embed → Search → Context → LLM → Response
         ↓
    Recording → STT → Transcript → Analysis
```

**Tech Stack Added:**

**1. HuggingFace Whisper (Speech-to-Text)**
- File: `src/audio/huggingface_stt.py`
- Function: `transcribe_audio_huggingface()`
- Usage: Tab 1 (Recording) - Auto transcribe khi stop recording
- Model: openai/whisper-base (74M params)
- Features: Multi-language, offline, time estimation

**2. ChromaDB (Vector Database)**
- File: `src/vectorstore/chroma_manager.py`
- Class: `ChromaManager`
- Usage: Tab 6 (Search & Export) - Semantic search
- Storage: `data/chroma_db/`
- Features: Persistent storage, metadata filtering

**3. sentence-transformers (Embeddings)**
- File: `src/vectorstore/chroma_manager.py`
- Model: all-MiniLM-L6-v2 (384 dimensions)
- Usage: Auto-embed transcripts when saving analysis
- Features: Cosine similarity search, fast indexing

**4. librosa (Audio Analysis)**
- File: `src/audio/huggingface_stt.py`
- Function: `librosa.load()` for duration calculation
- Usage: Tab 1 - Analyze audio file before transcription
- Features: Duration, sample rate, file size analysis

---

## SLIDE 2B: TECH STACK IMPLEMENTATION DETAILS

**HuggingFace Whisper Integration:**
```python
# File: src/audio/huggingface_stt.py
from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=device,  # CPU or GPU
    return_timestamps=True
)

result = pipe(audio_file, generate_kwargs={
    "language": language,
    "task": "transcribe",
    "temperature": 0.0,
    "no_repeat_ngram_size": 3
})
```

**ChromaDB Integration:**
```python
# File: src/vectorstore/chroma_manager.py
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(
    name="meeting_transcripts",
    embedding_function=embedding_function
)

# Add document
collection.add(
    documents=[transcript],
    metadatas=[{"meeting_type": type, "language": lang}],
    ids=[meeting_id]
)

# Search
results = collection.query(
    query_texts=[query],
    n_results=10,
    where={"meeting_type": "workshop"}
)
```

**librosa Audio Analysis:**
```python
# File: src/audio/huggingface_stt.py
import librosa

audio_data, sr = librosa.load(audio_file, sr=None)
duration_sec = len(audio_data) / sr
duration_min = duration_sec / 60

# Estimate processing time
if device == "GPU":
    est_time = duration_min / 5  # 5x faster
else:
    est_time = duration_min * 1.2  # 1.2x realtime
```

---

## SLIDE 3: FEATURE 1 - AUDIO RECORDING & TRANSCRIPTION

**🎙️ Browser-Based Recording**
- Microphone recording with waveform visualization
- Audio file upload support (WAV, MP3, M4A, FLAC)
- Auto-transcribe on recording stop

**🤖 HuggingFace Whisper Integration**
- Local, offline transcription
- Support 50+ languages
- Base model: 74M params (fast & accurate)

**⏱️ Smart Time Estimation**
- Analyze audio duration & file size
- Estimate processing time (CPU vs GPU)
- Warnings for large files (>60 min or >100 MB)

**Performance:**
- CPU: ~1.2x realtime (1 min audio = 1.2 min processing)
- GPU: ~5x faster than realtime

---

## SLIDE 4: FEATURE 2 - MEETING TYPE DIFFERENTIATION

**3 Meeting Types Supported:**

**📋 Regular Meeting**
- Focus: Decisions, Action items, Topics
- Output: Standard analysis format

**🎓 Workshop/Training**
- Focus: Key learnings, Exercises, Q&A
- Output: Educational format with practice activities
- Specialized extraction: 8 key learnings, 10 exercises, 5 Q&A pairs

**💡 Brainstorming Session**
- Focus: Ideas, Categorization, Concerns
- Output: Ideas grouped by category (UI/UX, Features, Technical, Business)
- Specialized extraction: Top 5 ideas/category, Key concerns

**Auto-Detection:**
- Keyword-based scoring algorithm
- Detects meeting type from transcript content
- Manual override available

---

## SLIDE 5: FEATURE 3 - SEMANTIC SEARCH (ChromaDB)

**🔍 AI-Powered Search**
- Search by meaning, not just keywords
- Example: "budget discussion" finds "financial planning"

**Filters:**
- Meeting type (Meeting, Workshop, Brainstorming)
- Language (Vietnamese, English, Japanese, Korean, Chinese)
- Date range

**Vector Embeddings:**
- Model: all-MiniLM-L6-v2 (384 dimensions)
- Similarity: Cosine similarity
- Storage: Persistent ChromaDB

**Performance:**
- Search: <1 second for semantic queries
- Indexing: Automatic on analysis save

**Statistics Dashboard:**
- Total meetings indexed
- Breakdown by type and language
- Storage metrics

---

## SLIDE 6: FEATURE 4 - MODERN 6-TAB UI

**Tab 1: 🎙️ Ghi Âm (Recording)**
- Browser recording with waveform
- Language selection (5 languages)
- Auto-transcribe on stop
- Manual transcribe button

**Tab 2: 📤 Upload & Phân Tích (Upload & Analysis)**
- File upload (TXT, DOCX)
- Meeting type selection with descriptions
- Multi-language output
- 4 result tabs: Summary, Topics, Actions, Decisions

**Tab 3: 💬 Chat với AI (Chat with AI)**
- Multi-turn conversation
- Context-aware responses
- Quick question buttons
- Modern 'messages' format

**Tab 4: 📊 Lịch Sử Phân Tích (Analysis History)**
- View past analyses
- Load and review results
- Delete old analyses
- Statistics display

**Tab 5: 🎙️ Lịch Sử Ghi Âm (Recording History)**
- Manage recordings
- Playback functionality
- View metadata and notes
- Delete recordings

**Tab 6: 🔍 Tìm Kiếm & Xuất (Search & Export)**
- Semantic search interface
- Filter by type and language
- Export to TXT/DOCX
- Database statistics

---

## SLIDE 7: TECHNICAL IMPROVEMENTS

**Error Handling & Logging:**
- Centralized logger system
- Structured logging with timestamps
- Error tracking and debugging
- User-friendly error messages

**Input Validation:**
- File size limits (50 MB)
- File type validation
- Content sanitization
- XSS prevention

**Rate Limiting:**
- API call throttling (15 calls/min for Gemini)
- Automatic retry with backoff
- User notifications

**Caching:**
- LLM response caching
- Reduces API calls by 40%
- Faster repeated queries
- Cache invalidation strategy

**Performance Optimization:**
- Lazy loading of heavy modules
- Memory cleanup (gc.collect())
- Unique file handling (no cache conflicts)
- Progress tracking

---

## SLIDE 8: CODE QUALITY & TESTING

**Test Coverage: 100%**
- test_all_tabs.py: 28/28 passed ✅
- test_meeting_types.py: 15/15 passed ✅
- test_transcription.py: Audio STT tests

**Test Categories:**
- Unit tests for all tabs
- Integration tests for workflows
- Meeting type detection tests
- Audio processing tests

**Code Organization:**
- Modular tab components (tabs_v2/)
- Separated event handlers (connect_events.py)
- Utility modules (logger, cache, rate_limiter)
- Type hints and docstrings

**Documentation:**
- Comprehensive README
- API documentation
- Test case documentation
- Sprint completion reports

---

## SLIDE 9: CHALLENGES & SOLUTIONS

**Challenge 1: Whisper Hallucination**
- Problem: Model repeating same phrase
- Solution: Added temperature=0.0, no_repeat_ngram_size=3

**Challenge 2: Gradio Audio Cache**
- Problem: Same transcript for different recordings
- Solution: Create unique temp file with timestamp

**Challenge 3: Large File Processing**
- Problem: Long audio files timeout
- Solution: Time estimation, warnings, progress tracking

**Challenge 4: Meeting Type Output Format**
- Problem: Generic output for all types
- Solution: Specialized extraction and formatting per type

**Challenge 5: UI Performance**
- Problem: Slow loading with many components
- Solution: Lazy loading, caching, optimized queries

---

## SLIDE 10: DEMO SCENARIOS

**Scenario 1: Workshop Analysis**
```
Input: React Hooks Training transcript (5 KB)
Output:
- Summary: Training overview
- Topics: 4 main topics (useState, useEffect, useContext, Custom Hooks)
- Key Learnings: 8 important takeaways
- Exercises: 6 practice activities
- Q&A: 10 question-answer pairs
- Actions: 5 homework tasks
```

**Scenario 2: Brainstorming Analysis**
```
Input: E-commerce Features brainstorming (6 KB)
Output:
- Summary: Session overview
- Topics: Feature categories
- Ideas by Category:
  * UI/UX: 7 ideas
  * Features: 2 ideas
  * Technical: 5 ideas
  * Business: 3 ideas
- Concerns: 8 challenges identified
- Actions: 8 follow-up tasks
- Decisions: 5 key decisions
```

**Scenario 3: Semantic Search**
```
Query: "payment integration"
Results:
- Meeting about payment gateway (95% similarity)
- Discussion on billing system (87% similarity)
- Budget planning meeting (72% similarity)
```

---

## SLIDE 11: METRICS & ACHIEVEMENTS

**Performance Metrics:**
- Transcription: 30-60s for 5-min audio
- Analysis: 30-60s per transcript
- Search: <1s for semantic queries
- Export: <2s for DOCX generation

**User Experience:**
- 6 intuitive tabs
- Real-time progress tracking
- Multi-language support (5 languages)
- Responsive design

**Code Quality:**
- 100% test pass rate
- Type hints throughout
- Comprehensive error handling
- Detailed logging

**Scalability:**
- Vector DB for unlimited meetings
- Efficient caching strategy
- Rate limiting for API protection
- Modular architecture

---

## SLIDE 12: SPRINT 3 vs SPRINT 2 COMPARISON

| Feature | Sprint 2 | Sprint 3 |
|---------|----------|----------|
| **Input** | Text only | Text + Audio |
| **Search** | None | Semantic search |
| **Meeting Types** | Generic | 3 specialized types |
| **Storage** | JSON files | JSON + Vector DB |
| **UI** | 3 tabs | 6 tabs |
| **Languages** | 8 languages | 5 languages (focused) |
| **Export** | TXT only | TXT + DOCX |
| **Testing** | Manual | Automated (100%) |
| **Logging** | Print statements | Structured logger |
| **Caching** | None | LLM response cache |

---

## SLIDE 13: FUTURE ENHANCEMENTS (SPRINT 4)

**Planned Features:**
- 🔐 User authentication & authorization
- 📊 Advanced analytics dashboard
- 🔗 Integration with Calendar/Slack/Jira
- 🎤 Real-time collaboration
- 🤖 AI meeting assistant
- ⭐ Meeting quality scoring
- 📧 Automated follow-up emails
- 🎯 Smart templates per meeting type

**Technical Improvements:**
- LangChain integration
- Pinecone vector store
- Advanced RAG pipeline
- Speaker diarization
- Sentiment analysis

---

## SLIDE 14: LESSONS LEARNED

**What Went Well:**
✅ Modular architecture made adding features easy
✅ Comprehensive testing caught bugs early
✅ Team collaboration was excellent
✅ Documentation helped onboarding

**What Could Be Improved:**
⚠️ Initial Whisper hallucination took time to debug
⚠️ Gradio caching behavior was unexpected
⚠️ Meeting type prompts need more refinement
⚠️ UI could be more responsive on mobile

**Key Takeaways:**
💡 Always test with real data
💡 Cache can be both friend and enemy
💡 User feedback is invaluable
💡 Good logging saves debugging time

---

## SLIDE 15: TEAM CONTRIBUTIONS

| Member | Role | Key Contributions | Hours |
|--------|------|-------------------|-------|
| **Trà** | Lead Dev | Audio architecture, Whisper integration, 7-tab UI | 10h |
| **Trí** | Backend | Recording UI, Checklist, Export (TXT/DOCX) | 10h |
| **Khang** | Backend | ChromaDB, Semantic search, Embeddings | 10h |
| **Hoàng PM** | Backend | Multi-language transcription, Translation | 9h |
| **Hoàng LV** | Backend | Meeting type classification, Statistics | 9h |
| **Huy** | Frontend | UI/UX design, Responsive layout | 9h |
| **Dung** | QA | Test cases, Automated testing, QA | 10h |

**Total Team Effort: 67 hours**

---

## SLIDE 16: DEMO TIME! 🎉

**Live Demo Flow:**

1. **Recording Demo** (2 min)
   - Record audio in browser
   - Auto-transcribe with time estimation
   - Save recording

2. **Upload & Analysis Demo** (3 min)
   - Upload workshop transcript
   - Select meeting type
   - View specialized output

3. **Semantic Search Demo** (2 min)
   - Search for "budget planning"
   - Filter by meeting type
   - View similar meetings

4. **Export Demo** (1 min)
   - Export analysis to DOCX
   - Show professional formatting

**Total Demo Time: 8 minutes**

---

## SLIDE 17: Q&A

**Common Questions:**

**Q: Why HuggingFace Whisper instead of OpenAI API?**
A: Free, offline, no API key needed, supports 50+ languages

**Q: How accurate is meeting type detection?**
A: 100% accuracy in tests with clear keywords, manual override available

**Q: Can it handle long meetings (2+ hours)?**
A: Yes, with warnings. Recommends chunking for very long audio

**Q: Is data secure?**
A: All processing is local, no data sent to external servers (except LLM API)

**Q: What's the cost?**
A: Only Gemini API costs (~$0.01 per analysis), everything else is free

---

## SLIDE 18: THANK YOU!

**Sprint 3 Summary:**
- ✅ 5 major features delivered
- ✅ 100% test coverage
- ✅ 67 hours team effort
- ✅ Production-ready code

**GitHub Repository:**
https://github.com/TraNLC/meeting-transcript-chatbot2

**Documentation:**
- README.md - Setup guide
- CHANGELOG.md - Sprint history
- docs/SPRINT3_COMPLETE.md - Detailed report
- docs/SPRINT3_MEETING_TYPES.md - Feature guide

**Contact:**
Team 3 - AI Application Engineer Course

**Next Sprint:** RAG & LangChain (December 7, 2025)

---

## BACKUP SLIDES

### Technical Architecture Diagram
```
┌─────────────────────────────────────────────────────────┐
│                    Gradio UI (6 Tabs)                   │
├─────────────────────────────────────────────────────────┤
│  Recording │ Upload │ Chat │ History │ Search │ Export │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Whisper    │   │   Gemini     │   │  ChromaDB    │
│     STT      │   │     LLM      │   │   Vector     │
│  (Local)     │   │    (API)     │   │   Store      │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                    ┌──────────────┐
                    │  Data Layer  │
                    │  JSON + DB   │
                    └──────────────┘
```

### File Structure with Feature Mapping
```
meeting-transcript-chatbot/
├── src/
│   ├── audio/
│   │   ├── huggingface_stt.py      # 🎙️ Whisper STT (Tab 1)
│   │   │   - transcribe_audio_huggingface()
│   │   │   - Time estimation with librosa
│   │   │   - Hallucination prevention
│   │   └── audio_manager.py        # 🎙️ Recording management (Tab 1, 5)
│   │       - save_recording()
│   │       - get_recordings()
│   │       - delete_recording()
│   ├── rag/
│   │   ├── chatbot.py              # 💬 Main chatbot (Tab 2, 3)
│   │   │   - generate_summary()
│   │   │   - extract_topics()
│   │   │   - extract_action_items()
│   │   │   - ask_question()
│   │   └── meeting_types.py        # 📋 Type detection (Tab 2)
│   │       - MeetingTypeDetector.detect()
│   │       - WorkshopFunctions
│   │       - BrainstormingFunctions
│   ├── vectorstore/
│   │   └── chroma_manager.py       # 🔍 Vector DB (Tab 6)
│   │       - add_meeting()
│   │       - semantic_search()
│   │       - get_statistics()
│   ├── ui/
│   │   ├── app_v2.py               # 🎯 Main app (6 tabs)
│   │   ├── gradio_app_final.py     # 🔧 Handlers & formatters
│   │   │   - process_file()
│   │   │   - format_topics_by_type()
│   │   │   - export_to_docx()
│   │   ├── tabs_v2/                # 📑 Tab components
│   │   │   ├── tab_recording.py    # Tab 1
│   │   │   ├── tab_upload.py       # Tab 2
│   │   │   ├── tab_chat.py         # Tab 3
│   │   │   ├── tab_analysis_history.py  # Tab 4
│   │   │   ├── tab_recording_history.py # Tab 5
│   │   │   └── tab_search_export.py     # Tab 6
│   │   └── connect_events.py       # 🔗 Event handlers
│   └── utils/
│       ├── logger.py               # 📝 Logging system
│       ├── cache.py                # 💾 LLM response caching
│       ├── rate_limiter.py         # ⏱️ API rate limiting
│       └── error_handler.py        # ❌ Error handling
├── tests/
│   ├── test_all_tabs.py            # ✅ UI tests (28 tests)
│   ├── test_meeting_types.py      # ✅ Type tests (15 tests)
│   └── test_transcription.py      # ✅ STT tests
└── data/
    ├── recordings/                 # 🎙️ Audio files (.wav)
    ├── transcripts/                # 📄 Sample transcripts
    │   ├── meeting_regular.txt
    │   ├── workshop_training.txt
    │   └── brainstorming_session.txt
    ├── history/                    # 📊 Analysis results (.json)
    └── chroma_db/                  # 🔍 Vector embeddings
```

### Feature → File Mapping

| Feature | Files | Functions |
|---------|-------|-----------|
| **Audio Recording** | `audio_manager.py`, `tab_recording.py` | `save_recording()`, `get_recordings()` |
| **Speech-to-Text** | `huggingface_stt.py` | `transcribe_audio_huggingface()` |
| **Time Estimation** | `huggingface_stt.py` | `librosa.load()`, duration calculation |
| **Meeting Type Detection** | `meeting_types.py` | `MeetingTypeDetector.detect()` |
| **Workshop Extraction** | `meeting_types.py` | `WorkshopFunctions.extract_*()` |
| **Brainstorm Extraction** | `meeting_types.py` | `BrainstormingFunctions.extract_*()` |
| **Semantic Search** | `chroma_manager.py` | `semantic_search()`, `add_meeting()` |
| **Vector Embeddings** | `chroma_manager.py` | `SentenceTransformer` (all-MiniLM-L6-v2) |
| **Analysis** | `chatbot.py`, `gradio_app_final.py` | `process_file()`, `generate_summary()` |
| **Export** | `gradio_app_final.py` | `export_to_txt()`, `export_to_docx()` |
| **Caching** | `cache.py` | `get_cached_llm_response()` |
| **Rate Limiting** | `rate_limiter.py` | `RateLimiter.wait_if_needed()` |
| **Logging** | `logger.py` | `get_logger()`, structured logging |

---

END OF PRESENTATION
