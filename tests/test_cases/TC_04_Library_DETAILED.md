# TC_04 - Library Tab (DETAILED)

## Test Environment
- **Browser:** Chrome 120+, Firefox 120+, Safari 17+
- **Screen Resolution:** 1920x1080, 1366x768, Mobile (375x667)
- **Network:** Fast (100Mbps), Slow (3G)
- **Database:** SQLite with sample data

---

## SECTION A: NORMAL CASES (Happy Path)

### TC_04.A1 - View Analysis History List (Normal)

**Objective:** Verify displaying analysis history list

**Preconditions:**
- At least 5 analyses saved in database
- Sample files analyzed:
  - meeting_notes_20251127.txt
  - workshop_transcript_20251126.txt
  - brainstorm_session_20251125.txt
  - team_standup_20251124.txt
  - client_call_20251123.txt

**Test Steps:**
1. Navigate to "📚 Library" tab
2. Select "📊 Analysis History" sub-tab
3. Verify initial display
4. Click "🔄 Refresh" button
5. Check list updates

**Expected Results:**

**UI/UX Validation:**
- ✅ Tab loads in < 2 seconds
- ✅ Sub-tab navigation clear and visible
- ✅ Refresh button prominent and accessible

**List Display:**
- ✅ Analysis list displayed in dropdown
- ✅ Format: "YYYY-MM-DD HH:MM - filename"
- ✅ Examples:
  - "2025-11-27 14:30 - meeting_notes_20251127.txt"
  - "2025-11-26 10:15 - workshop_transcript_20251126.txt"
- ✅ Sorted by date/time (newest first)
- ✅ All 5 analyses visible

**Statistics Display:**
- ✅ Header shows: "📊 Found 5 saved analyses"
- ✅ Count accurate
- ✅ Updates after refresh

**Dropdown Behavior:**
- ✅ Dropdown opens smoothly
- ✅ Scrollable if many items
- ✅ Can select any item
- ✅ Selected item highlighted

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Screenshots:**
- [ ] Initial view
- [ ] Dropdown expanded
- [ ] After refresh

**Notes:**


---

### TC_04.A2 - Load Analysis to Workspace (Normal)

**Objective:** Test reloading previous analysis results

**Preconditions:**
- Analysis exists: "meeting_notes_20251127.txt"
- Analysis contains:
  - Summary: 5 sentences
  - Topics: 3 main topics
  - Action items: 4 items
  - Decisions: 2 decisions

**Test Steps:**
1. Select "2025-11-27 14:30 - meeting_notes_20251127.txt" from dropdown
2. Click "📂 Load to workspace" button
3. Wait for loading
4. Navigate to "📤 Upload & Phân Tích" tab
5. Verify data loaded
6. Navigate to "💬 Chat with AI" tab
7. Ask question about loaded transcript

**Expected Results:**

**Loading Process:**
- ✅ Status shows: "🔄 Loading analysis..."
- ✅ Loading spinner appears
- ✅ Loads in < 3 seconds
- ✅ Success message: "✅ Loaded analysis: meeting_notes_20251127.txt"

**Data Loaded in Upload Tab:**
- ✅ File info displayed:
  - Filename: meeting_notes_20251127.txt
  - Type: Meeting
  - Language: Vietnamese
  - Date: 2025-11-27 14:30
- ✅ Summary section populated (5 sentences)
- ✅ Topics section populated (3 topics with descriptions)
- ✅ Action items section populated (4 items with assignees & deadlines)
- ✅ Decisions section populated (2 decisions)
- ✅ All formatting preserved (bullets, numbering)

**Chat Functionality:**
- ✅ Can ask questions about loaded transcript
- ✅ AI responds with relevant answers
- ✅ Context correctly loaded

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.A3 - View Recording History List (Normal)

**Objective:** Test displaying recording list

**Preconditions:**
- At least 3 recordings exist:
  - rec_001: "Team Meeting" - 5 min - Processed
  - rec_002: "Client Call" - 10 min - Processed
  - rec_003: "Quick Note" - 2 min - Unprocessed

**Test Steps:**
1. Select "🎙️ Recording History" sub-tab
2. Click "🔄 Refresh" button
3. Check list and statistics

**Expected Results:**

**List Display:**
- ✅ Recording list displayed in dropdown
- ✅ Format: "ID - Title"
- ✅ Examples:
  - "rec_001 - Team Meeting"
  - "rec_002 - Client Call"
  - "rec_003 - Quick Note"
- ✅ All 3 recordings visible

