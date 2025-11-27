# TC_03 - Chat with AI Tab (DETAILED)

## Test Environment
- **Browser:** Chrome 120+, Firefox 120+, Safari 17+
- **Screen Resolution:** 1920x1080, 1366x768, Mobile (375x667)
- **Network:** Fast (100Mbps), Slow (3G), Offline
- **API:** OpenAI GPT-4 or compatible

---

## SECTION A: NORMAL CASES (Happy Path)

### TC_03.A1 - Basic Chat Question (Normal)

**Objective:** Verify basic chat functionality with AI about transcript

**Preconditions:**
- Transcript analyzed successfully in Upload tab
- Sample transcript: Meeting about React Hooks training (200 words)
- ChromaDB has context loaded

**Test Steps:**
1. Navigate to "💬 Chat with AI" tab
2. Verify chat interface is ready
3. Type question in input box: "Summarize this meeting in 3 sentences"
4. Click "📤 Send" button (or press Enter)
5. Wait for AI response

**Expected Results:**

**UI/UX Validation:**
- ✅ Question appears in chat immediately
- ✅ Question displayed in user bubble (right-aligned, blue background)
- ✅ Timestamp shown: "[14:30]"
- ✅ Loading indicator appears: "🤔 AI is thinking..."
- ✅ Typing animation (three dots bouncing)

**Response Time:**
- ✅ AI responds in < 10 seconds
- ✅ No timeout errors
- ✅ Response appears smoothly (fade in animation)

**Response Quality:**
- ✅ Answer displayed in AI bubble (left-aligned, gray background)
- ✅ Response is relevant to transcript
- ✅ Response in selected language (matches transcript language)
- ✅ Response length: 3-5 sentences (as requested)
- ✅ Proper formatting (paragraphs, bullets if needed)

**Chat History:**
- ✅ Both question and answer saved in chat
- ✅ Scrollable if content exceeds viewport
- ✅ Auto-scroll to latest message

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Screenshots:**
- [ ] Before sending
- [ ] During AI thinking
- [ ] After response

**Notes:**


---

### TC_03.A2 - Suggested Questions (Normal)

**Objective:** Test pre-defined suggested question buttons

**Preconditions:**
- Transcript analyzed

**Test Steps:**
1. Verify suggested question buttons are visible
2. Click "📋 Summarize meeting" button
3. Wait for response
4. Click "👥 Who participated?" button
5. Wait for response
6. Click "✅ What are action items?" button
7. Click "🎯 Important decisions?" button
8. Click "📊 Main topics?" button

**Expected Results:**

**Button Display:**
- ✅ 5 suggested buttons visible:
  - 📋 Summarize meeting
  - 👥 Who participated?
  - ✅ What are action items?
  - 🎯 Important decisions?
  - 📊 Main topics?
- ✅ Buttons styled consistently (rounded, with icons)
- ✅ Hover effect (color change)

**Button Behavior:**
- ✅ Click auto-fills question in input
- ✅ Question auto-sends (no need to click Send)
- ✅ Button disabled during processing
- ✅ Button re-enables after response

**Responses:**
- ✅ Each question gets relevant answer
- ✅ Answers specific to button topic:
  - Summary: 3-5 sentence overview
  - Participants: List of names/roles
  - Action items: Numbered list with assignees
  - Decisions: Key decisions made
  - Topics: Main discussion points
- ✅ All responses accurate

**Chat History:**
- ✅ All Q&A pairs saved in order
- ✅ Can scroll through history

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.A3 - Multi-turn Conversation (Normal)

**Objective:** Test contextual follow-up questions

**Preconditions:**
- Transcript analyzed

**Test Steps:**
1. Ask: "What are the main topics discussed?"
2. Wait for response
3. Follow up: "Explain the first topic in more detail"
4. Wait for response
5. Follow up: "Are there any action items related to this topic?"
6. Wait for response
7. Follow up: "Who is responsible for these actions?"

**Expected Results:**

