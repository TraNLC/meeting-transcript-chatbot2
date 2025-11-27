# TC_01 - Recording Tab

## General Information
- **Module:** Recording Tab
- **Priority:** High
- **Tester:** 
- **Date:** 11/27/2025

---

## TC_01.1 - Basic Recording

### Description
Test basic recording and automatic transcription functionality

### Preconditions
- Application running at http://localhost:7777
- ffmpeg installed
- Microphone working properly

### Test Steps
1. Open "🎙️ Recording" tab
2. Select language: "Tiếng Việt" (Vietnamese)
3. Click microphone icon
4. Say: "Hello, this is a recording test"
5. Click Stop button

### Expected Result
- ✅ Waveform displays during recording
- ✅ Auto-transcribe after Stop
- ✅ Display transcript: "📝 **Transcript (vi):** [date time]\n\nHello, this is a recording test"
- ✅ Transcript matches spoken content accurately

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.2 - Save Audio and Transcript

### Description
Test saving audio file and transcript to library

### Preconditions
- Completed TC_01.1
- Transcript displayed

### Test Steps
1. Enter title: "Test Recording 01"
2. Click "💾 Save Audio & Transcript" button
3. Check status message
4. Open "📚 Library > 🎙️ Recording History" tab
5. Click "🔄 Refresh"

### Expected Result
- ✅ Display message: "✅ Audio and transcript saved!"
- ✅ Display ID and file paths
- ✅ Audio file exists: `data/recordings/[ID].wav`
- ✅ Transcript file exists: `data/transcripts/[ID].txt`
- ✅ Recording appears in library list

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.3 - Cancel Recording

### Description
Test cancel and clear recording functionality

### Preconditions
- Recording completed but not saved

### Test Steps
1. Record any audio
2. Click Stop
3. Click "🗑️ Cancel" button

### Expected Result
- ✅ Audio player cleared
- ✅ Transcript cleared
- ✅ Status cleared
- ✅ Can record new audio immediately

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.4 - Multi-language Recording

### Description
Test transcription with different languages

### Preconditions
- Application running

### Test Data
| Language | Test Content | Expected Transcript |
|----------|--------------|---------------------|
| Vietnamese | "Xin chào Việt Nam" | Xin chào Việt Nam |
| English | "Hello World" | Hello World |
| Japanese | "こんにちは" | こんにちは |
| Korean | "안녕하세요" | 안녕하세요 |
| Chinese | "你好" | 你好 |

### Test Steps
1. Select language from dropdown
2. Record corresponding content
3. Click Stop
4. Check transcript

### Expected Result
- ✅ Transcript accurate for selected language
- ✅ No encoding errors
- ✅ Special characters display correctly

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.5 - Error Handling - Missing ffmpeg

### Description
Test error message when ffmpeg not installed

### Preconditions
- ffmpeg not installed (or not in PATH)

### Test Steps
1. Record audio
2. Click Stop

### Expected Result
- ✅ Clear error message displayed
- ✅ ffmpeg installation instructions provided
- ✅ ffmpeg download link included

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.6 - Error Handling - No Microphone

### Description
Test handling when microphone unavailable

### Preconditions
- No microphone or microphone disabled

### Test Steps
1. Click microphone icon

### Expected Result
- ✅ Browser error message displayed
- ✅ Microphone permission requested

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.7 - Performance - Long Recording

### Description
Test performance with long audio

### Preconditions
- Application running

### Test Steps
1. Record continuously for 5 minutes
2. Click Stop
3. Measure transcription time

### Expected Result
- ✅ Recording not interrupted
- ✅ Transcription completes in < 2 minutes
- ✅ Transcript complete, not truncated

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

---

## TC_01.8 - Very Short Recording

### Description
Test recording < 1 second

### Test Steps
1. Click record
2. Immediately click stop (< 1 second)
3. Check transcript

### Expected Result
- ✅ Warning: "Recording too short (minimum 1 second)"
- ✅ No transcription attempted
- ✅ Clear user guidance

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.9 - Silent Recording

### Description
Test recording with no audio/silence

### Test Steps
1. Mute microphone
2. Record for 10 seconds
3. Stop and check transcript

### Expected Result
- ✅ Transcription completes
- ✅ Result: Empty or "[No speech detected]"
- ✅ No crash
- ✅ Suggestion to check microphone

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.10 - Background Noise

### Description
Test recording with heavy background noise

### Test Steps
1. Play loud music/noise
2. Record while speaking
3. Check transcript accuracy

### Expected Result
- ✅ Transcription completes
- ✅ Some words may be incorrect (acceptable)
- ✅ No crash
- ✅ Suggestion to reduce background noise

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.11 - Disk Space Full

### Description
Test recording when disk is full

### Preconditions
- Disk space < 10MB

### Test Steps
1. Record audio
2. Try to save

### Expected Result
- ✅ Error: "Insufficient disk space"
- ✅ No partial file saved
- ✅ Clear instructions to free space

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.12 - Microphone Permission Denied

### Description
Test when user denies microphone permission

### Test Steps
1. Click microphone icon
2. Deny permission in browser prompt

### Expected Result
- ✅ Error: "Microphone permission denied"
- ✅ Instructions to enable permission
- ✅ Link to browser settings

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_01.13 - Multiple Recordings Rapidly

### Description
Test recording multiple times in quick succession

### Test Steps
1. Record 5 times rapidly (each 5 seconds)
2. Save all recordings

### Expected Result
- ✅ All recordings saved with unique IDs
- ✅ No file overwrite
- ✅ All transcripts accurate
- ✅ No memory leak

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC_01.1 | ⏳ | High | Basic recording |
| TC_01.2 | ⏳ | High | Save audio & transcript |
| TC_01.3 | ⏳ | Medium | Cancel recording |
| TC_01.4 | ⏳ | High | Multi-language |
| TC_01.5 | ⏳ | Medium | Missing ffmpeg |
| TC_01.6 | ⏳ | Low | No microphone |
| TC_01.7 | ⏳ | Medium | Long recording (5 min) |
| TC_01.8 | ⏳ | Medium | Very short recording |
| TC_01.9 | ⏳ | Medium | Silent recording |
| TC_01.10 | ⏳ | Low | Background noise |
| TC_01.11 | ⏳ | Low | Disk space full |
| TC_01.12 | ⏳ | High | Permission denied |
| TC_01.13 | ⏳ | Medium | Multiple rapid recordings |

**Legend:** ✅ Pass | ❌ Fail | ⏳ Pending | ⚠️ Blocked

**Total:** 13 test cases
**Critical:** 4 (High priority)
**Important:** 7 (Medium priority)
**Nice-to-have:** 2 (Low priority)
