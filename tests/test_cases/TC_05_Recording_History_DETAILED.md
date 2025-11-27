# TC_05 - Recording History Tab (DETAILED)

## SECTION A: NORMAL CASES

### TC_05.A1 - View Recordings List
**Steps:** Open tab → Refresh → Check list
**Expected:** List displays, statistics shown, sorted by date
**Actual:** [ ] Pass [ ] Fail

### TC_05.A2 - Play Recording
**Steps:** Select recording → Click play
**Expected:** Audio plays, waveform shows, controls work
**Actual:** [ ] Pass [ ] Fail

### TC_05.A3 - Delete Recording
**Steps:** Select → Delete → Confirm
**Expected:** File deleted, list updated, success message
**Actual:** [ ] Pass [ ] Fail

---

## SECTION B: ABNORMAL CASES

### TC_05.B1 - Empty Recordings
**Steps:** No recordings → Refresh
**Expected:** "📊 Chưa có ghi âm nào", empty dropdown
**Actual:** [ ] Pass [ ] Fail

### TC_05.B2 - Corrupted Audio File
**Steps:** Corrupt WAV file → Try to play
**Expected:** Error: "Cannot play audio", no crash
**Actual:** [ ] Pass [ ] Fail

### TC_05.B3 - Missing Audio File
**Steps:** Delete file from disk → Try to play
**Expected:** Error: "File not found", option to remove from list
**Actual:** [ ] Pass [ ] Fail

### TC_05.B4 - Delete While Playing
**Steps:** Play audio → Delete while playing
**Expected:** Playback stops, file deleted, no error
**Actual:** [ ] Pass [ ] Fail

---

## SECTION C: UI/UX VALIDATION

### TC_05.C1 - Audio Player Controls
**Expected:** Play/Pause, Seek, Volume, Speed controls work
**Actual:** [ ] Pass [ ] Fail

### TC_05.C2 - Statistics Display
**Expected:** Total, Processed, Unprocessed, Duration accurate
**Actual:** [ ] Pass [ ] Fail

---

**Total:** 9 test cases