**Context Retention:**
- ✅ AI remembers previous questions
- ✅ AI understands "first topic" refers to previous answer
- ✅ AI understands "this topic" and "these actions" from context
- ✅ Answers logically connected across turns

**Response Quality:**
- ✅ Each answer builds on previous context
- ✅ No repetition of information
- ✅ Coherent conversation flow
- ✅ AI doesn't ask "which topic?" (understands context)

**Chat History:**
- ✅ Complete conversation thread visible
- ✅ Easy to follow conversation flow
- ✅ Timestamps for each message

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.A4 - Complex Question with Multiple Parts (Normal)

**Objective:** Test handling of complex, multi-part questions

**Test Steps:**
1. Ask complex question: "What were the main topics, who participated, and what are the next steps? Please organize your answer with bullet points."
2. Wait for response

**Expected Results:**

**Response Structure:**
- ✅ AI addresses all parts of question:
  1. Main topics listed
  2. Participants identified
  3. Next steps outlined
- ✅ Response well-organized with:
  - Clear sections/headings
  - Bullet points as requested
  - Logical flow

**Response Quality:**
- ✅ Complete answer (nothing missed)
- ✅ Proper formatting (markdown rendered)
- ✅ Easy to read and scan

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION B: ABNORMAL CASES (Error Handling)

### TC_03.B1 - Chat Without Transcript (Error)

**Objective:** Verify validation when no transcript analyzed

**Preconditions:**
- Fresh application start
- No transcript analyzed yet

**Test Steps:**
1. Navigate directly to "💬 Chat with AI" tab
2. Try to type question: "What is this meeting about?"
3. Click "📤 Send"

**Expected Results:**

