# TC_02 - Upload & Analysis Tab (DETAILED)

## Test Environment
- **Browser:** Chrome 120+, Firefox 120+, Safari 17+
- **Screen Resolution:** 1920x1080, 1366x768, Mobile (375x667)
- **Network:** Fast (100Mbps), Slow (3G), Offline

---

## SECTION A: NORMAL CASES (Happy Path)

### TC_02.A1 - Upload Small TXT File (Normal)

**Objective:** Verify basic upload and analysis workflow

**Preconditions:**
- Sample file: `data/test_samples/normal_meeting_100_words.txt`
- File size: ~1KB
- Content: 100 words, clean text, no special chars

**Test Steps:**
1. Navigate to "📤 Upload & Phân Tích" tab
2. Click "Chọn file transcript (TXT, DOCX)"
3. Select `normal_meeting_100_words.txt`
4. Verify file name displays in upload box
5. Select "Loại Cuộc Họp": "📋 Meeting - Cuộc họp thông thường"
6. Select "Ngôn Ngữ Output": "🇻🇳 Tiếng Việt"
7. Click "🚀 Phân Tích Ngay" button
8. Wait for processing

**Expected Results:**

**UI/UX Validation:**
- ✅ File upload box shows: "normal_meeting_100_words.txt"
- ✅ Upload box has green checkmark icon
- ✅ "Phân Tích Ngay" button is enabled (not grayed out)
- ✅ Button shows loading spinner during processing
- ✅ Processing takes 5-15 seconds

