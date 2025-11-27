# ChromaDB Integration Guide

## Overview

ChromaDB integration adds semantic search capabilities to the Meeting Analyzer, allowing you to:
- Store meeting transcripts with vector embeddings
- Search meetings by meaning, not just keywords
- Find similar meetings automatically
- Track meeting history with rich metadata

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Meeting Analysis                       │
│              (universal_executor.py)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ChromaDB Manager                            │
│           (chroma_manager.py)                            │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Sentence   │      │   ChromaDB   │                │
│  │ Transformers │──────│   Storage    │                │
│  └──────────────┘      └──────────────┘                │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Semantic Search UI                          │
│          (semantic_search_app.py)                        │
└─────────────────────────────────────────────────────────┘
```

## Installation

### 1. Install Dependencies

```bash
pip install chromadb sentence-transformers
```

Or update from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python test_chromadb.py
```

Expected output:
```
============================================================
TESTING CHROMADB INTEGRATION
============================================================

1. Initializing ChromaDB...
   ✓ ChromaDB initialized

2. Storing sample meeting...
   ✓ Sample meeting stored

3. Getting statistics...
   Total meetings: 1
   By type: {'workshop': 1}
   By language: {'en': 1}

4. Testing semantic search...
   Found 1 results
   ...
```

## Usage

### 1. Automatic Storage (Recommended)

When using `universal_executor`, meetings are automatically stored in ChromaDB:

```python
from src.rag.universal_executor import UniversalMeetingExecutor

executor = UniversalMeetingExecutor(
    transcript=transcript_text,
    meeting_type="workshop",
    output_language="vi"
)

# This automatically stores in ChromaDB
results = executor.execute_all(store_in_vectordb=True)
```

### 2. Manual Storage

```python
from src.vectorstore.chroma_manager import ChromaManager

chroma = ChromaManager()

chroma.store_meeting(
    meeting_id="meeting_001",
    transcript=transcript_text,
    analysis=analysis_results,
    meeting_type="workshop",
    language="en"
)
```

### 3. Semantic Search

```python
# Search by content
results = chroma.semantic_search(
    query="React Hooks training",
    n_results=5,
    meeting_type="workshop",
    language="en"
)

for result in results:
    print(f"Meeting: {result['meeting_id']}")
    print(f"Similarity: {result['distance']}")
    print(f"Preview: {result['transcript'][:200]}")
```

### 4. Find Similar Meetings

```python
# Find meetings similar to a specific one
similar = chroma.find_similar_meetings(
    meeting_id="meeting_001",
    n_results=3
)
```

## Semantic Search UI

Launch the standalone semantic search interface:

```bash
python src/ui/semantic_search_app.py
```

Access at: http://localhost:7865

### Features:

1. **Semantic Search Tab**
   - Search by keywords or questions
   - Filter by meeting type and language
   - Adjust number of results
   - View similarity scores

2. **Find Similar Tab**
   - Enter a meeting ID
   - Find similar meetings automatically
   - Useful for finding related discussions

3. **Statistics**
   - Total meetings stored
   - Breakdown by type and language
   - Real-time updates

## Migration

### Migrate Existing History

Convert existing meeting history to ChromaDB:

```bash
cd src/vectorstore
python migrate_history.py
```

This will:
- Scan `data/history/` folder
- Convert each meeting to vector embeddings
- Store in ChromaDB with metadata
- Skip already migrated meetings

## Data Storage

### Directory Structure

```
data/
├── chroma_db/              # ChromaDB persistence
│   ├── chroma.sqlite3      # Vector database
│   └── analysis/           # Full analysis JSON files
│       ├── meeting_001.json
│       └── meeting_002.json
└── history/                # Original history (kept for backup)
```

### Metadata Stored

For each meeting:
- `meeting_type`: meeting, workshop, brainstorming
- `language`: en, vi, ja, ko, etc.
- `timestamp`: ISO format datetime
- `transcript_length`: Character count
- `has_participants`: Boolean
- `has_action_items`: Boolean
- `has_decisions`: Boolean
- `has_key_learnings`: Boolean (workshops)
- `has_exercises`: Boolean (workshops)
- `has_qa_pairs`: Boolean (workshops)