**Error Display:**
- ✅ Status message: "⚠️ Please analyze a transcript first!"
- ✅ Warning color: Orange (#f59e0b)
- ✅ Icon: ⚠️
- ✅ Error appears immediately (< 0.5s)

**UI State:**
- ✅ Send button disabled (or shows warning)
- ✅ Input box disabled or shows placeholder: "Analyze transcript first"
- ✅ Suggested buttons disabled or hidden

**User Guidance:**
- ✅ Clear instructions: "Go to 'Recording' or 'Upload' tab to analyze a transcript first"
- ✅ Link/button to navigate to Upload tab
- ✅ No API call made (check network tab)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B2 - Empty Question (Error)

**Objective:** Verify validation for empty input

**Test Steps:**
1. Leave input box empty
2. Click "📤 Send" button

**Expected Results:**

**Validation:**
- ✅ Error message: "⚠️ Please enter a question"
- ✅ Input box highlighted with red border
- ✅ Shake animation on input box (optional)
- ✅ Focus returns to input box
- ✅ No API call made

**UI Feedback:**
- ✅ Error appears immediately
- ✅ Error dismisses when user starts typing
- ✅ Send button remains enabled

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B3 - Very Long Question (1000+ Words)

**Objective:** Test handling of extremely long questions

**Preconditions:**
- Prepare question with 1000+ words

**Test Steps:**
1. Paste very long question (1000 words)
2. Click Send
3. Monitor processing

**Expected Results:**

**Input Handling:**
- ✅ Input accepts long text (no character limit or reasonable limit like 5000)
- ✅ Input box expands or scrollable
- ✅ Can see full question

**Processing:**
- ✅ Question sent successfully
- ✅ May take longer (15-20 seconds acceptable)
- ✅ Loading indicator shows
- ✅ No timeout (or timeout > 30 seconds)

**Response:**
- ✅ AI responds appropriately
- ✅ May truncate question if too long (with notice)
- ✅ Response still relevant

**Performance:**
- ✅ No browser freeze
- ✅ UI remains responsive

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B4 - Irrelevant/Off-topic Questions (Error)

**Objective:** Test AI handling of questions unrelated to transcript

**Test Steps:**
1. Ask: "What's the weather today?"
2. Wait for response
3. Ask: "What is 2 + 2?"
4. Ask: "Tell me a joke"

**Expected Results:**

**AI Response:**
- ✅ AI politely declines to answer
- ✅ Response examples:
  - "I can only answer questions about the analyzed transcript"
  - "This question is not related to the meeting. Please ask about the transcript content."
- ✅ AI guides user back to topic
- ✅ Suggests relevant questions

**No Crash:**
- ✅ Application remains functional
- ✅ Can ask valid questions afterward
- ✅ Chat history preserved

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B5 - API Timeout (Network Error)

**Objective:** Test handling when API doesn't respond

**Test Steps:**
1. Disconnect internet (or block API endpoint)
2. Ask any question
3. Wait for timeout

**Expected Results:**

**Timeout Handling:**
- ✅ Loading indicator shows for 30 seconds
- ✅ Then error: "❌ Connection timeout"
- ✅ Detailed message: "Unable to reach AI service. Please check your internet connection."

**Retry Mechanism:**
- ✅ "🔄 Retry" button appears
- ✅ Clicking retry attempts request again
- ✅ Question preserved (no need to retype)

**User Guidance:**
- ✅ Troubleshooting tips:
  - Check internet connection
  - Check firewall settings
  - Try again in a few minutes
- ✅ Error logged (for debugging)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B6 - API Rate Limit Exceeded (Error)

**Objective:** Test handling when API rate limit hit

**Test Steps:**
1. Send 20 questions rapidly (< 1 minute)
2. Trigger rate limit error

**Expected Results:**

**Rate Limit Error:**
- ✅ Status: "⚠️ Rate limit exceeded"
- ✅ Message: "Too many requests. Please wait 60 seconds."
- ✅ Countdown timer: "Retry in: 59s, 58s, 57s..."

**UI State:**
- ✅ Send button disabled
- ✅ Input box disabled
- ✅ Countdown displayed prominently

**Auto-retry:**
- ✅ After countdown, UI re-enables
- ✅ Can send questions again
- ✅ Last question preserved (optional)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B7 - Malformed API Response (Error)

**Objective:** Test handling of invalid API response

**Test Steps:**
1. (Simulate malformed response from API)
2. Ask any question
3. Check error handling

**Expected Results:**

**Error Handling:**
- ✅ Error caught gracefully
- ✅ User-friendly message: "❌ Error processing response"
- ✅ Technical details hidden (or in collapsible section)
- ✅ No crash or blank screen

**Recovery:**
- ✅ Can try asking again
- ✅ Chat history preserved
- ✅ Application remains functional

**Logging:**
- ✅ Error logged to console (for debugging)
- ✅ Error details available for support

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.B8 - Special Characters & Emojis in Question

**Objective:** Test handling of special characters

**Test Steps:**
1. Ask question with special characters: "What about the 🎯 goals & objectives? (e.g., Q1 targets)"
2. Ask with code: "Did they discuss `React.useState()` hook?"
3. Ask with math: "What about the 50% increase?"

**Expected Results:**

**Character Handling:**
- ✅ All characters preserved in question
- ✅ Emojis display correctly: 🎯 ✅ 📊
- ✅ Special chars: & ( ) [ ] { } < > @ # $ %
- ✅ Code formatting: `backticks` preserved
- ✅ Math symbols: + - × ÷ = %

**Response:**
- ✅ AI understands question correctly
- ✅ Response relevant
- ✅ No encoding errors

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## SECTION C: UI/UX VALIDATION

### TC_03.C1 - Chat Interface Layout

**Objective:** Validate chat interface design and layout

**Test Steps:**
1. Open Chat tab
2. Send several messages
3. Check layout and styling

**Expected Results:**

**Layout:**
- ✅ User messages: Right-aligned, blue background
- ✅ AI messages: Left-aligned, gray background
- ✅ Clear visual distinction between user/AI
- ✅ Avatars/icons (optional): User icon, AI icon

**Message Bubbles:**
- ✅ Rounded corners
- ✅ Padding: 12px 16px
- ✅ Max width: 70% of container
- ✅ Proper spacing between messages (8px)

**Typography:**
- ✅ Readable font size (14-16px)
- ✅ Line height: 1.5
- ✅ High contrast text
- ✅ Markdown rendered (bold, italic, lists)

**Scrolling:**
- ✅ Chat container scrollable
- ✅ Auto-scroll to latest message
- ✅ Smooth scrolling
- ✅ Scroll bar styled (not default)

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C2 - Input Box Behavior

**Objective:** Validate input box functionality

**Test Steps:**
1. Click input box
2. Type text
3. Test multi-line input
4. Test keyboard shortcuts

**Expected Results:**

**Input Box:**
- ✅ Placeholder text: "Ask a question about the transcript..."
- ✅ Focus border: Blue highlight
- ✅ Auto-resize for multi-line (up to 5 lines)
- ✅ Scrollable if exceeds max height

**Keyboard Shortcuts:**
- ✅ Enter: Send message
- ✅ Shift+Enter: New line
- ✅ Ctrl+A: Select all
- ✅ Escape: Clear input (optional)

**Character Counter:**
- ✅ Shows character count (optional)
- ✅ Warning if approaching limit
- ✅ Format: "250 / 5000"

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C3 - Send Button States

**Objective:** Validate send button behavior

**Test Steps:**
1. Check button in different states
2. Test interactions

**Expected Results:**

**Default State:**
- ✅ Icon: 📤 or paper plane
- ✅ Background: Blue gradient
- ✅ Cursor: pointer
- ✅ Enabled

**Hover State:**
- ✅ Slightly darker blue
- ✅ Lift effect
- ✅ Smooth transition

**Disabled State:**
- ✅ Gray background
- ✅ Cursor: not-allowed
- ✅ Opacity: 0.5
- ✅ When: Empty input or processing

**Loading State:**
- ✅ Spinner icon
- ✅ Text: "Sending..." (optional)
- ✅ Disabled
- ✅ Pulsing animation

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C4 - Suggested Question Buttons

**Objective:** Validate suggested button styling and behavior

**Test Steps:**
1. Check button layout
2. Test hover effects
3. Test click behavior

**Expected Results:**

**Button Layout:**
- ✅ Displayed in row or grid
- ✅ Wrapped if screen narrow
- ✅ Equal spacing (8px gap)
- ✅ Responsive on mobile

**Button Styling:**
- ✅ Rounded corners (full rounded)
- ✅ Border: 1px solid
- ✅ Background: White or light gray
- ✅ Icon + text
- ✅ Padding: 8px 16px

**Hover Effect:**
- ✅ Background color change
- ✅ Border color change
- ✅ Slight scale up (1.05)
- ✅ Smooth transition

**Click Feedback:**
- ✅ Button press animation
- ✅ Ripple effect (optional)
- ✅ Disabled during processing

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C5 - Clear History Button

**Objective:** Validate clear history functionality

**Preconditions:**
- Chat history exists (5+ messages)

**Test Steps:**
1. Locate "🗑️ Clear history" button
2. Click button
3. Confirm action (if prompt appears)

**Expected Results:**

**Confirmation:**
- ✅ Confirmation dialog appears: "Are you sure you want to clear chat history?"
- ✅ Options: "Clear" and "Cancel"
- ✅ Warning icon

**Clear Operation:**
- ✅ All messages removed from chat
- ✅ Chat area shows: "No messages yet"
- ✅ Suggested buttons still visible
- ✅ Input box ready for new question

**No Data Loss:**
- ✅ Transcript data preserved
- ✅ Can start new chat immediately
- ✅ No errors

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C6 - Loading Indicator

**Objective:** Validate AI thinking/loading indicator

**Test Steps:**
1. Send a question
2. Observe loading indicator
3. Check animation

**Expected Results:**

**Indicator Display:**
- ✅ Appears immediately after sending
- ✅ Message: "🤔 AI is thinking..." or "Typing..."
- ✅ Position: Left-aligned (AI side)

**Animation:**
- ✅ Three dots bouncing animation
- ✅ Or spinner animation
- ✅ Smooth, not distracting
- ✅ Loops continuously

**Timing:**
- ✅ Shows for entire processing duration
- ✅ Disappears when response arrives
- ✅ Smooth transition to response

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C7 - Timestamp Display

**Objective:** Validate message timestamps

**Test Steps:**
1. Send multiple messages at different times
2. Check timestamp format

**Expected Results:**

**Timestamp Format:**
- ✅ Format: "[HH:MM]" or "HH:MM AM/PM"
- ✅ Example: "[14:30]" or "2:30 PM"
- ✅ Displayed for each message
- ✅ Position: Below or beside message

**Styling:**
- ✅ Small font size (11-12px)
- ✅ Gray color (low emphasis)
- ✅ Doesn't distract from message

**Accuracy:**
- ✅ Correct time for each message
- ✅ Updates in real-time
- ✅ Timezone consistent

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C8 - Markdown Rendering

**Objective:** Validate markdown formatting in responses

**Test Steps:**
1. Ask question that triggers formatted response
2. Check markdown rendering

**Expected Results:**

**Supported Markdown:**
- ✅ **Bold text** renders correctly
- ✅ *Italic text* renders correctly
- ✅ `Code inline` with monospace font
- ✅ Numbered lists (1. 2. 3.)
- ✅ Bullet lists (- or *)
- ✅ Headings (# ## ###)
- ✅ Links (if applicable)

**Rendering Quality:**
- ✅ Proper spacing between elements
- ✅ Lists indented correctly
- ✅ Code blocks with background
- ✅ Readable and professional

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.C9 - Responsive Design

**Objective:** Validate chat interface on different screen sizes

**Test Steps:**
1. Test on desktop (1920x1080)
2. Test on tablet (768x1024)
3. Test on mobile (375x667)

**Expected Results:**

**Desktop:**
- ✅ Full width chat area
- ✅ Suggested buttons in row
- ✅ Comfortable spacing

**Tablet:**
- ✅ Chat area adapts to width
- ✅ Buttons may wrap to 2 rows
- ✅ Still readable and usable

**Mobile:**
- ✅ Chat bubbles max 90% width
- ✅ Buttons stack vertically or wrap
- ✅ Input box full width
- ✅ Touch-friendly button sizes (44px min)
- ✅ No horizontal scroll

**Actual Result:**
- [ ] Pass (Desktop)
- [ ] Pass (Tablet)
- [ ] Pass (Mobile)
- [ ] Fail

**Notes:**


---

## SECTION D: PERFORMANCE & EDGE CASES

### TC_03.D1 - Rapid Question Sending

**Objective:** Test sending multiple questions quickly

**Test Steps:**
1. Send 5 questions rapidly (1 per second)
2. Monitor responses

**Expected Results:**

**Queueing:**
- ✅ All questions queued properly
- ✅ Responses arrive in order
- ✅ No questions lost
- ✅ No duplicate responses

**Performance:**
- ✅ UI remains responsive
- ✅ No lag or freeze
- ✅ Each response displays correctly

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

### TC_03.D2 - Long Chat Session (50+ Messages)

**Objective:** Test performance with extensive chat history

**Test Steps:**
1. Send 50+ questions and receive responses
2. Monitor performance

**Expected Results:**

**Performance:**
- ✅ Scrolling remains smooth
- ✅ No memory leaks
- ✅ Response time consistent
- ✅ UI not sluggish

**Memory:**
- ✅ Memory usage < 500MB
- ✅ No browser warnings

**Actual Result:**
- [ ] Pass
- [ ] Fail

**Notes:**


---

## Test Execution Summary

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Normal Cases | 4 | 0 | 0 | 0 |
| Abnormal Cases | 8 | 0 | 0 | 0 |
| UI/UX Validation | 9 | 0 | 0 | 0 |
| Performance | 2 | 0 | 0 | 0 |
| **TOTAL** | **23** | **0** | **0** | **0** |

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