**Status Display:**
- ✅ Shows: "✅ Đã xử lý: normal_meeting_100_words.txt | Loại: meeting | Ngôn ngữ: vi"
- ✅ Text color: Green (#10b981)
- ✅ No error messages

**Results Display:**
- ✅ "📝 Tóm Tắt Cuộc Họp" section populated with 3-5 sentences
- ✅ "🎯 Chủ Đề Chính" shows 2-3 topics with descriptions
- ✅ "✅ Action Items" shows at least 1 action with assignee & deadline
- ✅ "🎯 Quyết Định Quan Trọng" shows at least 1 decision
- ✅ All text in Vietnamese
- ✅ Proper formatting (bullets, numbering)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Screenshots:**
- [ ] Before upload
- [ ] During processing
- [ ] After completion

**Notes:**


---

### TC_02.A2 - Upload DOCX File (Normal)

**Objective:** Verify DOCX file format support

**Preconditions:**
- Sample file: `data/test_samples/normal_workshop_200_words.docx`
- File size: ~5KB
- Content: 200 words, formatted text, bold/italic

**Test Steps:**
1. Upload `normal_workshop_200_words.docx`
2. Select "Loại": "🎓 Workshop - Hội thảo/Đào tạo"
3. Select "Ngôn ngữ": "🇬🇧 English"
4. Click "Phân Tích Ngay"

**Expected Results:**

**UI/UX:**
- ✅ DOCX icon displayed in upload box
- ✅ File size shown: "~5KB"
- ✅ Processing time: 10-20 seconds

**Output:**
- ✅ Summary in English
- ✅ Topics focus on learning points (workshop-specific)
- ✅ Action items include practice exercises
- ✅ Formatting preserved (no garbled text)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES (Error Handling)

### TC_02.B1 - Upload Without Selecting File

**Objective:** Verify validation when no file selected

**Test Steps:**
1. Navigate to Upload tab
2. Do NOT select any file
3. Click "🚀 Phân Tích Ngay" directly

**Expected Results:**

**Error Display:**
- ✅ Status box shows: "❌ Vui lòng upload file!"
- ✅ Text color: Red (#ef4444)
- ✅ Background: Light red (#fee2e2)
- ✅ Icon: ❌ or ⚠️
- ✅ Error appears immediately (< 0.5s)
- ✅ No API call made (check network tab)

**UI State:**
- ✅ Upload box highlighted with red border
- ✅ Shake animation on upload box (optional)
- ✅ Focus moves to upload box
- ✅ Results sections remain empty

**User Guidance:**
- ✅ Tooltip appears: "Please select a file first"
- ✅ Upload box pulses to draw attention

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B2 - Upload 1000-Page File (Extreme Size)

**Objective:** Test truncation and performance with huge file

**Preconditions:**
- Sample file: `data/test_samples/extreme_1000_pages.txt`
- File size: ~5MB
- Content: 500,000 words (simulated 1000 pages)

**Test Steps:**
1. Upload `extreme_1000_pages.txt`
2. Select any meeting type
3. Select any language
4. Click "Phân Tích Ngay"
5. Monitor processing

**Expected Results:**

**Upload Phase:**
- ✅ File uploads successfully (may take 2-5 seconds)
- ✅ File size displayed: "~5MB"
- ✅ Warning message: "⚠️ File is very large and will be truncated"
- ✅ Warning color: Orange (#f59e0b)

**Processing Phase:**
- ✅ Progress indicator shows: "Đang xử lý... (truncating large file)"
- ✅ Processing completes in < 60 seconds
- ✅ No timeout error
- ✅ No browser freeze/crash

**Results:**
- ✅ Status shows: "✅ Đã xử lý (truncated to 15,000 chars)"
- ✅ Info message: "ℹ️ Original file was truncated to fit API limits"
- ✅ Analysis based on first 15,000 characters
- ✅ Results still meaningful

**Performance:**
- ✅ Memory usage < 2GB
- ✅ CPU usage returns to normal after processing
- ✅ No memory leaks

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B3 - Upload Empty File (0 bytes)

**Objective:** Verify empty file validation

**Preconditions:**
- Sample file: `data/test_samples/empty_file.txt`
- File size: 0 bytes

**Test Steps:**
1. Upload `empty_file.txt`
2. Click "Phân Tích Ngay"

**Expected Results:**

**Error Display:**
- ✅ Status: "❌ File is empty (0 bytes)"
- ✅ Red text with error icon
- ✅ Detailed message: "The uploaded file contains no content. Please upload a valid transcript file."

**UI Feedback:**
- ✅ Upload box shows red border
- ✅ File name crossed out or grayed
- ✅ "Phân Tích Ngay" button disabled

**User Guidance:**
- ✅ Suggestion: "Try uploading a different file"
- ✅ Link to sample files: "Download sample transcript"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B4 - Upload File with Only 5 Words

**Objective:** Test minimum content validation

**Preconditions:**
- Sample file: `data/test_samples/too_short_5_words.txt`
- Content: "Hello this is a test"

**Test Steps:**
1. Upload file
2. Analyze

**Expected Results:**

**Error Display:**
- ✅ Status: "❌ Transcript too short (5 words)"
- ✅ Message: "Minimum 50 words required for meaningful analysis"
- ✅ Current word count shown: "Current: 5 words | Required: 50 words"

**UI:**
- ✅ Progress bar showing: 5/50 words (10%)
- ✅ Red progress bar

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B5 - Upload Invalid File Format (PDF)

**Objective:** Test file format validation

**Preconditions:**
- Sample file: `data/test_samples/invalid_format.pdf`

**Test Steps:**
1. Try to upload PDF file

**Expected Results:**

**Validation:**
- ✅ File picker only shows .txt and .docx files
- ✅ PDF file grayed out in file picker
- ✅ If user forces upload (drag & drop):
  - Error: "❌ Invalid file format"
  - Message: "Only TXT and DOCX files are supported"
  - Supported formats listed: "Supported: .txt, .docx"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B6 - Upload Corrupted DOCX File

**Objective:** Test corrupted file handling

**Preconditions:**
- Sample file: `data/test_samples/corrupted_file.docx`
- File: Renamed ZIP file or corrupted DOCX

**Test Steps:**
1. Upload corrupted file
2. Click "Phân Tích Ngay"

**Expected Results:**

**Error Handling:**
- ✅ Status: "❌ File corrupted or unreadable"
- ✅ Technical details (collapsible): "Error: BadZipFile - File is not a valid DOCX"
- ✅ User-friendly message: "The file appears to be corrupted. Please try:"
  - Re-saving the file
  - Converting to TXT format
  - Uploading a different file

**No Crash:**
- ✅ App remains functional
- ✅ Can upload another file immediately
- ✅ No console errors visible to user

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B7 - Upload File with Special Characters & Emojis

**Objective:** Test encoding and special character handling

**Preconditions:**
- Sample file: `data/test_samples/special_chars_emojis.txt`
- Content: "Meeting 🎯 with team àáảãạ こんにちは 안녕하세요 你好"

**Test Steps:**
1. Upload file
2. Analyze
3. Check output

**Expected Results:**

**Character Preservation:**
- ✅ All emojis displayed: 🎯 ✅ 📊 💬
- ✅ Vietnamese diacritics: àáảãạ êếễệ
- ✅ Japanese: こんにちは
- ✅ Korean: 안녕하세요
- ✅ Chinese: 你好

**No Errors:**
- ✅ No encoding errors
- ✅ No "?" or "□" characters
- ✅ Proper UTF-8 handling

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B8 - API Timeout (No Internet)

**Objective:** Test offline/timeout handling

**Test Steps:**
1. Disconnect internet
2. Upload file
3. Click "Phân Tích Ngay"
4. Wait for timeout

**Expected Results:**

**Timeout Handling:**
- ✅ Loading spinner shows for 30 seconds
- ✅ Then error: "❌ Connection timeout"
- ✅ Message: "Unable to reach AI service. Please check your internet connection."

**Retry Mechanism:**
- ✅ "🔄 Retry" button appears
- ✅ Clicking retry attempts again
- ✅ File data preserved (no need to re-upload)

**User Guidance:**
- ✅ Troubleshooting tips:
  - Check internet connection
  - Check firewall settings
  - Try again in a few minutes

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.B9 - API Rate Limit Exceeded

**Objective:** Test rate limit handling

**Test Steps:**
1. Upload and analyze 20 files rapidly (< 1 minute)
2. Trigger rate limit

**Expected Results:**

**Rate Limit Error:**
- ✅ Status: "⚠️ Rate limit exceeded"
- ✅ Message: "Too many requests. Please wait 60 seconds."
- ✅ Countdown timer: "Retry in: 59s, 58s, 57s..."

**UI State:**
- ✅ "Phân Tích Ngay" button disabled
- ✅ Button shows countdown
- ✅ After countdown, button re-enables

**Queue System (Optional):**
- ✅ Pending requests queued
- ✅ Queue status shown: "2 files in queue"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_02.C1 - Meeting Type Dropdown

**Objective:** Validate dropdown functionality and options

**Test Steps:**
1. Click "Loại Cuộc Họp" dropdown
2. Hover over each option
3. Select each option
4. Check behavior

**Expected Results:**

**Dropdown Behavior:**
- ✅ Opens smoothly (no lag)
- ✅ Shows 3 options:
  1. "📋 Meeting - Cuộc họp thông thường"
  2. "🎓 Workshop - Hội thảo/Đào tạo"
  3. "💡 Brainstorming - Động não"
- ✅ Icons displayed correctly
- ✅ Hover effect: Light green background (#d1fae5)
- ✅ Selected option highlighted: Green (#10b981)

**Selection:**
- ✅ Click selects option
- ✅ Dropdown closes after selection
- ✅ Selected value displayed in dropdown
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

### TC_02.C2 - Language Dropdown

**Objective:** Validate language selection

**Test Steps:**
1. Click "Ngôn Ngữ Output" dropdown
2. Check all 8 languages
3. Test selection

**Expected Results:**

**Languages Available:**
- ✅ 🇻🇳 Tiếng Việt (vi)
- ✅ 🇬🇧 English (en)
- ✅ 🇯🇵 日本語 (ja)
- ✅ 🇰🇷 한국어 (ko)
- ✅ 🇨🇳 中文 (zh-CN)
- ✅ 🇪🇸 Español (es)
- ✅ 🇫🇷 Français (fr)
- ✅ 🇩🇪 Deutsch (de)

**Display:**
- ✅ Flags displayed correctly
- ✅ Native language names
- ✅ Alphabetical order (optional)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_02.C3 - Button States

**Objective:** Validate button states and feedback

**Test Steps:**
1. Check "Phân Tích Ngay" button in different states

**Expected Results:**

**Default State:**
- ✅ Green gradient background
- ✅ White text
- ✅ Rocket icon: 🚀
- ✅ Cursor: pointer

**Hover State:**
- ✅ Slightly darker green
- ✅ Lift effect (translateY(-2px))
- ✅ Shadow appears

**Disabled State:**
- ✅ Gray background (#9ca3af)
- ✅ Cursor: not-allowed
- ✅ No hover effect

**Loading State:**
- ✅ Spinner icon replaces rocket
- ✅ Text: "Đang xử lý..."
- ✅ Button disabled
- ✅ Pulsing animation

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION D: SAMPLE DATA FILES

Create these files in `data/test_samples/`:

### Normal Cases:
1. **normal_meeting_100_words.txt** - 100 words, clean
2. **normal_workshop_200_words.docx** - 200 words, formatted
3. **normal_brainstorm_150_words.txt** - 150 words

### Abnormal Cases:
4. **empty_file.txt** - 0 bytes
5. **too_short_5_words.txt** - 5 words only
6. **extreme_1000_pages.txt** - 500,000 words
7. **special_chars_emojis.txt** - Unicode, emojis
8. **corrupted_file.docx** - Invalid DOCX
9. **invalid_format.pdf** - PDF file
10. **only_numbers.txt** - "123 456 789"
11. **only_symbols.txt** - "!@#$%^&*()"
12. **mixed_languages.txt** - English + Vietnamese + Japanese

---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 2 | 0 | 0 | 0 |
| Abnormal Cases | 9 | 0 | 0 | 0 |
| UI/UX Validation | 3 | 0 | 0 | 0 |
| **TOTAL** | **14** | **0** | **0** | **0** |

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