## How Semantic Search Works

### 1. Embedding Generation

Uses `sentence-transformers/all-MiniLM-L6-v2` model:
- Fast and lightweight (80MB)
- 384-dimensional vectors
- Supports multiple languages
- Good balance of speed and accuracy

### 2. Similarity Calculation

ChromaDB uses cosine similarity:
- Distance 0.0 = identical
- Distance 1.0 = completely different
- Typical matches: 0.3-0.7 range

### 3. Example Queries

**Keyword Search (Old Way):**
```
Query: "budget"
Finds: Only meetings with exact word "budget"
```

**Semantic Search (New Way):**
```
Query: "budget planning"
Finds:
- "financial planning meeting"
- "cost estimation discussion"
- "ngân sách marketing" (Vietnamese)
- "quarterly spending review"
```

## Use Cases

### 1. Knowledge Discovery

Find all meetings about a topic:
```python
results = chroma.semantic_search("React training")
# Returns: workshops, Q&A sessions, code reviews about React
```

### 2. Duplicate Detection

Before analyzing a new meeting:
```python
similar = chroma.semantic_search(new_transcript, n_results=1)
if similar and similar[0]['distance'] < 0.2:
    print("Similar meeting already exists!")
```

### 3. Meeting Recommendations

After analyzing a meeting:
```python
similar = chroma.find_similar_meetings(current_meeting_id)
print("You might also be interested in:")
for meeting in similar:
    print(f"- {meeting['meeting_id']}")
```

### 4. Trend Analysis

Find patterns over time:
```python
all_meetings = chroma.get_all_meetings()
# Analyze topics, participants, action items over time
```

## Performance

### Benchmarks

- **Storage**: ~100ms per meeting
- **Search**: ~50ms for 100 meetings
- **Embedding**: ~200ms per transcript (1000 words)

### Optimization Tips

1. **Batch Processing**: Store multiple meetings at once
2. **Chunking**: For very long transcripts (>5000 words), consider chunking
3. **Caching**: Embeddings are cached automatically
4. **Persistence**: ChromaDB persists to disk, no need to reload

## Troubleshooting

### Issue: "No module named 'chromadb'"

```bash
pip install chromadb sentence-transformers
```

### Issue: "Collection already exists"

ChromaDB reuses existing collections. To reset:

```python
chroma.client.delete_collection("meetings")
```

### Issue: Slow embedding generation

First run downloads the model (~80MB). Subsequent runs are fast.

### Issue: Out of memory

For large transcripts, reduce `max_length` in preprocessing:

```python
transcript = preprocessor.truncate_text(transcript, max_length=10000)
```

## API Reference

### ChromaManager

```python
class ChromaManager:
    def __init__(self, persist_directory: str = "data/chroma_db")
    
    def store_meeting(
        self,
        meeting_id: str,
        transcript: str,
        analysis: Dict[str, Any],
        meeting_type: str = "meeting",
        language: str = "en"
    ) -> bool
    
    def semantic_search(
        self,
        query: str,
        n_results: int = 5,
        meeting_type: Optional[str] = None,
        language: Optional[str] = None
    ) -> List[Dict[str, Any]]
    
    def find_similar_meetings(
        self,
        meeting_id: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]
    
    def delete_meeting(self, meeting_id: str) -> bool
    
    def get_statistics(self) -> Dict[str, Any]
```

## Next Steps

1. **HuggingFace TTS Integration**: Convert search results to audio
2. **Advanced Filtering**: Add date range, participant filters
3. **Clustering**: Group similar meetings automatically
4. **Recommendations**: Suggest relevant meetings based on current context

## Related Documentation

- [Sprint 2 Summary](SPRINT2_SUMMARY.md)
- [Function Calling System](../src/rag/README.md)
- [Meeting Types](../src/rag/meeting_types.py)
