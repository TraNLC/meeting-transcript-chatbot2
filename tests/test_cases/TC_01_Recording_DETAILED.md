# TC_01 - Recording Tab (DETAILED)

## Test Environment
- **Browser:** Chrome 120+, Firefox 120+, Safari 17+
- **Screen Resolution:** 1920x1080, 1366x768, Mobile (375x667)
- **Network:** Fast (100Mbps), Slow (3G), Offline
- **Hardware:** Microphone required, ffmpeg installed

---

## SECTION A: NORMAL CASES (Happy Path)

### TC_01.A1 - Basic Recording (Normal)

**Objective:** Verify basic recording and automatic transcription workflow

**Preconditions:**
- Application running at http://localhost:7777
- ffmpeg installed and in PATH
- Microphone connected and working
- Browser microphone permission granted

**Test Steps:**
1. Navigate to "🎙️ Recording" tab
2. Verify initial state (no recording active)
3. Select language: "🇻🇳 Tiếng Việt" from dropdown
4. Click microphone icon button
5. Wait for recording to start (red indicator)
6. Speak clearly: "Xin chào, đây là bài test ghi âm số một"
7. Wait 5 seconds
8. Click "⏹️ Stop" button
9. Wait for auto-transcription

**Expected Results:**

**UI/UX Validation:**
- ✅ Microphone button changes to red when recording
- ✅ Waveform animation displays during recording
- ✅ Timer shows recording duration: "00:05"
- ✅ Stop button is enabled and visible
- ✅ Recording indicator pulses (red dot animation)

**Transcription Process:**
- ✅ Status shows: "🔄 Đang xử lý âm thanh..."
- ✅ Loading spinner appears
- ✅ Processing completes in 5-15 seconds
- ✅ Status changes to: "✅ Transcription hoàn tất!"

**Results Display:**
- ✅ Transcript section populated with:
  - Header: "📝 **Transcript (vi):**"
  - Timestamp: "[2025-11-27 14:30:45]"
  - Content: "Xin chào, đây là bài test ghi âm số một"
- ✅ Audio player appears with waveform
- ✅ Can play back recorded audio
- ✅ Transcript accuracy ≥ 90%

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Screenshots:**
- [ ] Before recording
- [ ] During recording (waveform)
- [ ] After transcription

**Notes:**


---

### TC_01.A2 - Save Audio and Transcript (Normal)

**Objective:** Verify saving functionality to library

**Preconditions:**
- Completed TC_01.A1
- Transcript displayed successfully

**Test Steps:**
1. Verify "💾 Save Audio & Transcript" button is enabled
2. Enter title in textbox: "Test Recording 01 - Vietnamese"
3. Click "💾 Save Audio & Transcript" button
4. Wait for save operation
5. Check status message
6. Navigate to "📚 Library > 🎙️ Recording History" tab
7. Click "🔄 Refresh" button
8. Verify recording appears in list

**Expected Results:**

**Save Operation:**
- ✅ Status shows: "✅ Audio and transcript saved successfully!"
- ✅ Display recording ID: "ID: rec_20251127_143045"
- ✅ Display file paths:
  - Audio: `data/recordings/rec_20251127_143045.wav`
  - Transcript: `data/transcripts/rec_20251127_143045.txt`
- ✅ Save completes in < 2 seconds

**File System Validation:**
- ✅ Audio file exists at specified path
- ✅ Audio file size > 0 bytes (typically 500KB - 5MB)
- ✅ Transcript file exists at specified path
- ✅ Transcript file contains correct content
- ✅ Files have correct permissions (readable)

**Library Display:**
- ✅ Recording appears in dropdown list
- ✅ Format: "rec_20251127_143045 - Test Recording 01 - Vietnamese"
- ✅ Statistics updated: "Total: X recordings"
- ✅ Can select and view recording details

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.A3 - Multi-language Recording (Normal)

**Objective:** Test transcription accuracy across different languages

**Preconditions:**
- Application running
- Microphone working

**Test Data:**

| Language | Test Content | Expected Transcript | Min Accuracy |
|----------|--------------|---------------------|--------------|
| 🇻🇳 Tiếng Việt | "Xin chào Việt Nam, hôm nay là một ngày đẹp trời" | Xin chào Việt Nam, hôm nay là một ngày đẹp trời | 90% |
| 🇬🇧 English | "Hello World, this is a test recording for English language" | Hello World, this is a test recording for English language | 95% |
| 🇯🇵 日本語 | "こんにちは、これはテストです" | こんにちは、これはテストです | 85% |
| 🇰🇷 한국어 | "안녕하세요, 이것은 테스트입니다" | 안녕하세요, 이것은 테스트입니다 | 85% |
| 🇨🇳 中文 | "你好世界，这是一个测试录音" | 你好世界，这是一个测试录音 | 85% |

