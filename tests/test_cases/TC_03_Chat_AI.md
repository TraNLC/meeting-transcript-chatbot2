# TC_03 - Chat with AI Tab

## General Information
- **Module:** Chat with AI Tab
- **Priority:** High
- **Tester:** 
- **Date:** 11/27/2025

---

## TC_03.1 - Basic Chat

### Description
Test basic chat functionality with AI about transcript

### Preconditions
- Transcript analyzed successfully

### Test Steps
1. Open "💬 Chat with AI" tab
2. Enter question: "Summarize this meeting"
3. Click "📤 Send"

### Expected Result
- ✅ Question displayed in chatbot
- ✅ AI responds in < 10 seconds
- ✅ Answer related to transcript
- ✅ Answer in selected language

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.2 - Suggested Questions

### Description
Test suggested question buttons

### Test Steps
1. Click "📋 Summarize meeting" button
2. Click "👥 Who participated?" button
3. Click "✅ What are action items?" button
4. Click "🎯 Important decisions?" button
5. Click "📊 Main topics?" button

### Expected Result
- ✅ Each button auto-sends question
- ✅ AI answers appropriately
- ✅ Chat history saved

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.3 - Continuous Chat

### Description
Test multi-turn conversation

### Test Steps
1. Ask: "What are the main topics?"
2. Follow up: "Explain the first topic in detail"
3. Follow up: "Are there related action items?"

### Expected Result
- ✅ AI remembers previous context
- ✅ Answers logically connected
- ✅ Complete chat history

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.4 - Clear Chat History

### Description
Test clear history functionality

### Preconditions
- Chat history exists

### Test Steps
1. Click "🗑️ Clear history"

### Expected Result
- ✅ All chat cleared
- ✅ Chatbot empty
- ✅ Can start new chat immediately

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.5 - Error Handling - No Transcript

### Description
Test chat without analyzing transcript first

### Preconditions
- No transcript analyzed

### Test Steps
1. Open Chat tab
2. Enter any question
3. Click Send

### Expected Result
- ✅ Display: "⚠️ Please process transcript first!"
- ✅ No API call
- ✅ Clear instructions provided

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.6 - Irrelevant Questions

### Description
Test AI handling off-topic questions

### Test Steps
1. Ask: "What's the weather today?"
2. Ask: "What is 2 + 2?"

### Expected Result
- ✅ AI politely declines
- ✅ Guides to ask about transcript
- ✅ No crash

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.7 - Submit with Enter

### Description
Test sending question with Enter key

### Test Steps
1. Type question
2. Press Enter (don't click Send button)

### Expected Result
- ✅ Question sent
- ✅ Input cleared
- ✅ AI responds normally

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## TC_03.8 - Performance - Long Question

### Description
Test with very long question

### Test Steps
1. Enter question > 500 words
2. Send

### Expected Result
- ✅ Question processed
- ✅ AI responds in < 15 seconds
- ✅ No timeout

### Actual Result
- [ ] Pass
- [ ] Fail

### Notes


---

## Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC_03.1 | ⏳ | High | |
| TC_03.2 | ⏳ | High | |
| TC_03.3 | ⏳ | Medium | |
| TC_03.4 | ⏳ | Low | |
| TC_03.5 | ⏳ | Medium | |
| TC_03.6 | ⏳ | Low | |
| TC_03.7 | ⏳ | Medium | |
| TC_03.8 | ⏳ | Low | |

**Legend:** ✅ Pass | ❌ Fail | ⏳ Pending | ⚠️ Blocked