**Statistics Display:**
- ✅ Total recordings: 3
- ✅ Processed: 2
- ✅ Unprocessed: 1
- ✅ Total duration: 17 minutes
- ✅ Format: "📊 Total: 3 | ✅ Processed: 2 | ⏳ Unprocessed: 1 | ⏱️ Duration: 17 min"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.A4 - View Recording Details (Normal)

**Objective:** Test viewing detailed recording information

**Preconditions:**
- Recording exists: rec_001 - "Team Meeting"
- Recording details:
  - ID: rec_001
  - Title: Team Meeting
  - Date: 2025-11-27 14:30
  - Duration: 5:23
  - Status: Processed
  - Notes: "Discussed Q4 goals and budget"
  - Audio file: data/recordings/rec_001.wav

**Test Steps:**
1. Select "rec_001 - Team Meeting" from dropdown
2. View displayed information
3. Test audio player

**Expected Results:**

**Details Display:**
- ✅ ID displayed: "rec_001"
- ✅ Title: "Team Meeting"
- ✅ Date: "2025-11-27 14:30"
- ✅ Duration: "5:23"
- ✅ Status badge: "✅ Processed" (green)
- ✅ Notes: "Discussed Q4 goals and budget"
- ✅ All fields clearly labeled

**Audio Player:**
- ✅ Audio player displayed
- ✅ Waveform visualization
- ✅ Play button works
- ✅ Can play audio successfully
- ✅ Seek bar functional
- ✅ Volume control works
- ✅ Time display: "00:00 / 05:23"

**Layout:**
- ✅ Information organized in sections
- ✅ Readable font and spacing
- ✅ Professional appearance

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.A5 - Delete Recording (Normal)

**Objective:** Test deleting recording from library

**Preconditions:**
- Recording exists: rec_003 - "Quick Note"
- Total recordings: 3

**Test Steps:**
1. Select "rec_003 - Quick Note" from dropdown
2. Click "🗑️ Delete" button
3. Confirm deletion (if prompt appears)
4. Wait for deletion
5. Click "🔄 Refresh"
6. Check file system

**Expected Results:**

**Confirmation:**
- ✅ Confirmation dialog: "Are you sure you want to delete this recording?"
- ✅ Warning: "This action cannot be undone"
- ✅ Options: "Delete" (red) and "Cancel"

**Deletion Process:**
- ✅ Status shows: "🔄 Deleting..."
- ✅ Completes in < 2 seconds
- ✅ Success message: "✅ Deleted rec_003 successfully"

**List Update:**
- ✅ Recording removed from dropdown
- ✅ List now shows 2 recordings
- ✅ Statistics updated: "Total: 2"
- ✅ Dropdown auto-clears selection

**File System:**
- ✅ Audio file deleted: data/recordings/rec_003.wav
- ✅ Transcript file deleted: data/transcripts/rec_003.txt
- ✅ Database record removed
- ✅ No orphaned files

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES (Error Handling)

### TC_04.B1 - Empty Analysis History (Error)

**Objective:** Test display when no analyses exist

**Preconditions:**
- Empty database (or all history deleted)
- No analyses saved

**Test Steps:**
1. Navigate to "📊 Analysis History" sub-tab
2. Click "🔄 Refresh"

**Expected Results:**

**Empty State Display:**
- ✅ Message: "📭 No analysis history yet"
- ✅ Subtitle: "Analyze a transcript to see it here"
- ✅ Empty dropdown (or disabled)
- ✅ Statistics: "📊 Found 0 saved analyses"

**UI State:**
- ✅ "Load to workspace" button disabled
- ✅ No errors in console
- ✅ Professional empty state design

**User Guidance:**
- ✅ Suggestion: "Go to 'Upload' or 'Recording' tab to analyze transcripts"
- ✅ Link/button to navigate to Upload tab

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B2 - Empty Recording History (Error)

**Objective:** Test display when no recordings exist

**Preconditions:**
- No recordings in database

**Test Steps:**
1. Navigate to "🎙️ Recording History" sub-tab
2. Click "🔄 Refresh"

**Expected Results:**

**Empty State:**
- ✅ Message: "📭 No recordings yet"
- ✅ Subtitle: "Record audio to see it here"
- ✅ Empty dropdown
- ✅ Statistics: "📊 Total: 0 | ✅ Processed: 0 | ⏳ Unprocessed: 0"

**UI State:**
- ✅ Delete button disabled
- ✅ Audio player hidden
- ✅ No errors

**User Guidance:**
- ✅ Link to Recording tab

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B3 - Load Corrupted Analysis (Error)

**Objective:** Test loading analysis with corrupted data