**Test Steps (for each language):**
1. Select language from dropdown
2. Click record
3. Speak test content clearly
4. Stop recording
5. Wait for transcription
6. Compare result with expected

**Expected Results:**

**For Each Language:**
- ✅ Transcription completes successfully
- ✅ Accuracy meets minimum threshold
- ✅ No encoding errors (no "?" or "□" characters)
- ✅ Special characters display correctly:
  - Vietnamese: àáảãạ êếễệ ôốổỗộ
  - Japanese: Hiragana, Katakana, Kanji
  - Korean: Hangul
  - Chinese: Simplified characters
- ✅ Proper spacing and punctuation

**UI Display:**
- ✅ Language flag displayed correctly
- ✅ Transcript header shows correct language code
- ✅ Font renders characters properly

**Actual Result:**
- [ ] Pass (vi)
- [ ] Pass (en)
- [ ] Pass (ja)
- [ ] Pass (ko)
- [ ] Pass (zh)
- [ ] Fail

**Notes:**


---

### TC_01.A4 - Long Recording (5 Minutes)

**Objective:** Test performance with extended recording duration

**Preconditions:**
- Application running
- Sufficient disk space (> 100MB)

**Test Steps:**
1. Select language: English
2. Start recording
3. Speak continuously or play audio for 5 minutes
4. Monitor recording indicator
5. Stop recording
6. Wait for transcription
7. Measure processing time

**Expected Results:**

**Recording Phase:**
- ✅ Recording continues uninterrupted for full 5 minutes
- ✅ Timer displays correctly: "05:00"
- ✅ Waveform animation smooth (no lag)
- ✅ No memory leaks (check browser task manager)
- ✅ Audio file size: ~50MB (for WAV format)

**Transcription Phase:**
- ✅ Processing starts immediately after stop
- ✅ Status shows: "🔄 Processing long audio..."
- ✅ Progress indicator (if available)
- ✅ Transcription completes in < 2 minutes
- ✅ No timeout errors

**Results:**
- ✅ Complete transcript (not truncated)
- ✅ Transcript length: ~750-1000 words (for continuous speech)
- ✅ Audio playback works correctly
- ✅ Can save to library successfully

**Performance:**
- ✅ CPU usage returns to normal after processing
- ✅ Memory usage < 2GB
- ✅ Browser remains responsive

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES (Error Handling)

### TC_01.B1 - Very Short Recording (< 1 Second)

**Objective:** Verify validation for extremely short recordings

**Test Steps:**
1. Click record button
2. Immediately click stop (< 1 second)
3. Check system response

**Expected Results:**

