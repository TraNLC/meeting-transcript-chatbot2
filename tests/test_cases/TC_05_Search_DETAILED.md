# TC_05 - Smart Search Tab (DETAILED)

## Test Environment
- **Browser:** Chrome 120+, Firefox 120+, Safari 17+
- **Screen Resolution:** 1920x1080, 1366x768, Mobile (375x667)
- **Network:** Fast (100Mbps), Slow (3G)
- **Database:** ChromaDB with sample embeddings

---

## SECTION A: NORMAL CASES (Happy Path)

### TC_05.A1 - Basic Semantic Search (Normal)

**Objective:** Verify semantic search with ChromaDB

**Preconditions:**
- ChromaDB has 10+ meetings indexed
- Sample meetings include:
  - "React Hooks training workshop"
  - "Budget planning for Q4"
  - "Team brainstorming session"
  - "Client project kickoff"

**Test Steps:**
1. Navigate to "🔍 Smart Search" tab
2. Select "📊 Search Analysis" sub-tab
3. Enter query: "React Hooks training"
4. Click "🔍 Search" button
5. Wait for results

**Expected Results:**

**UI/UX Validation:**
- ✅ Search input box clear and prominent
- ✅ Search button enabled
- ✅ Loading indicator during search

**Search Process:**
- ✅ Status shows: "🔄 Searching..."
- ✅ Search completes in < 3 seconds
- ✅ Success message: "✅ Found X matching meetings"

**Results Display:**
- ✅ Results related to React Hooks displayed first
- ✅ Each result shows:
  - Meeting ID
  - Meeting type (workshop/meeting/brainstorm)
  - Language
  - Date
  - Similarity score (e.g., "95% match")
  - Transcript preview (first 200 chars)
- ✅ Results sorted by similarity (highest first)
- ✅ Minimum 1 relevant result

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Screenshots:**
- [ ] Search interface
- [ ] Results display

**Notes:**


---

### TC_05.A2 - Filter by Meeting Type (Normal)

**Objective:** Test filtering results by meeting type

**Test Steps:**
1. Enter query: "team discussion"
2. Select filter "Meeting Type": "workshop"
3. Click "🔍 Search"
4. Check results

**Expected Results:**

**Filter UI:**
- ✅ Dropdown shows options:
  - All types
  - Meeting
  - Workshop
  - Brainstorming
- ✅ Selected filter highlighted

**Results:**
- ✅ Only "workshop" type meetings displayed
- ✅ Results still relevant to query
- ✅ Result count may be lower than unfiltered
- ✅ Message: "Filtered by: Workshop"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.A3 - Filter by Language (Normal)

**Objective:** Test filtering by language

**Test Steps:**
1. Enter query: "budget planning"
2. Select filter "Language": "en" (English)
3. Click Search

**Expected Results:**

**Filter UI:**
- ✅ Language dropdown shows:
  - All languages
  - vi, en, ja, ko, zh, es, fr, de
- ✅ Flags displayed

**Results:**
- ✅ Only English meetings displayed
- ✅ Language field shows "en" for all results
- ✅ Results accurate

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---


### TC_05.A4 - Adjust Result Count (Normal)

**Objective:** Test result count slider

**Test Steps:**
1. Enter query: "project update"
2. Set slider "Number of results" = 3
3. Click Search
4. Note result count
5. Set slider = 10
6. Search again

**Expected Results:**

**Slider UI:**
- ✅ Slider range: 1-20
- ✅ Current value displayed: "Results: 3"
- ✅ Smooth sliding

**Results:**
- ✅ First search: Exactly 3 results (if available)
- ✅ Second search: Exactly 10 results (if available)
- ✅ Results sorted by similarity
- ✅ If fewer meetings exist, shows all available

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.A5 - View ChromaDB Statistics (Normal)

**Objective:** Test database statistics display

**Test Steps:**
1. Open "📊 Database Statistics" accordion
2. Click "🔄 Refresh statistics"
3. Check displayed information

**Expected Results:**

