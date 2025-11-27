# TC_04 - Analysis History Tab (DETAILED)

## Test Environment
- **Storage:** Local JSON files
- **Location:** data/history/

---

## SECTION A: NORMAL CASES

### TC_04.A1 - View History List

**Objective:** Test displaying analysis history

**Preconditions:**
- At least 5 analyses saved

**Test Steps:**
1. Navigate to "📊 Lịch Sử Phân Tích" tab
2. Click "🔄 Làm mới"
3. Check dropdown

**Expected Results:**

**Dropdown Display:**
- ✅ Shows all analyses (max 20)
- ✅ Format: "YYYY-MM-DD - filename.txt"
- ✅ Sorted: Newest first
- ✅ Scrollable if > 10 items

**Statistics:**
- ✅ Shows: "📊 Tìm thấy X phân tích đã lưu"
- ✅ Count accurate

**Performance:**
- ✅ Loads in < 2 seconds
- ✅ No lag when opening dropdown

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.A2 - Load Analysis

**Objective:** Test loading previous analysis

**Test Steps:**
1. Select analysis from dropdown
2. Click "📂 Tải vào workspace"
3. Check loaded data

**Expected Results:**

**Loading Process:**
- ✅ Status: "✅ Đã tải phân tích: [filename]"
- ✅ Loading time: < 1 second

**Data Display:**
- ✅ Summary populated
- ✅ Topics displayed with formatting
- ✅ All data matches original analysis

**Integration:**
- ✅ Can chat about loaded transcript
- ✅ Can export loaded analysis
- ✅ Data persists when switching tabs

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES

### TC_04.B1 - Empty History

**Objective:** Test when no history exists

**Preconditions:**
- Delete all history files
- Or fresh installation

**Test Steps:**
1. Open History tab
2. Click Refresh

**Expected Results:**

**Empty State:**
- ✅ Dropdown empty
- ✅ Message: "_Chưa có lịch sử_"
- ✅ Helpful text: "Analyze a transcript to create history"
- ✅ No error messages

**UI:**
- ✅ Load button disabled
- ✅ Delete button disabled
- ✅ Clean, not broken

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B2 - Corrupted History File

**Objective:** Test with corrupted JSON file

**Preconditions:**
- Corrupt one history JSON file

**Test Steps:**
1. Refresh history
2. Try to load corrupted file

**Expected Results:**

**Error Handling:**
- ✅ Corrupted file skipped
- ✅ Other files still load
- ✅ Warning: "⚠️ 1 file could not be loaded"
- ✅ No crash

**User Action:**
- ✅ Option to delete corrupted file
- ✅ App remains functional

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B3 - Delete Analysis

**Objective:** Test delete functionality

**Test Steps:**
1. Select analysis
2. Click "🗑️ Xóa"
3. Confirm deletion

**Expected Results:**

**Confirmation:**
- ✅ Popup: "Delete this analysis?"
- ✅ Shows filename
- ✅ "Yes, delete" (red) and "Cancel" buttons

**After Delete:**
- ✅ Success: "✅ Đã xóa [filename]"
- ✅ File removed from disk
- ✅ Dropdown updated automatically
- ✅ Count decremented

**Cannot Undo:**
- ✅ Warning: "This action cannot be undone"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.B4 - Load Non-Existent Analysis

**Objective:** Test loading deleted/missing file

**Test Steps:**
1. Select analysis
2. Manually delete file from disk
3. Click "Tải vào workspace"

**Expected Results:**

**Error Handling:**
- ✅ Error: "❌ File not found"
- ✅ Message: "This analysis may have been deleted"
- ✅ Option to remove from list
- ✅ No crash

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_04.C1 - Dropdown Behavior

**Objective:** Validate dropdown functionality

**Expected Results:**

**Interaction:**
- ✅ Opens on click
- ✅ Closes on selection
- ✅ Closes on outside click
- ✅ Search/filter works (if available)

**Display:**
- ✅ Readable font size
- ✅ Proper spacing
- ✅ Hover effect
- ✅ Selected item highlighted

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_04.C2 - Button States

**Objective:** Validate button states

**Expected Results:**

**Load Button:**
- Disabled: No selection
- Enabled: Selection made
- Loading: Spinner icon
- Success: Green checkmark (brief)

**Delete Button:**
- Disabled: No selection
- Enabled: Red color
- Confirm: Popup appears
- Success: Item removed

**Refresh Button:**
- Always enabled
- Loading: Spinner icon
- Success: List updated

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 2 | 0 | 0 | 0 |
| Abnormal Cases | 4 | 0 | 0 | 0 |
| UI/UX Validation | 2 | 0 | 0 | 0 |
| **TOTAL** | **8** | **0** | **0** | **0** |

**Success Rate:** 0% (Not tested yet)

---

## Notes & Observations

**Issues Found:**
1. 
2. 

**Improvements Needed:**
1. 
2. 

**Tested By:** _______________
**Date:** _______________