**Error Display:**
- ✅ Status shows: "⚠️ Recording too short (minimum 1 second required)"
- ✅ Warning color: Orange (#f59e0b)
- ✅ Icon: ⚠️
- ✅ Error appears immediately (< 0.5s)

**UI Feedback:**
- ✅ No transcription attempted
- ✅ Audio player not displayed
- ✅ Transcript section remains empty
- ✅ Can record again immediately

**User Guidance:**
- ✅ Message: "Please record for at least 1 second for meaningful transcription"
- ✅ Suggestion: "Try recording again with longer audio"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B2 - Silent Recording (No Audio Input)

**Objective:** Test handling of recording with no speech detected

**Preconditions:**
- Microphone muted or no audio input

**Test Steps:**
1. Mute microphone or ensure silent environment
2. Start recording
3. Wait 10 seconds (no speech)
4. Stop recording
5. Wait for transcription

**Expected Results:**

**Processing:**
- ✅ Recording completes normally
- ✅ Audio file created (silent WAV file)
- ✅ Transcription process runs

**Results Display:**
- ✅ Status shows: "⚠️ No speech detected in recording"
- ✅ Transcript shows: "[No speech detected]" or empty
- ✅ Warning message: "Please check your microphone:"
  - Ensure microphone is not muted
  - Check microphone permissions
  - Try speaking louder
- ✅ Audio player shows flat waveform (no peaks)

**No Crash:**
- ✅ Application remains functional
- ✅ Can record again immediately
- ✅ No console errors

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B3 - Recording with Heavy Background Noise

**Objective:** Test transcription quality with noise interference

**Preconditions:**
- Play loud background music or noise

**Test Steps:**
1. Start playing loud music/noise
2. Start recording
3. Speak test phrase while noise playing
4. Stop recording
5. Check transcript accuracy

**Expected Results:**

**Transcription:**
- ✅ Transcription completes (no crash)
- ✅ Some words may be incorrect (acceptable)
- ✅ Accuracy may be lower (60-80%)
- ✅ Warning displayed: "⚠️ Background noise detected"

**User Guidance:**
- ✅ Suggestion: "For better accuracy:"
  - Record in quiet environment
  - Reduce background noise
  - Speak closer to microphone
- ✅ Option to re-record

**Quality Indicator:**
- ✅ Audio quality score displayed (if available)
- ✅ Visual indicator of noise level

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B4 - Missing ffmpeg

**Objective:** Verify error handling when ffmpeg not installed

**Preconditions:**
- ffmpeg not installed or not in PATH
- (Temporarily rename ffmpeg.exe for testing)

**Test Steps:**
1. Start recording
2. Speak for 5 seconds
3. Stop recording
4. Wait for transcription attempt

**Expected Results:**

**Error Display:**
- ✅ Status shows: "❌ ffmpeg not found"
- ✅ Red error message with icon
- ✅ Detailed error: "Audio processing requires ffmpeg"

**Installation Instructions:**
- ✅ Clear instructions provided:
  - "Please install ffmpeg to enable audio processing"
  - Download link: https://ffmpeg.org/download.html
  - Installation guide link
- ✅ Platform-specific instructions (Windows/Mac/Linux)

**UI State:**
- ✅ Recording button disabled (or warning shown)
- ✅ Helpful error message (not technical jargon)
- ✅ Link to documentation

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B5 - No Microphone Permission

**Objective:** Test handling when microphone permission denied

**Test Steps:**
1. Deny microphone permission in browser
2. Click record button
3. Check error handling

**Expected Results:**

**Permission Request:**
- ✅ Browser permission prompt appears
- ✅ If denied, error message shows immediately

**Error Display:**
- ✅ Status: "❌ Microphone permission denied"
- ✅ User-friendly message: "This app needs microphone access to record audio"

**Instructions:**
- ✅ How to enable permission:
  - Chrome: Click lock icon → Site settings → Microphone → Allow
  - Firefox: Click shield icon → Permissions → Microphone → Allow
  - Safari: Safari → Settings → Websites → Microphone → Allow
- ✅ Visual guide (screenshot or icon)
- ✅ "Retry" button to request permission again

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B6 - No Microphone Connected

**Objective:** Test handling when no microphone device available

**Preconditions:**
- Disconnect all microphones
- Or disable microphone in system settings

**Test Steps:**
1. Click record button
2. Check system response

**Expected Results:**

**Error Display:**
- ✅ Status: "❌ No microphone detected"
- ✅ Message: "Please connect a microphone to record audio"

**Troubleshooting:**
- ✅ Suggestions:
  - Connect a microphone or headset
  - Check system audio settings
  - Restart browser after connecting microphone
- ✅ Link to system audio settings (if possible)

**UI State:**
- ✅ Record button disabled or shows warning
- ✅ Clear visual indicator (microphone icon with X)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B7 - Disk Space Full

**Objective:** Test recording when disk space insufficient

**Preconditions:**
- Disk space < 10MB (simulate by filling disk)

**Test Steps:**
1. Start recording
2. Record for 30 seconds
3. Try to save recording

**Expected Results:**

**Error Handling:**
- ✅ Error during save: "❌ Insufficient disk space"
- ✅ Detailed message: "Unable to save recording. Please free up disk space."
- ✅ Current available space shown: "Available: 5MB | Required: ~10MB"

**No Partial Files:**
- ✅ No corrupted files created
- ✅ Temporary files cleaned up
- ✅ No orphaned data

**User Guidance:**
- ✅ Suggestions:
  - Delete old recordings
  - Free up disk space
  - Save to different location (if supported)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B8 - Multiple Rapid Recordings

**Objective:** Test recording multiple times in quick succession

**Test Steps:**
1. Record 5 times rapidly (each 5 seconds)
2. Save all recordings with different titles
3. Verify all saved correctly

**Expected Results:**

**Recording Process:**
- ✅ Each recording completes successfully
- ✅ No interference between recordings
- ✅ Each gets unique ID with timestamp

**File Management:**
- ✅ All 5 audio files created with unique names:
  - rec_20251127_143001.wav
  - rec_20251127_143010.wav
  - rec_20251127_143019.wav
  - rec_20251127_143028.wav
  - rec_20251127_143037.wav
- ✅ No file overwrite
- ✅ All transcripts accurate
- ✅ All appear in library

**Performance:**
- ✅ No memory leaks
- ✅ No performance degradation
- ✅ Each transcription completes normally

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B9 - Cancel Recording

**Objective:** Test cancel and clear functionality

**Preconditions:**
- Recording completed but not saved

**Test Steps:**
1. Complete a recording
2. Verify transcript displayed
3. Click "🗑️ Cancel" or "Clear" button
4. Confirm cancellation (if prompt appears)

**Expected Results:**

**Clear Operation:**
- ✅ Audio player cleared/removed
- ✅ Transcript section cleared
- ✅ Status message cleared
- ✅ Title input cleared
- ✅ Recording state reset

**UI State:**
- ✅ Can record new audio immediately
- ✅ No residual data displayed
- ✅ All buttons in default state

**File System:**
- ✅ Temporary files cleaned up (if any)
- ✅ No orphaned audio files

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.B10 - Browser Crash During Recording

**Objective:** Test recovery after unexpected browser crash

**Test Steps:**
1. Start recording
2. Force close browser (Task Manager or Force Quit)
3. Restart browser and application
4. Check for recovery or cleanup

**Expected Results:**

**Recovery:**
- ✅ Application starts normally
- ✅ No corrupted state
- ✅ No error messages on startup

**File Cleanup:**
- ✅ Temporary recording files cleaned up
- ✅ No partial/corrupted files in recordings folder
- ✅ Database consistent

**User Experience:**
- ✅ Can start new recording immediately
- ✅ No data loss for previously saved recordings
- ✅ No need for manual cleanup

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_01.C1 - Language Dropdown

**Objective:** Validate language selection dropdown functionality

**Test Steps:**
1. Click "Language" dropdown
2. Hover over each option
3. Select each language
4. Check keyboard navigation

**Expected Results:**

**Dropdown Behavior:**
- ✅ Opens smoothly (no lag)
- ✅ Shows all 8 languages:
  1. 🇻🇳 Tiếng Việt (vi)
  2. 🇬🇧 English (en)
  3. 🇯🇵 日本語 (ja)
  4. 🇰🇷 한국어 (ko)
  5. 🇨🇳 中文 (zh-CN)
  6. 🇪🇸 Español (es)
  7. 🇫🇷 Français (fr)
  8. 🇩🇪 Deutsch (de)
- ✅ Flags displayed correctly
- ✅ Native language names shown

**Interaction:**
- ✅ Hover effect: Light background color
- ✅ Selected option highlighted
- ✅ Click selects and closes dropdown
- ✅ Can change selection multiple times

**Keyboard Navigation:**
- ✅ Tab key focuses dropdown
- ✅ Arrow keys navigate options
- ✅ Enter key selects
- ✅ Escape key closes

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C2 - Record Button States

**Objective:** Validate record button visual states and feedback

**Test Steps:**
1. Check button in different states
2. Test hover effects
3. Test click feedback

**Expected Results:**

**Default State (Not Recording):**
- ✅ Microphone icon: 🎙️
- ✅ Background: Blue or primary color
- ✅ Text: "Start Recording" or icon only
- ✅ Cursor: pointer
- ✅ Enabled and clickable

**Hover State:**
- ✅ Slightly darker background
- ✅ Lift effect (translateY(-2px))
- ✅ Shadow appears
- ✅ Smooth transition (0.3s)

**Recording State:**
- ✅ Background: Red (#ef4444)
- ✅ Pulsing animation (heartbeat effect)
- ✅ Icon changes or indicator added
- ✅ Text: "Recording..." (if shown)

**Disabled State:**
- ✅ Gray background (#9ca3af)
- ✅ Cursor: not-allowed
- ✅ No hover effect
- ✅ Opacity: 0.5

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C3 - Waveform Visualization

**Objective:** Validate audio waveform display during recording

**Test Steps:**
1. Start recording
2. Speak at different volumes
3. Observe waveform animation
4. Test with silence

**Expected Results:**

**Visual Display:**
- ✅ Waveform appears immediately when recording starts
- ✅ Bars animate in real-time
- ✅ Height corresponds to audio volume:
  - Loud speech: Tall bars
  - Quiet speech: Short bars
  - Silence: Minimal/flat bars
- ✅ Smooth animation (60fps)
- ✅ Color: Green or blue gradient

**Performance:**
- ✅ No lag or stuttering
- ✅ Responsive to audio input
- ✅ Clears when recording stops

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C4 - Timer Display

**Objective:** Validate recording timer accuracy and display

**Test Steps:**
1. Start recording
2. Monitor timer for 60 seconds
3. Check format and accuracy

**Expected Results:**

**Display Format:**
- ✅ Format: "MM:SS" (e.g., "00:05", "01:30")
- ✅ Updates every second
- ✅ Accurate timing (±1 second tolerance)
- ✅ Visible and readable

**Visual Design:**
- ✅ Clear font (monospace recommended)
- ✅ Sufficient size (16px+)
- ✅ High contrast with background
- ✅ Positioned prominently

**Behavior:**
- ✅ Starts at "00:00"
- ✅ Counts up continuously
- ✅ Stops when recording stops
- ✅ Resets for new recording

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C5 - Audio Player Controls

**Objective:** Validate audio playback controls after recording

**Test Steps:**
1. Complete a recording
2. Test all player controls
3. Check responsiveness

**Expected Results:**

**Player Components:**
- ✅ Play/Pause button
- ✅ Seek bar (progress slider)
- ✅ Volume control
- ✅ Time display (current/total)
- ✅ Waveform visualization

**Play/Pause:**
- ✅ Click play starts playback
- ✅ Icon changes to pause
- ✅ Click pause stops playback
- ✅ Smooth toggle

**Seek Bar:**
- ✅ Shows playback progress
- ✅ Can click to jump to position
- ✅ Can drag to scrub
- ✅ Smooth seeking

**Volume Control:**
- ✅ Slider adjusts volume (0-100%)
- ✅ Mute button works
- ✅ Volume persists across recordings

**Time Display:**
- ✅ Shows: "00:05 / 00:30"
- ✅ Updates in real-time
- ✅ Accurate timing

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C6 - Save Button States

**Objective:** Validate save button behavior and states

**Test Steps:**
1. Check button before recording
2. Check after recording
3. Check during save operation

**Expected Results:**

**Before Recording:**
- ✅ Button disabled
- ✅ Gray background
- ✅ Cursor: not-allowed
- ✅ Tooltip: "Record audio first"

**After Recording (No Title):**
- ✅ Button enabled
- ✅ Green background
- ✅ Cursor: pointer
- ✅ Can click to save

**During Save:**
- ✅ Button disabled
- ✅ Loading spinner
- ✅ Text: "Saving..."
- ✅ Cannot click again

**After Save:**
- ✅ Button re-enabled
- ✅ Success feedback (checkmark animation)
- ✅ Can save another recording

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_01.C7 - Status Messages

**Objective:** Validate status message display and styling

**Test Steps:**
1. Trigger different status messages
2. Check styling and timing

**Expected Results:**

**Success Messages:**
- ✅ Green background (#d1fae5)
- ✅ Green text (#10b981)
- ✅ Checkmark icon: ✅
- ✅ Example: "✅ Recording saved successfully!"

**Error Messages:**
- ✅ Red background (#fee2e2)
- ✅ Red text (#ef4444)
- ✅ Error icon: ❌
- ✅ Example: "❌ Microphone permission denied"

**Warning Messages:**
- ✅ Orange background (#fef3c7)
- ✅ Orange text (#f59e0b)
- ✅ Warning icon: ⚠️
- ✅ Example: "⚠️ Recording too short"

**Info Messages:**
- ✅ Blue background (#dbeafe)
- ✅ Blue text (#3b82f6)
- ✅ Info icon: ℹ️
- ✅ Example: "ℹ️ Processing audio..."

**Behavior:**
- ✅ Messages appear smoothly (fade in)
- ✅ Auto-dismiss after 5 seconds (for non-critical)
- ✅ Can manually dismiss (X button)
- ✅ Multiple messages stack vertically

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION D: SAMPLE DATA & TEST FILES

### Audio Test Samples

Create these test scenarios:

1. **Normal Speech:**
   - Clear voice, no background noise
   - Duration: 10-30 seconds
   - Languages: vi, en, ja, ko, zh

2. **Long Recording:**
   - Continuous speech or audio
   - Duration: 5 minutes
   - File size: ~50MB

3. **Short Recording:**
   - Very brief audio
   - Duration: < 1 second

4. **Silent Recording:**
   - No speech, just silence
   - Duration: 10 seconds

5. **Noisy Recording:**
   - Speech with loud background music
   - Duration: 15 seconds

6. **Multiple Languages:**
   - Code-switching between languages
   - Duration: 20 seconds

---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 4 | 0 | 0 | 0 |
| Abnormal Cases | 10 | 0 | 0 | 0 |
| UI/UX Validation | 7 | 0 | 0 | 0 |
| **TOTAL** | **21** | **0** | **0** | **0** |

**Success Rate:** 0% (Not tested yet)

---

## Notes & Observations

**Issues Found:**
1. 
2. 
3. 

**Improvements Needed:**
1. 
2. 
3. 

**Tested By:** _______________
**Date:** _______________
**Environment:** _______________
**Browser:** _______________
**Microphone:** _______________

