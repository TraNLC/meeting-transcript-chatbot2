# TC_06 - Export Results Tab

## General Information
- **Module:** Export Results Tab
- **Priority:** Medium
- **Tester:** 
- **Date:** 11/27/2025

---

## TC_06.1 - Export TXT File

### Description
Test exporting analysis results to TXT file

### Preconditions
- Transcript analyzed successfully

### Test Steps
1. Open "📄 Export Results" tab
2. Click "📄 Export TXT"
3. Check downloaded file

### Expected Result
- ✅ File created: `meeting_analysis_YYYYMMDD_HHMMSS.txt`
- ✅ File downloadable
- ✅ Content includes:
  - Header with title
  - Filename and timestamp
  - Summary
  - Topics
  - Action items
  - Decisions
- ✅ Readable format with separators
- ✅ UTF-8 encoding (Vietnamese displays correctly)

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.2 - Export DOCX File

### Description
Test exporting results to Word file

### Preconditions
- Transcript analyzed

### Test Steps
1. Click "📝 Export DOCX"
2. Open file in Microsoft Word

### Expected Result
- ✅ File created: `meeting_analysis_YYYYMMDD_HHMMSS.docx`
- ✅ File opens in Word
- ✅ Professional format:
  - Centered title
  - Styled headings
  - Proper bullet points
  - Readable font
- ✅ Complete content like TXT
- ✅ Editable

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.3 - Export with Different Languages

### Description
Test exporting files with different output languages

### Test Data
| Language | Expected Headers |
|----------|------------------|
| vi | TÓM TẮT, CHỦ ĐỀ, ACTION ITEMS |
| en | SUMMARY, TOPICS, ACTION ITEMS |

### Test Steps
1. Analyze with language vi
2. Export TXT
3. Analyze with language en
4. Export TXT
5. Compare headers

### Expected Result
- ✅ Headers in correct language
- ✅ Content in correct language
- ✅ No encoding errors

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.4 - Error Handling - No Data

### Description
Test exporting without analysis

### Preconditions
- No transcript analyzed

### Test Steps
1. Click "📄 Export TXT"

### Expected Result
- ✅ No file created
- ✅ Error message displayed (or nothing happens)
- ✅ No crash

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.5 - Export Multiple Times

### Description
Test exporting files multiple times consecutively

### Test Steps
1. Click "📄 Export TXT"
2. Wait 2 seconds
3. Click "📄 Export TXT" again
4. Click "📝 Export DOCX"

### Expected Result
- ✅ Each time creates new file with different timestamp
- ✅ Old files not overwritten
- ✅ All files valid

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.6 - Check TXT File Content

### Description
Test detailed TXT file content

### Test Steps
1. Export TXT
2. Open file in Notepad
3. Check each section

### Expected Result
- ✅ Header has "=" separator
- ✅ Filename and timestamp accurate
- ✅ Complete summary
- ✅ Topics numbered (1., 2., 3.)
- ✅ Action items include:
  - Task description
  - Assignee
  - Deadline
- ✅ Decisions include:
  - Decision text
  - Context
- ✅ Footer has separator

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.7 - Check DOCX File Format

### Description
Test detailed DOCX file formatting

### Test Steps
1. Export DOCX
2. Open in Word
3. Check styles

### Expected Result
- ✅ Title: Heading 0, centered
- ✅ Sections: Heading 1
- ✅ Topics: Numbered list
- ✅ Action items: Numbered list with sub-bullets
- ✅ Font: Inter or Arial
- ✅ Can apply other styles
- ✅ Can copy/paste

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.8 - Reasonable File Size

### Description
Test exported file sizes

### Test Steps
1. Export TXT and DOCX
2. Check file sizes

### Expected Result
- ✅ TXT: < 100 KB (for normal transcript)
- ✅ DOCX: < 500 KB
- ✅ Files not too large
- ✅ Opens quickly

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.9 - Compatibility

### Description
Test file opens in different applications

### Test Steps
1. Export DOCX
2. Try opening in:
   - Microsoft Word
   - Google Docs
   - LibreOffice Writer

### Expected Result
- ✅ Opens in all applications
- ✅ Format preserved
- ✅ No warnings

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_06.10 - Export with Special Characters

### Description
Test exporting with special characters, emoji

### Preconditions
- Transcript contains emoji, special characters

### Test Steps
1. Analyze transcript with: 🎯 ✅ 📊 Vietnamese with diacritics
2. Export TXT and DOCX

### Expected Result
- ✅ Emoji displays correctly
- ✅ Vietnamese diacritics correct
- ✅ Special characters no errors

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC_06.1 | ⏳ | High | |
| TC_06.2 | ⏳ | High | |
| TC_06.3 | ⏳ | Medium | |
| TC_06.4 | ⏳ | Medium | |
| TC_06.5 | ⏳ | Low | |
| TC_06.6 | ⏳ | Medium | |
| TC_06.7 | ⏳ | Medium | |
| TC_06.8 | ⏳ | Low | |
| TC_06.9 | ⏳ | Medium | |
| TC_06.10 | ⏳ | Low | |

**Legend:** ✅ Pass | ❌ Fail | ⏳ Pending | ⚠️ Blocked
