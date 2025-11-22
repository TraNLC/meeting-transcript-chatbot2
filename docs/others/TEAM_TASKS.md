# 👥 Team Task Assignment - Meeting Transcript Chatbot

## 📅 Sprint 1 Timeline
**Session**: Session 1 - Python & OpenAI API  
**Timeline**: November 10-14, 2025 (5 days)  
**Workshop**: Saturday, Nov 15, 2025 (1.5 hours)  
**Team Size**: 7 members  
**Related Assignment**: Assignment 03 - AI-Powered Meeting Summarizer

---

## 🎯 Sprint 1 Goals
✅ Hoàn thành chatbot cơ bản với Gemini API  
✅ Xử lý transcript và phân tích thông tin  
✅ Giao diện Gradio đầy đủ chức năng  
✅ Export kết quả (TXT/DOCX)  
✅ Unit tests & documentation

---

## 👤 Team Member Assignments

### 1️⃣ Member 1: Project Lead & Configuration
**Role**: Tech Lead / DevOps  
**Responsibilities**: Setup project, configuration, deployment

#### Tasks:
- [x] ✅ Setup project structure
- [x] ✅ Configure environment (.env, .gitignore)
- [x] ✅ Setup dependencies (requirements.txt)
- [ ] 📝 Create deployment scripts (run.bat, run.sh)
- [ ] 📝 Setup CI/CD (GitHub Actions - optional)
- [ ] 📝 Write deployment documentation
- [ ] 🧪 Integration testing
- [ ] 📊 Performance monitoring setup

**Deliverables**:
- ✅ Working project structure
- ✅ Configuration files
- 📝 Deployment guide
- 📝 CI/CD pipeline (optional)

**Estimated Time**: 8-10 hours  
**Priority**: HIGH

---

### 2️⃣ Member 2: LLM Integration Specialist
**Role**: AI/ML Engineer  
**Responsibilities**: LLM API integration, prompt engineering

#### Tasks:
- [x] ✅ Implement Gemini API client (`src/llm/chat_model.py`)
- [x] ✅ Design prompt templates (`src/llm/prompts.py`)
- [ ] 🔄 Optimize prompts for better accuracy
- [ ] 🔄 Add error handling & retry logic
- [ ] 🔄 Implement rate limiting
- [ ] 🔄 Add response validation
- [ ] 🧪 Test with various transcript formats
- [ ] 📝 Document prompt engineering decisions

**Deliverables**:
- ✅ LLM Manager module
- ✅ Prompt templates (5 languages)
- 🔄 Optimized prompts
- 📝 API usage documentation

**Estimated Time**: 10-12 hours  
**Priority**: HIGH

---

### 3️⃣ Member 3: Data Processing Engineer
**Role**: Backend Engineer  
**Responsibilities**: File loading, text preprocessing

#### Tasks:
- [x] ✅ Implement file loader (`src/data/loader.py`)
  - [x] Support TXT files
  - [x] Support DOCX files
- [x] ✅ Implement text preprocessor (`src/data/preprocessor.py`)
  - [x] Text cleaning
  - [x] Text truncation
- [ ] 🔄 Add more file format support (PDF, CSV)
- [ ] 🔄 Improve text cleaning logic
- [ ] 🔄 Add text validation
- [ ] 🧪 Write unit tests for data modules
- [ ] 📝 Document data processing pipeline

**Deliverables**:
- ✅ TranscriptLoader class
- ✅ TranscriptPreprocessor class
- 🔄 Extended file format support
- 🧪 Unit tests (>80% coverage)

**Estimated Time**: 8-10 hours  
**Priority**: MEDIUM

---

### 4️⃣ Member 4: RAG & Chatbot Logic
**Role**: AI Engineer  
**Responsibilities**: Chatbot core logic, information extraction

#### Tasks:
- [x] ✅ Implement Chatbot class (`src/rag/chatbot.py`)
- [x] ✅ Summary generation
- [x] ✅ Action items extraction
- [x] ✅ Decisions extraction
- [x] ✅ Topics extraction
- [ ] 🔄 Add Q&A functionality
- [ ] 🔄 Improve JSON parsing logic
- [ ] 🔄 Add conversation history
- [ ] 🧪 Test extraction accuracy
- [ ] 📝 Document chatbot architecture

**Deliverables**:
- ✅ Chatbot module
- ✅ 4 extraction functions
- 🔄 Q&A feature
- 📝 Architecture documentation

**Estimated Time**: 10-12 hours  
**Priority**: HIGH

---

### 5️⃣ Member 5: UI/UX Developer
**Role**: Frontend Engineer  
**Responsibilities**: Gradio interface, user experience

