# TC_05 - Smart Search Tab

## General Information
- **Module:** Smart Search Tab
- **Priority:** Medium
- **Tester:** 
- **Date:** 11/27/2025

---

## TC_05.1 - Basic Semantic Search

### Description
Test semantic search with ChromaDB

### Preconditions
- At least 5 meetings in ChromaDB

### Test Steps
1. Open "🔍 Smart Search" tab
2. Select "📊 Search Analysis" sub-tab
3. Enter: "React Hooks training"
4. Click "🔍 Search"

### Expected Result
- ✅ Status displays: "✅ Found X matching meetings"
- ✅ Results related to React Hooks
- ✅ Display: Meeting ID, Type, Language, Date
- ✅ Similarity score (%) displayed
- ✅ Transcript preview displayed
- ✅ Search time < 3 seconds

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.2 - Filter by Meeting Type

### Description
Test filtering results by meeting type

### Test Steps
1. Enter query: "team meeting"
2. Select filter "Meeting Type": "workshop"
3. Search

### Expected Result
- ✅ Only "workshop" meetings displayed
- ✅ Results still relevant to query
- ✅ Result count reduced vs no filter

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.3 - Filter by Language

### Description
Test filtering by language

### Test Steps
1. Enter query: "budget planning"
2. Select filter "Language": "en"
3. Search

### Expected Result
- ✅ Only English meetings displayed
- ✅ Results accurate

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.4 - Adjust Result Count

### Description
Test result count slider

### Test Steps
1. Enter query: "project update"
2. Set slider "Number of results" = 3
3. Search
4. Set slider = 10
5. Search again

### Expected Result
- ✅ First time: Exactly 3 results
- ✅ Second time: Exactly 10 results (if available)
- ✅ Results sorted by similarity

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.5 - View ChromaDB Statistics

### Description
Test database statistics display

### Test Steps
1. Open "📊 Database Statistics" accordion
2. Click "🔄 Refresh statistics"

### Expected Result
- ✅ Display: Total meetings
- ✅ Display: Distribution by type
- ✅ Display: Distribution by language
- ✅ Accurate numbers

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.6 - Search Recordings

### Description
Test searching recording history

### Preconditions
- At least 3 recordings with different titles/notes

### Test Steps
1. Select "🎙️ Search Recordings" sub-tab
2. Enter: "Team meeting"
3. Click "🔍 Search"

### Expected Result
- ✅ Display recordings with "Team meeting" in title/notes
- ✅ Format: ID, Title, Date, Duration, Status
- ✅ Unrelated recordings not displayed

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.7 - Error Handling - Empty Query

### Description
Test searching with empty query

### Test Steps
1. Don't enter anything
2. Click "🔍 Search"

### Expected Result
- ✅ Display: "⚠️ Please enter search keywords"
- ✅ No API call
- ✅ No errors

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.8 - Error Handling - No Results

### Description
Test when no results found

### Test Steps
1. Enter irrelevant query: "xyz123abc"
2. Search

### Expected Result
- ✅ Display: "❌ No matching results found"
- ✅ Suggest trying different query
- ✅ No crash

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.9 - Test with Examples

### Description
Test provided examples

### Test Steps
1. Click example: "React Hooks training"
2. Check results
3. Click example: "budget planning meeting"
4. Click example: "brainstorming new features"

### Expected Result
- ✅ Each example auto-fills form
- ✅ Search successful
- ✅ Results match example

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_05.10 - Performance - Large Database

### Description
Test performance with many meetings

### Preconditions
- ChromaDB has > 100 meetings

### Test Steps
1. Search with any query
2. Measure time

### Expected Result
- ✅ Search time < 5 seconds
- ✅ Results accurate
- ✅ UI not lagging

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC_05.1 | ⏳ | High | |
| TC_05.2 | ⏳ | Medium | |
| TC_05.3 | ⏳ | Medium | |
| TC_05.4 | ⏳ | Low | |
| TC_05.5 | ⏳ | Low | |
| TC_05.6 | ⏳ | Medium | |
| TC_05.7 | ⏳ | Medium | |
| TC_05.8 | ⏳ | Medium | |
| TC_05.9 | ⏳ | Low | |
| TC_05.10 | ⏳ | Low | |

**Legend:** ✅ Pass | ❌ Fail | ⏳ Pending | ⚠️ Blocked
