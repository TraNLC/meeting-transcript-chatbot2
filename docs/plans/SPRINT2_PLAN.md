# 🚀 Sprint 2 Plan - Advanced Chatbot Systems

**Workshop Date**: Saturday, November 23, 2025  
**Duration**: 8 hours (9 AM - 6 PM)  
**Format**: Virtual via MS Teams  
**Team**: Team 3 - Akatsuki (5 active participants)

---

## 📋 Workshop 2 Requirements

### 🎯 Goal
Collaboratively design, implement, and test advanced multi-turn chatbot systems using OpenAI SDK with:
- Chat completion
- Function calling
- Batching
- Conversation management
- Advanced prompting (few-shot, chain-of-thought)

### ✅ Deliverables (8 hours)
1. **Problem definition** + mock data schema
2. **Prompt templates** (few-shot & chain-of-thought)
3. **Working chatbot** (OpenAI SDK)
4. **Conversation logs** (multi-turn dialogue)
5. **Team presentation** (demo + insights)

---

## ⏰ Workshop Schedule

### Hour 1-2 (9:00 AM - 11:00 AM): Problem Definition & Design
**Goal**: Define problem, design solution, plan implementation

#### Activities:
- [ ] Team introduction & role assignment (15 mins)
- [ ] Brainstorm real-world problem scenarios (30 mins)
  - HR: Employee onboarding assistant
  - Sales: Customer inquiry chatbot
  - IT: Technical support assistant
  - Finance: Expense report analyzer
- [ ] Select problem to solve - team vote (15 mins)
- [ ] Define mock data schema (30 mins)
- [ ] Design conversation flow diagram (30 mins)

**Deliverable**: Problem definition document + mock data schema

---

### Hour 3-4 (11:00 AM - 1:00 PM): Prompt Engineering & Setup
**Goal**: Create prompt templates and setup OpenAI SDK

#### Activities:
- [ ] Design system message (20 mins)
- [ ] Create few-shot examples (40 mins)
- [ ] Design chain-of-thought prompts (40 mins)
- [ ] Setup OpenAI SDK environment (20 mins)

**Deliverable**: Prompt templates library

**Break**: 1:00 PM - 2:00 PM (Lunch)

---

### Hour 5-6 (2:00 PM - 4:00 PM): Core Implementation
**Goal**: Implement chatbot with conversation management

#### Activities:
- [ ] Implement chat completion (30 mins)
- [ ] Add conversation history (30 mins)
- [ ] Implement message management (30 mins)
- [ ] Test multi-turn conversations (30 mins)

**Deliverable**: Working multi-turn chatbot

---

### Hour 7 (4:00 PM - 5:00 PM): Function Calling Implementation
**Goal**: Add function calling capabilities

#### Activities:
- [ ] Define function schemas (15 mins)
- [ ] Implement function executor (20 mins)
- [ ] Create 2-3 example functions (15 mins)
- [ ] Test function calling flow (10 mins)

**Deliverable**: Function calling working

---

### Hour 8 (5:00 PM - 6:00 PM): Testing & Presentation
**Goal**: Test, document, and present

#### Activities:
- [ ] End-to-end testing (15 mins)
- [ ] Generate conversation logs (10 mins)
- [ ] Prepare presentation slides (15 mins)
- [ ] Practice demo (10 mins)
- [ ] Team presentation (10 mins)

**Deliverable**: Complete presentation with demo

---

## 📅 Pre-Workshop Prep (Nov 17-22)

### Technical Setup
- [ ] Azure OpenAI credentials
- [ ] OpenAI SDK installed
- [ ] Test chat completion
- [ ] Development environment ready

### Knowledge Prep
- [ ] Read OpenAI API docs
- [ ] Study function calling guide
- [ ] Review conversation patterns
- [ ] Learn few-shot & chain-of-thought

### Code Templates
- [ ] Chat completion template
- [ ] Conversation manager
- [ ] Function calling framework
- [ ] Prompt templates library

### Workshop Materials
- [ ] Problem scenario ideas
- [ ] Mock data templates
- [ ] Presentation template
- [ ] Demo script outline

---

## 👥 Workshop Day Team Roles (5 members)

### Role 1: Team Lead & Presenter
**Responsibilities**:
- Coordinate team activities
- Time management
- Final presentation
- Demo coordination

### Role 2: Problem Designer
**Responsibilities**:
- Define real-world problem
- Create mock data schema
- Design conversation scenarios
- Document requirements

### Role 3: Prompt Engineer
**Responsibilities**:
- Design prompt templates
- Few-shot examples
- Chain-of-thought reasoning
- System message optimization

### Role 4: Backend Developer
**Responsibilities**:
- OpenAI SDK implementation
- Function calling logic
- Conversation management
- Message handling

### Role 5: QA & Documentation
**Responsibilities**:
- Test conversation flows
- Document code
- Capture conversation logs
- Prepare insights & lessons learned

---

