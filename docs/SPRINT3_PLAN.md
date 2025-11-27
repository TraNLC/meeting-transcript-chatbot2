# Sprint 3 Plan - Audio Recording & STT Integration

## 🎯 Objective
Add real-time audio recording and speech-to-text capabilities to Meeting Analyzer.

## 📋 Phases

### Phase 1: Basic Recording (Week 1) ✅ CURRENT
**Goal:** Browser-based microphone recording in Gradio UI

**Tasks:**
- [x] Add "🎙️ Recording" tab to main UI
- [x] Implement browser-based audio recording
- [x] Save audio files to `data/recordings/`
- [x] Manual upload and test workflow
- [x] Audio player for playback

**Deliverables:**
- Recording tab in `gradio_app_final.py`
- Audio storage system
- Basic recording controls (Start/Stop/Save)

**Effort:** 8-10 hours

---

### Phase 2: System Audio Capture (Week 2) 🔜 NEXT
**Goal:** Python background service for system audio

**Tasks:**
- [ ] Python background service with `sounddevice`
- [ ] System audio capture (meeting audio)
- [ ] API communication with Gradio
- [ ] Auto-process workflow
- [ ] Recording metadata tracking

**Deliverables:**
- `src/audio/recorder.py` - Background recording service
- `src/audio/audio_manager.py` - Audio file management
- API endpoints for control

**Effort:** 12-15 hours

**Tech Stack:**
- `sounddevice` - System audio capture
- `wave` - WAV file handling
- `pydub` - Audio processing (optional)

---

### Phase 3: STT Integration (Week 3) 🔮 FUTURE
**Goal:** Automatic speech-to-text transcription

**Tasks:**
- [ ] OpenAI Whisper API integration
- [ ] Auto-generate transcript from audio
- [ ] Real-time transcription (optional)
- [ ] Speaker diarization
- [ ] Auto-save to ChromaDB

**Deliverables:**
- `src/audio/stt_processor.py` - Speech-to-text
- `src/audio/whisper_client.py` - Whisper API client
- Auto-transcription workflow

**Effort:** 10-12 hours

**Tech Stack Options:**
1. **OpenAI Whisper API** (Recommended)
   - Best quality
   - $0.006/minute
   - Fast processing
   - Multiple languages

2. **Google Speech-to-Text**
   - Good quality
   - Cheaper
   - Real-time capable

3. **Whisper Local**
   - Free
   - Slower
   - Requires GPU for speed

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Gradio UI                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Analysis   │  │   Recording  │  │    Search    │  │
│  │     Tab      │  │     Tab      │  │     Tab      │  │
│  └──────────────┘  └──────┬───────┘  └──────────────┘  │
└────────────────────────────┼────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│              Audio Recording Module                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Browser    │  │   System     │  │     STT      │  │
│  │  Recording   │  │   Audio      │  │  Processor   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Audio     │  │  Transcripts │  │   ChromaDB   │  │
│  │    Files     │  │     Text     │  │   Vectors    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
data/
├── recordings/              # Audio files
│   ├── 20241125_143022.wav
│   └── 20241125_150033.wav
├── transcripts/             # Generated transcripts
│   ├── 20241125_143022.txt
│   └── 20241125_150033.txt
└── chroma_db/              # Vector database

src/
├── audio/                   # NEW MODULE
│   ├── __init__.py
│   ├── recorder.py         # Recording logic
│   ├── audio_manager.py    # File management
│   ├── stt_processor.py    # Speech-to-text
│   └── whisper_client.py   # Whisper API
├── ui/
│   └── gradio_app_final.py # Updated with recording tab
└── vectorstore/
    └── chroma_manager.py   # Auto-store transcripts
```

## 🎨 UI Design

### Recording Tab Layout

```
┌─────────────────────────────────────────────────────────┐
│  🎙️ Audio Recording                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Recording Controls                             │    │
│  │                                                 │    │
│  │  [🔴 Start Recording]  [⏹️ Stop]  [💾 Save]    │    │
│  │                                                 │    │
│  │  Status: ⚪ Ready                               │    │
│  │  Duration: 00:00:00                            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Audio Player                                   │    │
│  │  [▶️ Play] [⏸️ Pause] ━━━━━━━━━━━━━━━━━━━━━━  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Recent Recordings                              │    │
│  │  📁 20241125_143022.wav (5:23) [Process]       │    │
│  │  📁 20241125_150033.wav (3:45) [Process]       │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  [🔄 Process Selected] [🗑️ Delete]                     │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Workflow