**Preconditions:**
- Analysis exists but data corrupted in database

**Test Steps:**
1. Select corrupted analysis
2. Click "Load to workspace"

**Expected Results:**

**Error Handling:**
- ✅ Error message: "❌ Failed to load analysis"
- ✅ Details: "The analysis data appears to be corrupted"
- ✅ Suggestion: "Try loading a different analysis"

**No Crash:**
- ✅ Application remains functional
- ✅ Can select other analyses
- ✅ Error logged for debugging

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B4 - Delete Non-existent Recording (Error)

**Objective:** Test deleting recording that doesn't exist

**Preconditions:**
- Recording in list but files deleted manually

**Test Steps:**
1. Select recording
2. Click Delete

**Expected Results:**

**Error Handling:**
- ✅ Error: "❌ Recording not found"
- ✅ Message: "The recording files may have been deleted"
- ✅ Suggestion: "Refresh the list"

**Auto-cleanup:**
- ✅ Recording removed from list
- ✅ Database cleaned up
- ✅ Statistics updated

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B5 - Audio File Missing (Error)

**Objective:** Test viewing recording when audio file missing

**Preconditions:**
- Recording exists in database
- Audio file deleted from disk

**Test Steps:**
1. Select recording
2. Try to play audio

**Expected Results:**

**Error Display:**
- ✅ Warning: "⚠️ Audio file not found"
- ✅ Message: "The audio file may have been moved or deleted"
- ✅ Audio player shows error state

**Recording Info:**
- ✅ Other details still displayed (ID, title, date, notes)
- ✅ Status shows: "⚠️ File missing"

**Options:**
- ✅ Option to delete recording from database
- ✅ Option to refresh list

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B6 - Database Connection Error (Error)

**Objective:** Test handling when database unavailable

**Test Steps:**
1. (Simulate database connection error)
2. Try to refresh list

**Expected Results:**

**Error Display:**
- ✅ Error: "❌ Database connection error"
- ✅ Message: "Unable to load library data"
- ✅ Retry button available

**User Guidance:**
- ✅ Troubleshooting tips
- ✅ Check database file exists
- ✅ Restart application

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_04.C1 - Sub-tab Navigation

**Objective:** Validate sub-tab switching

**Test Steps:**
1. Click "📊 Analysis History" sub-tab
2. Click "🎙️ Recording History" sub-tab
3. Switch back and forth multiple times

**Expected Results:**

**Tab Behavior:**
- ✅ Smooth transition (no flicker)
- ✅ Active tab highlighted
- ✅ Content loads immediately
- ✅ Previous selections cleared

**Visual Design:**
- ✅ Active tab: Bold text, underline, or colored background
- ✅ Inactive tab: Normal text, gray
- ✅ Hover effect on inactive tabs
- ✅ Clear visual distinction

**Performance:**
- ✅ Switching instant (< 0.5s)
- ✅ No lag
- ✅ Data persists (no unnecessary reloads)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C2 - Dropdown Styling

**Objective:** Validate dropdown appearance and behavior

**Test Steps:**
1. Click dropdown
2. Hover over items
3. Select item

**Expected Results:**

**Dropdown Design:**
- ✅ Border: 1px solid gray
- ✅ Rounded corners
- ✅ Padding: 8px 12px
- ✅ Font size: 14px
- ✅ Max height: 300px (scrollable)