**Statistics Display:**
- ✅ Total meetings: X
- ✅ Distribution by type:
  - Meeting: Y
  - Workshop: Z
  - Brainstorming: W
- ✅ Distribution by language:
  - vi: A, en: B, ja: C, etc.
- ✅ Charts/graphs (optional)

**Accuracy:**
- ✅ Numbers match actual database
- ✅ Percentages calculated correctly
- ✅ Updates after refresh

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.A6 - Search Recordings (Normal)

**Objective:** Test searching recording history

**Preconditions:**
- 5+ recordings with different titles/notes:
  - "Team meeting Monday"
  - "Client call notes"
  - "Workshop recording"

**Test Steps:**
1. Select "🎙️ Search Recordings" sub-tab
2. Enter: "Team meeting"
3. Click "🔍 Search"

**Expected Results:**

**Search Results:**
- ✅ Recordings with "Team meeting" in title/notes displayed
- ✅ Format for each result:
  - ID: rec_001
  - Title: Team meeting Monday
  - Date: 2025-11-27
  - Duration: 5:23
  - Status: Processed
- ✅ Unrelated recordings not shown
- ✅ Case-insensitive search

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES (Error Handling)

### TC_05.B1 - Empty Query (Error)

**Objective:** Verify validation for empty search

**Test Steps:**
1. Leave search box empty
2. Click "🔍 Search"

**Expected Results:**

**Validation:**
- ✅ Error: "⚠️ Please enter search keywords"
- ✅ Orange warning color
- ✅ Input box highlighted with red border
- ✅ Focus moves to input box
- ✅ No API call made

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.B2 - No Results Found (Error)

**Objective:** Test when no matching results

**Test Steps:**
1. Enter irrelevant query: "xyz123abc999"
2. Click Search

**Expected Results:**

**Empty State:**
- ✅ Message: "❌ No matching results found"
- ✅ Suggestion: "Try different keywords or remove filters"
- ✅ Tips:
  - Use more general terms
  - Check spelling
  - Try different language
- ✅ No crash

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.B3 - ChromaDB Not Initialized (Error)

**Objective:** Test when ChromaDB not available

**Test Steps:**
1. (Simulate ChromaDB connection error)
2. Try to search

**Expected Results:**

**Error Display:**
- ✅ Error: "❌ Search database not available"
- ✅ Message: "ChromaDB connection failed"
- ✅ Troubleshooting:
  - Check ChromaDB is running
  - Restart application
  - Check database files

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.B4 - Very Long Query (Edge Case)

**Objective:** Test with extremely long search query

**Test Steps:**
1. Enter query with 500+ words
2. Click Search

**Expected Results:**

**Handling:**
- ✅ Query accepted (or truncated with warning)
- ✅ Search completes (may take longer)
- ✅ Results still relevant
- ✅ No timeout

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.B5 - Special Characters in Query (Edge Case)

**Objective:** Test search with special characters

**Test Steps:**
1. Enter: "React.js & Vue.js (comparison)"
2. Search

**Expected Results:**

**Character Handling:**
- ✅ Special chars processed correctly: . & ( ) [ ] { }
- ✅ Search works normally
- ✅ Results relevant
- ✅ No encoding errors

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_05.C1 - Search Input Box

**Objective:** Validate search input design

**Test Steps:**
1. Check input box appearance
2. Test interactions

**Expected Results:**

**Design:**
- ✅ Placeholder: "Enter search keywords..."
- ✅ Border: 1px solid gray
- ✅ Rounded corners
- ✅ Padding: 10px 15px
- ✅ Font size: 14-16px

**Interactions:**
- ✅ Focus: Blue border highlight
- ✅ Can type freely
- ✅ Clear button (X) appears when text entered
- ✅ Enter key triggers search

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C2 - Search Button States

**Objective:** Validate search button behavior

**Expected Results:**

**Default State:**
- ✅ Icon: 🔍
- ✅ Background: Blue gradient
- ✅ Text: "Search"
- ✅ Cursor: pointer