#### Tasks:
- [x] ✅ Design Gradio layout (`src/ui/gradio_app.py`)
- [x] ✅ Implement file upload
- [x] ✅ Display analysis results
- [x] ✅ Export functionality (TXT/DOCX)
- [ ] 🔄 Improve UI/UX design
- [ ] 🔄 Add loading indicators
- [ ] 🔄 Add error messages (user-friendly)
- [ ] 🔄 Add language selector (optional)
- [ ] 🔄 Responsive design improvements
- [ ] 📝 Create user guide with screenshots

**Deliverables**:
- ✅ Gradio interface
- ✅ Export features
- 🔄 Improved UX
- 📝 User guide

**Estimated Time**: 8-10 hours  
**Priority**: MEDIUM

---

### 6️⃣ Member 6: QA Engineer & Tester
**Role**: Quality Assurance  
**Responsibilities**: Testing, bug fixing, quality control

#### Tasks:
- [ ] 🧪 Write unit tests (`tests/`)
  - [ ] Test data loader
  - [ ] Test preprocessor
  - [ ] Test LLM integration
  - [ ] Test chatbot logic
- [ ] 🧪 Integration testing
- [ ] 🧪 End-to-end testing
- [ ] 🐛 Bug tracking & fixing
- [ ] 📊 Test coverage report
- [ ] 📝 Create test documentation
- [ ] ✅ Quality checklist

**Deliverables**:
- 🧪 Test suite (>80% coverage)
- 🐛 Bug report & fixes
- 📊 Test coverage report
- 📝 Testing documentation

**Estimated Time**: 10-12 hours  
**Priority**: HIGH

---

### 7️⃣ Member 7: Documentation & Support
**Role**: Technical Writer  
**Responsibilities**: Documentation, README, guides

#### Tasks:
- [x] ✅ Write README.md
- [x] ✅ Create SPRINTS.md
- [ ] 📝 Write API documentation
- [ ] 📝 Create user guide (Vietnamese & English)
- [ ] 📝 Write developer guide
- [ ] 📝 Create troubleshooting guide
- [ ] 📝 Add code comments & docstrings
- [ ] 📝 Create demo video/GIF
- [ ] 📝 Prepare presentation slides

**Deliverables**:
- ✅ README.md
- ✅ SPRINTS.md
- 📝 Complete documentation set
- 📝 User & developer guides
- 📝 Demo materials

**Estimated Time**: 8-10 hours  
**Priority**: MEDIUM

---

## 📊 Task Status Legend
- ✅ **Completed** - Task hoàn thành
- 🔄 **In Progress** - Đang làm
- 📝 **Planned** - Đã lên kế hoạch
- 🧪 **Testing** - Đang test
- 🐛 **Bug Fix** - Sửa lỗi
- 📊 **Review** - Đang review

---

## 🔄 Daily Standup Format

**Time**: 9:00 AM daily (15 minutes)  
**Update Kanban Board**: Move tasks between columns

### Template for Each Member:
```
Member X - [Role]
✅ Yesterday: [Completed tasks]
🎯 Today: [Planned tasks]
🚧 Blockers: [Issues/dependencies]
📊 Progress: [X%]
```

### Example:
```
Member 2 - LLM Specialist
✅ Yesterday: 
  - Implemented Gemini API client
  - Created prompt templates
🎯 Today:
  - Add error handling & retry logic
  - Optimize prompts for accuracy
🚧 Blockers:
  - Need API rate limit info from Member 1
📊 Progress: 29% → Target 50% by EOD
```

### Daily Standup Log

#### Day 1 - Nov 10 (Sunday)
- ✅ Foundation setup complete
- ✅ 18/40 tasks done (60% foundation)
- 🎯 Tomorrow: Focus on IN PROGRESS tasks

#### Day 2 - Nov 11 (Monday)
- [ ] Update after standup

#### Day 3 - Nov 12 (Tuesday)
- [ ] Update after standup

#### Day 4 - Nov 13 (Wednesday)
- [ ] Update after standup

#### Day 5 - Nov 14 (Thursday)
- [ ] Final review & demo prep

---

## 📅 Sprint 1 Milestones

### Day 1 (Nov 10 - Sunday): Foundation ✅
- [x] Project setup
- [x] Core modules implementation
- [x] Basic Gradio UI
- [x] Initial commit to GitHub

### Day 2-3 (Nov 11-12 - Mon-Tue): Features 🔄
- [ ] Complete all extraction features
- [ ] Improve prompts
- [ ] Add export functionality (TXT/DOCX)
- [ ] Error handling & validation

### Day 4 (Nov 13 - Wed): Testing & Polish 📝
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Bug fixes
- [ ] Code review
- [ ] Documentation updates