## 👥 Pre-Workshop Team Assignment (7 members)

### Member 1 - Project Lead
- Setup Azure OpenAI credentials
- Coordinate pre-workshop prep
- Prepare demo environment

### Member 2 - OpenAI Specialist
- Study OpenAI SDK documentation
- Test chat completion API
- Prepare code templates

### Member 3 - Backend Engineer
- Setup conversation management structure
- Prepare message handling code
- Test multi-turn logic

### Member 4 - AI Engineer
- Design function calling framework
- Prepare function schemas
- Create example functions

### Member 5 - Frontend Engineer
- Prepare UI for demo
- Test conversation display
- Setup export functionality

### Member 6 - QA Engineer
- Prepare test cases
- Setup testing framework
- Document test scenarios

### Member 7 - Tech Writer
- Prepare presentation template
- Document setup process
- Create demo script template

---

## � Keey Technical Components

### 1. OpenAI Chat Completion
```python
from openai import OpenAI
client = OpenAI(api_key="...")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are..."},
        {"role": "user", "content": "Question"}
    ]
)
```

### 2. Conversation Management
```python
conversation = [
    {"role": "system", "content": "System message"},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "AI response"}
]
```

### 3. Function Calling
```python
functions = [{
    "name": "get_action_items",
    "description": "Get action items",
    "parameters": {
        "type": "object",
        "properties": {
            "assignee": {"type": "string"}
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    functions=functions
)
```

---

## 🎯 Workshop Demo Scenario

### Problem: Intelligent Meeting Assistant

**Scenario**: HR department needs to analyze meeting transcripts and extract insights

**Mock Data**: 
- 5 sample meeting transcripts (team meetings, 1-on-1s, all-hands)
- Participants, timestamps, action items, decisions

**Demo Flow**:
1. Upload meeting transcript
2. Ask questions about the meeting (multi-turn)
3. Use function calling to get specific data
4. Show conversation history
5. Export conversation log

**Example Conversation**:
```
User: "What was discussed in this meeting?"
Assistant: [Summary using chat completion]

User: "Who attended?"
Assistant: [Calls get_meeting_participants() function]

User: "What are Alice's action items?"
Assistant: [Calls get_action_items(assignee="Alice")]

User: "Search for 'budget' in the transcript"
Assistant: [Calls search_transcript(keyword="budget")]
```

---

## 📊 Success Criteria

### Technical
- [ ] Multi-provider LLM support working
- [ ] Conversation history maintained across turns
- [ ] Function calling working reliably
- [ ] Batching reduces API costs by >30%
- [ ] All tests passing (>80% coverage)

### Workshop
- [ ] Clear problem definition
- [ ] Working demo (no crashes)
- [ ] Multi-turn conversation demonstrated
- [ ] Function calling demonstrated
- [ ] Team presentation <10 minutes
- [ ] Q&A handled confidently

### Code Quality
- [ ] Clean architecture
- [ ] Well-documented code
- [ ] Error handling
- [ ] Type hints
- [ ] Unit tests

---

## 📚 Resources

### Documentation
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Llama 3 Guide](https://llama.meta.com/)

### Code Examples
- OpenAI Cookbook: https://github.com/openai/openai-cookbook
- Function calling examples
- Conversation management patterns

---

## 🚨 Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API costs too high | High | Implement caching, batching |
| Function calling complex | Medium | Start simple, iterate |
| Time constraint | High | Focus on core features first |
| Integration issues | Medium | Test early and often |
| Workshop demo fails | High | Practice multiple times, have backup |

---

**Last Updated**: November 10, 2025  
**Next Review**: November 17, 2025 (Sprint 2 Start)


---

## ✅ Pre-Workshop Checklist

### Technical
- [ ] Azure OpenAI credentials
- [ ] OpenAI SDK installed
- [ ] Test chat completion
- [ ] Demo environment ready

### Knowledge
- [ ] Read OpenAI docs
- [ ] Study function calling
- [ ] Learn few-shot prompting
- [ ] Understand chain-of-thought

### Materials
- [ ] Code templates ready
- [ ] Mock data prepared
- [ ] Presentation template
- [ ] Demo script

---

## 🎯 Success Criteria

### Technical
- [ ] Working chatbot (OpenAI SDK)
- [ ] Multi-turn conversation
- [ ] Function calling (2-3 functions)
- [ ] Conversation logs

### Presentation
- [ ] Clear problem definition
- [ ] Live demo successful
- [ ] Insights shared
- [ ] Q&A handled

---

## 💡 Tips

- ⏰ Stick to schedule
- 👥 Clear roles
- 💻 Test frequently
- 🎤 Practice demo

## 🚨 Avoid

- ❌ API rate limits
- ❌ Over-engineering
- ❌ Unclear roles
- ❌ No testing

---

**Workshop**: Saturday, Nov 23, 2025 | 9 AM - 6 PM | MS Teams  
**Team**: Team 3 - Akatsuki 🔥