**Item Styling:**
- ✅ Hover: Light background (#f3f4f6)
- ✅ Selected: Blue background (#dbeafe)
- ✅ Proper spacing between items (4px)

**Icons:**
- ✅ Dropdown arrow icon
- ✅ Rotates when open
- ✅ Smooth animation

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C3 - Refresh Button

**Objective:** Validate refresh button behavior

**Test Steps:**
1. Click refresh button
2. Check animation and feedback

**Expected Results:**

**Button Design:**
- ✅ Icon: 🔄 or circular arrow
- ✅ Tooltip: "Refresh list"
- ✅ Positioned prominently

**Click Feedback:**
- ✅ Rotation animation on click
- ✅ Button disabled during refresh
- ✅ Loading indicator (optional)
- ✅ Re-enables after refresh

**Functionality:**
- ✅ List updates with latest data
- ✅ Statistics recalculated
- ✅ Completes in < 2 seconds

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C4 - Delete Button States

**Objective:** Validate delete button appearance

**Test Steps:**
1. Check button when no selection
2. Check after selection
3. Check during deletion

**Expected Results:**

**No Selection:**
- ✅ Button disabled
- ✅ Gray background
- ✅ Cursor: not-allowed

**With Selection:**
- ✅ Button enabled
- ✅ Red background (#ef4444)
- ✅ Icon: 🗑️
- ✅ Cursor: pointer

**Hover:**
- ✅ Darker red
- ✅ Lift effect

**During Deletion:**
- ✅ Button disabled
- ✅ Loading spinner
- ✅ Text: "Deleting..."

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C5 - Statistics Display

**Objective:** Validate statistics formatting

**Test Steps:**
1. Check statistics for both sub-tabs
2. Verify accuracy

**Expected Results:**

**Analysis History Stats:**
- ✅ Format: "📊 Found X saved analyses"
- ✅ Icon: 📊
- ✅ Color: Blue or neutral
- ✅ Font size: 14-16px

**Recording History Stats:**
- ✅ Format: "📊 Total: X | ✅ Processed: Y | ⏳ Unprocessed: Z | ⏱️ Duration: N min"
- ✅ Icons for each metric
- ✅ Color-coded: Green for processed, orange for unprocessed
- ✅ Separator: | or •

**Accuracy:**
- ✅ Counts match actual data
- ✅ Duration calculated correctly
- ✅ Updates after changes

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C6 - Audio Player in Library

**Objective:** Validate audio player functionality

**Test Steps:**
1. Select recording
2. Test all player controls

**Expected Results:**

**Player Components:**
- ✅ Play/Pause button
- ✅ Seek bar with progress
- ✅ Volume slider
- ✅ Time display (current/total)
- ✅ Waveform visualization (optional)

**Functionality:**
- ✅ Play starts audio
- ✅ Pause stops audio
- ✅ Seek bar updates in real-time
- ✅ Can click seek bar to jump
- ✅ Volume control works (0-100%)
- ✅ Time display accurate

**Design:**
- ✅ Compact layout
- ✅ Clear controls
- ✅ Responsive

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C7 - Recording Details Layout

**Objective:** Validate recording details display

**Test Steps:**
1. Select recording
2. Check information layout

**Expected Results:**

**Layout:**
- ✅ Information in card or panel
- ✅ Sections clearly separated
- ✅ Labels bold, values normal
- ✅ Proper spacing

**Fields:**
- ✅ ID: Monospace font
- ✅ Title: Larger font, bold
- ✅ Date: Format "YYYY-MM-DD HH:MM"
- ✅ Duration: Format "MM:SS"
- ✅ Status: Badge with color (green/orange/red)
- ✅ Notes: Multi-line, scrollable if long

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C8 - Responsive Design

**Objective:** Validate library on different screens

**Test Steps:**
1. Test on desktop (1920x1080)
2. Test on tablet (768x1024)
3. Test on mobile (375x667)

**Expected Results:**

**Desktop:**
- ✅ Full layout with all elements
- ✅ Comfortable spacing
- ✅ Dropdowns full width

**Tablet:**
- ✅ Layout adapts
- ✅ Buttons may stack
- ✅ Still usable

**Mobile:**
- ✅ Single column layout
- ✅ Dropdowns full width
- ✅ Buttons full width
- ✅ Touch-friendly sizes (44px min)
- ✅ No horizontal scroll

**Actual Result:**
- [ ] Pass (Desktop)
- [ ] Pass (Tablet)
- [ ] Pass (Mobile)
- [ ] Fail

**Notes:**


---

## SECTION D: PERFORMANCE & DATA INTEGRITY

### TC_04.D1 - Large History List (100+ Items)

**Objective:** Test performance with many analyses

**Preconditions:**
- 100+ analyses in database

**Test Steps:**
1. Open Analysis History
2. Click Refresh
3. Scroll through dropdown
4. Select item

**Expected Results:**

**Performance:**
- ✅ List loads in < 3 seconds
- ✅ Dropdown scrollable
- ✅ Smooth scrolling
- ✅ No lag when selecting

**UI:**
- ✅ Virtual scrolling (if implemented)
- ✅ Search/filter option (optional)
- ✅ Pagination (optional)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.D2 - Concurrent Access

**Objective:** Test multiple operations simultaneously

**Test Steps:**
1. Load analysis in one tab
2. Delete recording in another tab
3. Refresh both

**Expected Results:**

**Data Consistency:**
- ✅ No conflicts
- ✅ Both operations complete
- ✅ Data synchronized

**No Errors:**
- ✅ No database locks
- ✅ No data corruption

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 5 | 0 | 0 | 0 |
| Abnormal Cases | 6 | 0 | 0 | 0 |
| UI/UX Validation | 8 | 0 | 0 | 0 |
| Performance | 2 | 0 | 0 | 0 |
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