### Day 5 (Nov 14 - Thu): Final Preparation 🚀
- [ ] Final testing
- [ ] Performance optimization
- [ ] Demo preparation
- [ ] Sprint review meeting
- [ ] Prepare for Quiz 01

### Day 6 (Nov 15 - Sat): Workshop & Assessment 🎓
- [ ] Attend Workshop 1 (1.5 hours)
- [ ] Complete Quiz 01 (15 mins)
- [ ] Mock Interview 1 (10-15 mins)
- [ ] Sprint retrospective

---

## 🎯 Definition of Done (DoD)

### Code Quality
- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] No hardcoded values (use config)
- [ ] Error handling implemented
- [ ] Type hints added

### Testing
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passed
- [ ] Manual testing completed
- [ ] No critical bugs

### Documentation
- [ ] README updated
- [ ] API documentation complete
- [ ] Code comments added
- [ ] User guide available

### Deployment
- [ ] Runs on local machine
- [ ] Environment setup documented
- [ ] Dependencies listed
- [ ] Demo ready

---

## 🚨 Risk Management

### High Priority Risks
1. **API Rate Limits**
   - Risk: Gemini API có giới hạn 15 requests/minute
   - Mitigation: Implement rate limiting, caching
   - Owner: Member 2

2. **Large File Processing**
   - Risk: Transcript quá dài (>15k chars)
   - Mitigation: Text truncation, chunking
   - Owner: Member 3

3. **JSON Parsing Errors**
   - Risk: LLM không trả về đúng JSON format
   - Mitigation: Robust parsing, fallback logic
   - Owner: Member 4

4. **Testing Coverage**
   - Risk: Không đủ thời gian viết tests
   - Mitigation: Prioritize critical paths
   - Owner: Member 6

---

## 📞 Communication Channels

### Daily Updates
- **Time**: 9:00 AM daily
- **Duration**: 15 minutes
- **Platform**: Discord/Slack/Teams

### Code Review
- **Process**: Pull Request → Review → Merge
- **Reviewers**: At least 1 other member
- **Timeline**: Within 24 hours

### Issue Tracking
- **Platform**: GitHub Issues
- **Labels**: bug, feature, documentation, question
- **Priority**: high, medium, low

---

## 🎉 Sprint 1 Success Criteria

### Must Have (P0)
- [x] ✅ Gemini API integration working
- [x] ✅ File upload & processing
- [x] ✅ Summary generation
- [x] ✅ Action items extraction
- [x] ✅ Basic Gradio UI
- [ ] 📝 Export to TXT/DOCX

### Should Have (P1)
- [ ] 🔄 Topics extraction
- [ ] 🔄 Decisions extraction
- [ ] 🔄 Error handling
- [ ] 🔄 Unit tests (>50% coverage)
- [ ] 🔄 Basic documentation

### Nice to Have (P2)
- [ ] 📝 Q&A functionality
- [ ] 📝 Multi-language support
- [ ] 📝 Advanced UI features
- [ ] 📝 CI/CD pipeline
- [ ] 📝 Demo video

---

## 📊 Kanban Board - Sprint 1

### 📋 TODO (Not Started)
- [ ] Member 1: Create deployment scripts (run.bat, run.sh)
- [ ] Member 1: Setup CI/CD pipeline
- [ ] Member 2: Optimize prompts for accuracy
- [ ] Member 2: Add rate limiting
- [ ] Member 3: Add PDF/CSV support
- [ ] Member 3: Improve text cleaning
- [ ] Member 4: Add Q&A functionality
- [ ] Member 4: Add conversation history
- [ ] Member 5: Improve UI/UX design
- [ ] Member 5: Add loading indicators
- [ ] Member 6: Write all unit tests
- [ ] Member 6: Integration testing
- [ ] Member 7: Write API documentation
- [ ] Member 7: Create user guide

### 🔄 IN PROGRESS (Current Work)
- [ ] Member 2: Add error handling & retry logic
- [ ] Member 2: Add response validation
- [ ] Member 3: Add text validation
- [ ] Member 4: Improve JSON parsing logic
- [ ] Member 5: Add error messages (user-friendly)
- [ ] Member 7: Add code comments & docstrings

### 👀 REVIEW (Waiting for Review)
- [ ] (None yet - will add after PRs)