**Hover:**
- ✅ Darker blue
- ✅ Lift effect

**Loading:**
- ✅ Spinner icon
- ✅ Text: "Searching..."
- ✅ Disabled

**Disabled:**
- ✅ Gray background
- ✅ Cursor: not-allowed

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C3 - Filter Dropdowns

**Objective:** Validate filter UI

**Expected Results:**

**Meeting Type Dropdown:**
- ✅ Options: All, Meeting, Workshop, Brainstorming
- ✅ Icons for each type
- ✅ Hover effect
- ✅ Selected highlighted

**Language Dropdown:**
- ✅ Options: All, vi, en, ja, ko, zh, es, fr, de
- ✅ Flags displayed
- ✅ Native names

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C4 - Result Cards

**Objective:** Validate result display design

**Expected Results:**

**Card Design:**
- ✅ Border: 1px solid light gray
- ✅ Rounded corners
- ✅ Padding: 16px
- ✅ Shadow on hover
- ✅ Spacing between cards: 12px

**Content:**
- ✅ Meeting ID: Monospace font, small
- ✅ Type badge: Colored (blue/green/purple)
- ✅ Language flag: Small icon
- ✅ Date: Gray text
- ✅ Similarity score: Bold, green if >80%
- ✅ Preview: Truncated with "..."

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C5 - Result Count Slider

**Objective:** Validate slider design

**Expected Results:**

**Slider:**
- ✅ Track: Gray background
- ✅ Thumb: Blue circle
- ✅ Range: 1-20
- ✅ Current value displayed: "Results: 5"
- ✅ Smooth dragging

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C6 - Statistics Accordion

**Objective:** Validate statistics section

**Expected Results:**

**Accordion:**
- ✅ Header: "📊 Database Statistics"
- ✅ Expand/collapse icon
- ✅ Smooth animation
- ✅ Collapsed by default

**Content:**
- ✅ Total count prominent
- ✅ Charts/bars for distribution
- ✅ Color-coded
- ✅ Refresh button

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C7 - Example Queries

**Objective:** Validate example query buttons

**Test Steps:**
1. Check example buttons
2. Click each example

**Expected Results:**

**Examples Provided:**
- ✅ "React Hooks training"
- ✅ "budget planning meeting"
- ✅ "brainstorming new features"

**Button Behavior:**
- ✅ Click auto-fills search box
- ✅ Auto-triggers search (or requires click)
- ✅ Hover effect
- ✅ Styled as chips/pills

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.C8 - Responsive Design

**Objective:** Validate on different screens

**Expected Results:**

**Desktop (1920x1080):**
- ✅ Full layout
- ✅ Filters in row
- ✅ Results in grid (2 columns)

**Tablet (768x1024):**
- ✅ Filters may stack
- ✅ Results single column

**Mobile (375x667):**
- ✅ All elements stack vertically
- ✅ Full width components
- ✅ Touch-friendly (44px min)
- ✅ No horizontal scroll

**Actual Result:**
- [ ] Pass (Desktop)
- [ ] Pass (Tablet)
- [ ] Pass (Mobile)
- [ ] Fail

**Notes:**


---

## SECTION D: PERFORMANCE

### TC_05.D1 - Large Database (1000+ Meetings)

**Objective:** Test performance with large dataset

**Preconditions:**
- ChromaDB has 1000+ meetings

**Test Steps:**
1. Search with any query
2. Measure time

**Expected Results:**

**Performance:**
- ✅ Search completes in < 5 seconds
- ✅ Results accurate
- ✅ UI responsive
- ✅ No timeout

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_05.D2 - Rapid Searches

**Objective:** Test multiple searches quickly

**Test Steps:**
1. Perform 10 searches rapidly
2. Check performance

**Expected Results:**

**Performance:**
- ✅ All searches complete
- ✅ No queue overflow
- ✅ Results accurate
- ✅ No memory leaks

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 6 | 0 | 0 | 0 |
| Abnormal Cases | 5 | 0 | 0 | 0 |
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