### Phase 1 Workflow (Current)
```
User clicks "Start Recording"
    ↓
Browser captures microphone audio
    ↓
User clicks "Stop Recording"
    ↓
Audio saved to data/recordings/
    ↓
User clicks "Process"
    ↓
Manual upload to Analysis tab
```

### Phase 2 Workflow (Future)
```
Background service starts
    ↓
Captures system audio (Zoom/Teams/etc.)
    ↓
Auto-saves every N minutes
    ↓
Notifies UI of new recording
    ↓
User reviews and processes
```

### Phase 3 Workflow (Future)
```
Recording completed
    ↓
Auto-send to Whisper API
    ↓
Generate transcript
    ↓
Auto-analyze with universal_executor
    ↓
Store in ChromaDB
    ↓
Notify user of completion
```

## 📊 Success Metrics

### Phase 1
- ✅ Can record audio from browser
- ✅ Audio files saved correctly
- ✅ Can play back recordings
- ✅ Can manually process recordings

### Phase 2
- ⏳ System audio capture works
- ⏳ Background service stable
- ⏳ Auto-save every 5 minutes
- ⏳ No audio quality loss

### Phase 3
- ⏳ Transcription accuracy >90%
- ⏳ Processing time <1 minute per 10 minutes audio
- ⏳ Auto-analysis works end-to-end
- ⏳ Speaker diarization functional

## 💰 Cost Estimation (Phase 3)

### OpenAI Whisper API
- **Price:** $0.006 per minute
- **1 hour meeting:** $0.36
- **10 meetings/day:** $3.60/day
- **Monthly (200 meetings):** ~$72/month

### Google Speech-to-Text
- **Price:** $0.004 per 15 seconds
- **1 hour meeting:** $0.96
- **Monthly (200 meetings):** ~$192/month

### Whisper Local (Free)
- **Cost:** $0
- **Requirement:** GPU recommended
- **Speed:** Slower than API

**Recommendation:** Start with OpenAI Whisper API for best quality/price ratio.

## 🚀 Getting Started (Phase 1)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch App
```bash
python src/ui/gradio_app_final.py
```

### 3. Test Recording
1. Go to "🎙️ Recording" tab
2. Click "Start Recording"
3. Speak into microphone
4. Click "Stop Recording"
5. Click "Save"
6. Play back to verify

## 🔧 Configuration

### Audio Settings
```python
# src/config/settings.py

# Recording
SAMPLE_RATE = 16000  # 16kHz for speech
CHANNELS = 1         # Mono
AUDIO_FORMAT = "wav" # WAV format

# Storage
RECORDINGS_DIR = "data/recordings"
TRANSCRIPTS_DIR = "data/transcripts"

# STT (Phase 3)
WHISPER_API_KEY = "sk-..."
WHISPER_MODEL = "whisper-1"
```

## 📝 Notes

### Browser Recording Limitations
- Only captures microphone input
- Cannot capture system audio (Zoom/Teams)
- Requires user permission
- Works in Chrome, Firefox, Safari

### System Audio Capture (Phase 2)
- Requires Python background service
- Platform-specific (Windows/Mac/Linux)
- May need admin permissions
- Can capture all system audio

### STT Considerations (Phase 3)
- Whisper supports 50+ languages
- Speaker diarization requires additional processing
- Real-time transcription needs streaming API
- Local Whisper needs ~5GB disk space

## 🐛 Known Issues & Solutions

### Issue: No microphone permission
**Solution:** Browser will prompt for permission on first use

### Issue: Audio quality poor
**Solution:** Adjust sample rate in settings (try 44100 Hz)

### Issue: Large file sizes
**Solution:** Use MP3 compression (Phase 2)

### Issue: Background noise
**Solution:** Add noise reduction preprocessing (Phase 2)

## 📚 References

- [Gradio Audio Documentation](https://www.gradio.app/docs/audio)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [sounddevice Documentation](https://python-sounddevice.readthedocs.io/)
- [ChromaDB Integration Guide](./CHROMADB_INTEGRATION.md)

## 🎯 Next Steps

1. ✅ Complete Phase 1 implementation
2. Test with real meetings
3. Gather user feedback
4. Plan Phase 2 system audio capture
5. Evaluate STT providers for Phase 3