### ✅ DONE (Completed)
- [x] Member 1: Setup project structure
- [x] Member 1: Configure environment (.env, .gitignore)
- [x] Member 1: Setup dependencies (requirements.txt)
- [x] Member 2: Implement Gemini API client
- [x] Member 2: Design prompt templates (5 languages)
- [x] Member 3: Implement file loader (TXT/DOCX)
- [x] Member 3: Implement text preprocessor
- [x] Member 4: Implement Chatbot class
- [x] Member 4: Summary generation
- [x] Member 4: Action items extraction
- [x] Member 4: Decisions extraction
- [x] Member 4: Topics extraction
- [x] Member 5: Design Gradio layout
- [x] Member 5: Implement file upload
- [x] Member 5: Display analysis results
- [x] Member 5: Export functionality (TXT/DOCX)
- [x] Member 7: Write README.md
- [x] Member 7: Create SPRINTS.md

---

## 📈 Progress Tracking

### Overall Sprint 1 Progress: 60% ✅

| Member | Role | TODO | In Progress | Done | Total | Progress |
|--------|------|------|-------------|------|-------|----------|
| Member 1 | Project Lead | 2 | 0 | 3 | 5 | 60% 🟢 |
| Member 2 | LLM Specialist | 2 | 3 | 2 | 7 | 29% 🟡 |
| Member 3 | Data Engineer | 2 | 2 | 2 | 6 | 33% 🟡 |
| Member 4 | RAG Engineer | 2 | 1 | 5 | 8 | 63% 🟢 |
| Member 5 | UI/UX Dev | 2 | 1 | 4 | 7 | 57% 🟢 |
| Member 6 | QA Tester | 2 | 0 | 0 | 2 | 0% 🔴 |
| Member 7 | Tech Writer | 2 | 1 | 2 | 5 | 40% 🟡 |
| **TOTAL** | | **14** | **8** | **18** | **40** | **60%** |

**Last Updated**: November 10, 2025 - 20:00  
**Current Day**: Day 1 of Sprint 1  
**Days Remaining**: 4 days until deadline

### 🎯 Daily Goals
**Today (Nov 10)**: Foundation setup ✅  
**Tomorrow (Nov 11)**: Complete IN PROGRESS tasks, move 5 tasks to DONE  
**Nov 12**: Testing begins, Member 6 starts work  
**Nov 13**: Code review & bug fixes  
**Nov 14**: Final polish & demo prep

---

## 📚 Course Context

### Full Learning Path Timeline
- **Session 1**: Nov 10-14 → Python & OpenAI API
- **Session 2**: Nov 17-21 → OpenAI API & Llama 3
- **Session 3**: Nov 24-28 → Hugging Face & Embeddings
- **Session 4**: Dec 1-5 → Pinecone & LangChain
- **Session 5**: Dec 8-12 → RAG & LangGraph
- **Hackathon**: Dec 13 (8 hours)
- **Final Assessment**: Dec (70 mins)

### Sprint 1 Learning Objectives
**Python Basics:**
- Data types, Variables, Lists, Dictionaries
- Conditional statements, Loops
- Functions & Error handling

**OpenAI API:**
- API authentication & requests
- Text generation & Chat completions
- Prompt design & engineering
- Real-world applications

### Related Assignments (Reference)
1. Assignment 01: Command-Line Task Manager (Python)
2. Assignment 02: Automotive Prompt-Driven Agent
3. **Assignment 03: AI-Powered Meeting Summarizer** ⭐ (Our project!)

---

## 🔗 Useful Links

### Project Documentation
- **Project README**: [README.md](README.md)
- **Sprint Planning**: [SPRINTS.md](SPRINTS.md)
- **Daily Work Log**: [DAILY_LOG.md](DAILY_LOG.md) ⭐ Update daily!
- **Course Overview**: [COURSE_OVERVIEW.md](COURSE_OVERVIEW.md)

### External Resources
- **Repository**: https://github.com/TraNLC/meeting-transcript-chatbot2
- **Gemini API**: https://ai.google.dev/docs
- **OpenAI API**: https://platform.openai.com/docs
- **Gradio Docs**: https://gradio.app/docs

### 📝 Daily Update Process
1. **End of day**: Each member updates their section in DAILY_LOG.md
2. **Include**: Time log, completed tasks, in-progress, blockers, notes
3. **Team lead**: Summarizes team metrics
4. **Mentor**: Reviews and provides feedback

---

## 📝 Notes for Team

### Best Practices
1. **Commit often** - Small, focused commits
2. **Write tests** - Test as you code
3. **Document code** - Clear docstrings
4. **Ask for help** - Don't block yourself
5. **Review code** - Learn from each other

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature"

# Push and create PR
git push origin feature/your-feature-name
```

### Code Review Checklist
- [ ] Code works as expected
- [ ] Tests are included
- [ ] Documentation updated
- [ ] No security issues
- [ ] Follows style guide

---

**Good luck team! Let's build something amazing! 🚀**
