# TC_04 - Library Tab

## General Information
- **Module:** Library Tab
- **Priority:** Medium
- **Tester:** 
- **Date:** 11/27/2025

---

## TC_04.1 - View Analysis History

### Description
Test displaying analysis history list

### Preconditions
- At least 3 analyses in history

### Test Steps
1. Open "📚 Library" tab
2. Select "📊 Analysis History" sub-tab
3. Click "🔄 Refresh"

### Expected Result
- ✅ Analysis list displayed
- ✅ Format: "YYYY-MM-DD - filename"
- ✅ Sorted by time (newest first)
- ✅ Statistics displayed: "📊 Found X saved analyses"

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.2 - Reload Analysis

### Description
Test reloading previous analysis results

### Preconditions
- Analysis exists in history

### Test Steps
1. Select 1 analysis from dropdown
2. Click "📂 Load to workspace"

### Expected Result
- ✅ Status displays: "✅ Loaded analysis: [filename]"
- ✅ Summary loaded to Upload tab
- ✅ Topics loaded
- ✅ Actions loaded
- ✅ Decisions loaded
- ✅ Can chat with loaded transcript

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.3 - View Recording History

### Description
Test displaying recording list

### Preconditions
- At least 2 recordings exist

### Test Steps
1. Select "🎙️ Recording History" sub-tab
2. Click "🔄 Refresh"

### Expected Result
- ✅ Recording list displayed
- ✅ Format: "ID - Title"
- ✅ Statistics displayed: total, processed, unprocessed, total duration

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.4 - View Recording Details

### Description
Test viewing recording details

### Preconditions
- Recording exists in library

### Test Steps
1. Select 1 recording from dropdown
2. View displayed information

### Expected Result
- ✅ Display: ID, Date, Duration, Status, Notes
- ✅ Audio player displayed
- ✅ Can play audio
- ✅ Notes displayed completely

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.5 - Delete Recording

### Description
Test deleting recording from library

### Preconditions
- Recording exists in library

### Test Steps
1. Select 1 recording
2. Click "🗑️ Delete"
3. Click "🔄 Refresh"

### Expected Result
- ✅ Display: "✅ Deleted [ID]"
- ✅ Recording removed from list
- ✅ Audio file deleted from disk
- ✅ Statistics updated

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.6 - Error Handling - No History

### Description
Test display when no data exists

### Preconditions
- Empty database (or all history deleted)

### Test Steps
1. Open Analysis History tab
2. Click Refresh

### Expected Result
- ✅ Display: "_No history yet_"
- ✅ Empty dropdown
- ✅ No console errors

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.7 - Auto-refresh with New Data

### Description
Test automatic update when new analysis added

### Test Steps
1. Open Library tab
2. Switch to Upload tab
3. Analyze 1 new file
4. Return to Library tab

### Expected Result
- ✅ List auto-updates
- ✅ New analysis appears first
- ✅ No need to click Refresh

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_04.8 - Play Audio from Library

### Description
Test playing saved audio

### Preconditions
- Recording exists in library

### Test Steps
1. Select recording
2. Click play on audio player
3. Test controls: play, pause, seek, volume

### Expected Result
- ✅ Audio plays normally
- ✅ Waveform displayed
- ✅ Can seek, pause, adjust volume
- ✅ Time displayed: current/total

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC_04.1 | ⏳ | High | |
| TC_04.2 | ⏳ | High | |
| TC_04.3 | ⏳ | High | |
| TC_04.4 | ⏳ | Medium | |
| TC_04.5 | ⏳ | Medium | |
| TC_04.6 | ⏳ | Low | |
| TC_04.7 | ⏳ | Medium | |
| TC_04.8 | ⏳ | Medium | |

**Legend:** ✅ Pass | ❌ Fail | ⏳ Pending | ⚠️ Blocked
