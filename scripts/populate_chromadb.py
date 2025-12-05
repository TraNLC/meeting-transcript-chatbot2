"""Populate ChromaDB with sample meeting data for demo.

This script adds sample meetings to ChromaDB so the search feature can be demonstrated.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.vectorstore.chroma_manager import ChromaManager
from datetime import datetime, timedelta

def populate_sample_data():
    """Add sample meetings to ChromaDB."""
    
    print("=" * 70)
    print("POPULATING CHROMADB WITH SAMPLE DATA")
    print("=" * 70)
    print()
    
    manager = ChromaManager()
    
    # Sample meetings data
    sample_meetings = [
        {
            "meeting_id": "demo_meeting_001",
            "transcript": """
Cuộc họp ngân sách Q4 2025

Chủ tọa: Nguyễn Văn A
Thành viên: Trần Thị B, Lê Văn C, Phạm Thị D

Nội dung:
1. Xem xét ngân sách marketing Q4
   - Đề xuất tăng 20% cho digital marketing
   - Phân bổ 500 triệu cho campaign Tết
   
2. Chi phí vận hành
   - Tiết kiệm 15% chi phí văn phòng
   - Đầu tư thêm vào infrastructure
   
3. Dự báo doanh thu
   - Mục tiêu: 10 tỷ trong Q4
   - Tăng trưởng 25% so với Q3
   
Quyết định:
- Phê duyệt ngân sách marketing 500 triệu
- Cắt giảm chi phí không cần thiết
- Họp lại vào 15/12 để review

Action items:
- Chuẩn bị báo cáo chi tiết (Trần Thị B, 10/12/2025)
- Liên hệ agency marketing (Lê Văn C, 12/12/2025)
            """,
            "analysis": {
                "summary": "Cuộc họp xem xét ngân sách Q4, quyết định tăng budget marketing và cắt giảm chi phí vận hành.",
                "topics": ["Ngân sách marketing", "Chi phí vận hành", "Dự báo doanh thu"],
                "action_items": [
                    {"task": "Chuẩn bị báo cáo chi tiết", "assignee": "Trần Thị B", "deadline": "10/12/2025"},
                    {"task": "Liên hệ agency marketing", "assignee": "Lê Văn C", "deadline": "12/12/2025"}
                ]
            },
            "metadata": {
                "meeting_type": "meeting",
                "language": "vi",
                "timestamp": (datetime.now() - timedelta(days=5)).isoformat()
            }
        },
        {
            "meeting_id": "demo_workshop_001",
            "transcript": """
Workshop: Python Programming Basics

Giảng viên: Trần Văn Khoa
Học viên: 15 người

Nội dung:
1. Giới thiệu Python
   - Cài đặt Python và IDE
   - Syntax cơ bản
   
2. Data Types
   - String, Integer, Float, Boolean
   - Lists, Tuples, Dictionaries
   
3. Control Flow
   - If/else statements
   - For và while loops
   
4. Functions
   - Định nghĩa function
   - Parameters và return values
   
Bài tập:
- Viết function tính tổng các số trong list
- Tạo dictionary quản lý thông tin sinh viên
- Xử lý file text với Python

Q&A:
Q: Python khác gì JavaScript?
A: Python dùng indentation, JS dùng brackets. Python backend-focused, JS frontend-focused.

Q: Học Python mất bao lâu?
A: Cơ bản 2-3 tháng, thành thạo 6-12 tháng.
            """,
            "analysis": {
                "summary": "Workshop Python cơ bản, cover syntax, data types, control flow và functions.",
                "topics": ["Python basics", "Data types", "Control flow", "Functions"],
                "action_items": [
                    {"task": "Hoàn thành bài tập về functions", "assignee": "All students", "deadline": "05/12/2025"}
                ]
            },
            "metadata": {
                "meeting_type": "workshop",
                "language": "vi",
                "timestamp": (datetime.now() - timedelta(days=3)).isoformat()
            }
        },
        {
            "meeting_id": "demo_brainstorm_001",
            "transcript": """
Brainstorming: Tính năng mới cho Mobile App

Facilitator: Lê Thị Mai
Team: Product (3), Design (2), Engineering (4)

Ideas:
1. Dark mode - tiết kiệm pin, dễ nhìn ban đêm
2. Offline mode - dùng được khi không có mạng
3. Voice search - tìm kiếm bằng giọng nói
4. AR try-on - thử đồ bằng camera
5. Social sharing - chia sẻ lên mạng xã hội
6. Push notifications - thông báo real-time
7. Chatbot support - hỗ trợ 24/7
8. Loyalty program - tích điểm đổi quà

Voting:
- Dark mode: 8 votes ⭐
- Offline mode: 7 votes ⭐
- Chatbot: 6 votes
- Voice search: 5 votes

Concerns:
- Dark mode cần redesign toàn bộ UI
- Offline mode phức tạp về database sync
- AR try-on cần nhiều resources

Quyết định:
- Implement dark mode trong Q1 2026
- Research offline mode cho Q2
- Chatbot dùng solution có sẵn

Action items:
- Design dark mode mockups (Design team, 20/12/2025)
- Research offline solutions (Engineering, 15/12/2025)
- Evaluate chatbot vendors (Product, 18/12/2025)
            """,
            "analysis": {
                "summary": "Brainstorming tính năng mobile app, chọn dark mode và offline mode làm priority.",
                "topics": ["Dark mode", "Offline mode", "Chatbot", "Voice search"],
                "action_items": [
                    {"task": "Design dark mode mockups", "assignee": "Design team", "deadline": "20/12/2025"},
                    {"task": "Research offline solutions", "assignee": "Engineering", "deadline": "15/12/2025"}
                ]
            },
            "metadata": {
                "meeting_type": "brainstorming",
                "language": "vi",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
            }
        },
        {
            "meeting_id": "demo_meeting_002",
            "transcript": """
Sprint Planning Meeting - Sprint 15

Scrum Master: Phạm Văn Hùng
Team: 6 developers, 2 QA

Sprint Goal: Complete payment integration and user profile features

Stories:
1. Payment Gateway Integration (13 points)
   - Integrate VNPay
   - Integrate Momo
   - Handle payment callbacks
   
2. User Profile Enhancement (8 points)
   - Add avatar upload
   - Edit profile information
   - Change password
   
3. Bug Fixes (5 points)
   - Fix login timeout issue
   - Resolve image upload bug
   
4. Testing (8 points)
   - Write unit tests
   - Integration testing
   - UAT preparation

Capacity: 34 points
Committed: 34 points

Risks:
- Payment gateway API documentation unclear
- Avatar upload needs S3 setup

Quyết định:
- Start with VNPay first (more documentation)
- Use Cloudinary for avatar storage (faster than S3)
- Daily standup at 9:30 AM

Action items:
- Setup VNPay sandbox (Dev team, 02/12/2025)
- Create Cloudinary account (DevOps, 01/12/2025)
- Prepare test cases (QA team, 03/12/2025)
            """,
            "analysis": {
                "summary": "Sprint planning cho Sprint 15, focus vào payment integration và user profile.",
                "topics": ["Payment integration", "User profile", "Bug fixes", "Testing"],
                "action_items": [
                    {"task": "Setup VNPay sandbox", "assignee": "Dev team", "deadline": "02/12/2025"},
                    {"task": "Create Cloudinary account", "assignee": "DevOps", "deadline": "01/12/2025"}
                ]
            },
            "metadata": {
                "meeting_type": "meeting",
                "language": "vi",
                "timestamp": (datetime.now() - timedelta(days=2)).isoformat()
            }
        },
        {
            "meeting_id": "demo_meeting_003",
            "transcript": """
Client Meeting - Website Redesign Project

Client: ABC Corporation
Agency: XYZ Digital

Attendees:
- Client: CEO, Marketing Director
- Agency: Account Manager, Designer, Developer

Agenda:
1. Review current website issues
   - Slow loading speed
   - Not mobile-friendly
   - Outdated design
   
2. Discuss redesign requirements
   - Modern, clean design
   - Fast performance
   - SEO optimized
   - Mobile responsive
   
3. Timeline and budget
   - Project duration: 3 months
   - Budget: 200 million VND
   - Launch date: March 2026
   
4. Next steps
   - Wireframe approval by 15/12
   - Design mockups by 30/12
   - Development starts 05/01/2026

Client feedback:
- Want to see competitor analysis
- Need e-commerce functionality
- Prefer blue color scheme

Quyết định:
- Approve project scope and budget
- Weekly progress meetings every Friday
- Use WordPress + WooCommerce platform

Action items:
- Send competitor analysis report (Agency, 08/12/2025)
- Prepare wireframes (Designer, 15/12/2025)
- Setup development environment (Developer, 10/12/2025)
- Sign contract (Both parties, 05/12/2025)
            """,
            "analysis": {
                "summary": "Client meeting về dự án redesign website, thống nhất scope, budget và timeline.",
                "topics": ["Website redesign", "Requirements", "Timeline", "Budget"],
                "action_items": [
                    {"task": "Send competitor analysis", "assignee": "Agency", "deadline": "08/12/2025"},
                    {"task": "Prepare wireframes", "assignee": "Designer", "deadline": "15/12/2025"}
                ]
            },
            "metadata": {
                "meeting_type": "meeting",
                "language": "vi",
                "timestamp": (datetime.now() - timedelta(days=4)).isoformat()
            }
        },
        {
            "meeting_id": "demo_meeting_004",
            "transcript": "Họp team marketing về chiến dịch Black Friday. Thảo luận về ngân sách quảng cáo, kênh marketing, và KPI. Quyết định tăng budget Facebook Ads lên 100 triệu, chạy Google Ads 50 triệu. Mục tiêu doanh thu 500 triệu trong 3 ngày. Action: Chuẩn bị creative (Design team, 25/11), Setup campaigns (Marketing, 26/11).",
            "analysis": {"summary": "Họp marketing Black Friday, budget 150 triệu, target 500 triệu doanh thu.", "topics": ["Black Friday", "Facebook Ads", "Google Ads"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=10)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_005",
            "transcript": "Cuộc họp về tuyển dụng nhân sự. Cần tuyển 5 developers, 2 QA, 1 designer. Yêu cầu: 2+ năm kinh nghiệm, biết React/Node.js. Lương: 15-25 triệu. Quyết định đăng tin trên TopCV, ITviec, LinkedIn. Action: Viết JD (HR, 01/12), Screen CV (HR, 05/12), Schedule interviews (HR, 10/12).",
            "analysis": {"summary": "Họp tuyển dụng, cần 8 người, lương 15-25tr.", "topics": ["Tuyển dụng", "Developers", "QA", "Designer"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=7)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_002",
            "transcript": "Workshop: Git & GitHub cho beginners. Nội dung: Git basics (init, add, commit, push), Branching strategy, Pull requests, Merge conflicts. Bài tập: Tạo repo, commit code, tạo branch, merge code. Q&A: Git vs GitHub? Khi nào dùng rebase? Action: Practice daily (All, ongoing).",
            "analysis": {"summary": "Workshop Git/GitHub cơ bản, cover branching và PR.", "topics": ["Git", "GitHub", "Branching", "Pull Request"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=6)).isoformat()}
        },
        {
            "meeting_id": "demo_brainstorm_002",
            "transcript": "Brainstorming: Cải thiện UX của website. Ideas: Simplify navigation, Add search bar, Improve loading speed, Better mobile experience, Add chatbot, Live chat support. Voting: Search bar (9 votes), Loading speed (8 votes), Mobile UX (7 votes). Quyết định: Implement search và optimize performance trong Q1. Action: Design search UI (Design, 15/12), Audit performance (Dev, 18/12).",
            "analysis": {"summary": "Brainstorm UX improvements, priority: search và performance.", "topics": ["UX", "Search", "Performance", "Mobile"], "action_items": []},
            "metadata": {"meeting_type": "brainstorming", "language": "vi", "timestamp": (datetime.now() - timedelta(days=8)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_006",
            "transcript": "Daily standup meeting. Team updates: John đang fix bug login, Sarah làm payment integration, Mike design dashboard mới. Blockers: API documentation thiếu, staging server down. Action: Contact vendor về API docs (John, today), Restart staging server (DevOps, today).",
            "analysis": {"summary": "Daily standup, có 2 blockers cần resolve.", "topics": ["Standup", "Bug fixes", "Payment", "Dashboard"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_007",
            "transcript": "Retrospective Sprint 14. What went well: Completed all stories, Good teamwork, Fast deployment. What to improve: More code review, Better testing, Clearer requirements. Action items: Setup code review checklist (Tech lead, 03/12), Add more unit tests (All devs, ongoing), Refine user stories (PO, before sprint).",
            "analysis": {"summary": "Sprint retro, team làm tốt nhưng cần improve testing và requirements.", "topics": ["Retrospective", "Code review", "Testing", "Requirements"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=3)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_003",
            "transcript": "Workshop: Docker & Kubernetes basics. Topics: Container concepts, Docker commands, Dockerfile, Docker Compose, K8s architecture, Pods, Services, Deployments. Hands-on: Build Docker image, Run container, Deploy to K8s cluster. Q&A: Docker vs VM? When to use K8s? Action: Complete lab exercises (All, 10/12).",
            "analysis": {"summary": "Workshop Docker/K8s, hands-on với containers và orchestration.", "topics": ["Docker", "Kubernetes", "Containers", "Deployment"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=9)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_008",
            "transcript": "Họp về bảo mật hệ thống. Phát hiện: SQL injection vulnerability, Weak password policy, No rate limiting. Quyết định: Fix SQL injection ngay (Critical), Implement rate limiting (High), Update password policy (Medium). Action: Patch SQL injection (Security team, 30/11), Add rate limiter (Backend, 05/12), Update auth flow (Backend, 08/12).",
            "analysis": {"summary": "Họp security, phát hiện 3 vulnerabilities cần fix urgent.", "topics": ["Security", "SQL Injection", "Rate Limiting", "Password Policy"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_009",
            "transcript": "Product roadmap Q1 2026. Features: User authentication, Payment gateway, Admin dashboard, Reporting module, Mobile app MVP. Priority: Auth (P0), Payment (P0), Dashboard (P1), Reporting (P2), Mobile (P3). Timeline: Auth (Jan), Payment (Feb), Dashboard (Mar). Action: Create detailed specs (PM, 15/12), Estimate effort (Tech lead, 20/12).",
            "analysis": {"summary": "Product roadmap Q1, focus vào auth và payment.", "topics": ["Roadmap", "Authentication", "Payment", "Dashboard"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=12)).isoformat()}
        },
        {
            "meeting_id": "demo_brainstorm_003",
            "transcript": "Brainstorming: Tên cho sản phẩm mới. Ideas: QuickPay, FastBuy, EasyShop, SmartCart, OneClick, PayNow, ShopEasy, BuyFast. Voting: QuickPay (12 votes), EasyShop (10 votes), SmartCart (8 votes). Concerns: QuickPay domain đã có người dùng, EasyShop quá generic. Quyết định: Check trademark QuickPay, nếu không được thì dùng SmartCart. Action: Trademark search (Legal, 05/12).",
            "analysis": {"summary": "Brainstorm tên sản phẩm, chọn QuickPay hoặc SmartCart.", "topics": ["Product naming", "Branding", "Trademark"], "action_items": []},
            "metadata": {"meeting_type": "brainstorming", "language": "vi", "timestamp": (datetime.now() - timedelta(days=11)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_010",
            "transcript": "Họp về performance optimization. Vấn đề: Page load 5s, API response 2s, Database queries chậm. Giải pháp: Add caching (Redis), Optimize queries (indexing), CDN cho static files, Code splitting. Quyết định: Implement Redis cache, Add DB indexes, Setup CloudFlare CDN. Action: Setup Redis (DevOps, 02/12), Optimize queries (Backend, 05/12), Configure CDN (DevOps, 03/12).",
            "analysis": {"summary": "Họp performance, implement caching và CDN để tăng tốc.", "topics": ["Performance", "Caching", "Redis", "CDN", "Database"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=5)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_004",
            "transcript": "Workshop: API Design Best Practices. Topics: RESTful principles, HTTP methods, Status codes, Versioning, Authentication (JWT, OAuth), Rate limiting, Documentation (Swagger). Examples: Good vs bad API design. Hands-on: Design API cho e-commerce system. Q&A: REST vs GraphQL? API versioning strategies? Action: Design API for project (All, 12/12).",
            "analysis": {"summary": "Workshop API design, cover REST principles và best practices.", "topics": ["API Design", "REST", "JWT", "Swagger", "GraphQL"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=13)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_011",
            "transcript": "Họp về customer feedback. Feedback: App crashes nhiều (20 reports), Checkout process phức tạp (15 reports), Slow loading (10 reports), Missing features (8 reports). Priority: Fix crashes (P0), Simplify checkout (P1), Improve performance (P1). Action: Debug crash logs (Dev, 01/12), Redesign checkout flow (UX, 05/12), Performance audit (Dev, 03/12).",
            "analysis": {"summary": "Review customer feedback, priority fix crashes và checkout.", "topics": ["Customer Feedback", "Bug Fixes", "UX", "Performance"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=6)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_012",
            "transcript": "Kick-off meeting dự án CRM mới. Scope: Customer management, Sales pipeline, Email integration, Reporting. Team: 4 devs, 1 designer, 1 PM, 1 QA. Timeline: 4 tháng (Jan-Apr 2026). Budget: 500 triệu. Tech stack: React, Node.js, PostgreSQL, AWS. Action: Setup project (PM, 02/12), Design mockups (Designer, 10/12), Setup infrastructure (DevOps, 05/12).",
            "analysis": {"summary": "Kick-off CRM project, 4 tháng, budget 500tr.", "topics": ["CRM", "Project Kickoff", "React", "Node.js"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=14)).isoformat()}
        },
        {
            "meeting_id": "demo_brainstorm_004",
            "transcript": "Brainstorming: Content marketing strategy. Ideas: Blog posts (SEO), Video tutorials (YouTube), Podcasts, Webinars, Case studies, Infographics, Social media campaigns, Email newsletters. Voting: Blog (15 votes), Video (12 votes), Webinars (10 votes). Quyết định: Focus vào blog và video, 2 posts/week, 1 video/week. Action: Content calendar (Marketing, 08/12), Hire content writer (HR, 15/12).",
            "analysis": {"summary": "Brainstorm content strategy, focus blog và video.", "topics": ["Content Marketing", "SEO", "Video", "Blog"], "action_items": []},
            "metadata": {"meeting_type": "brainstorming", "language": "vi", "timestamp": (datetime.now() - timedelta(days=15)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_013",
            "transcript": "Họp về infrastructure migration. Plan: Migrate từ on-premise sang AWS. Services: EC2, RDS, S3, CloudFront, Route53. Timeline: 2 tháng. Risks: Downtime, Data loss, Cost overrun. Mitigation: Blue-green deployment, Backup strategy, Cost monitoring. Action: AWS account setup (DevOps, 01/12), Migration plan (DevOps, 10/12), Test migration (DevOps, 20/12).",
            "analysis": {"summary": "Plan migrate lên AWS, 2 tháng, dùng blue-green deployment.", "topics": ["AWS", "Migration", "Infrastructure", "DevOps"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=16)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_005",
            "transcript": "Workshop: Agile & Scrum fundamentals. Topics: Agile manifesto, Scrum roles (PO, SM, Team), Ceremonies (Sprint planning, Daily standup, Review, Retro), Artifacts (Backlog, Sprint backlog, Increment). Exercises: Write user stories, Estimate with planning poker, Run mock standup. Q&A: Scrum vs Kanban? Sprint length? Action: Apply Scrum in team (All, ongoing).",
            "analysis": {"summary": "Workshop Agile/Scrum, cover roles, ceremonies, và artifacts.", "topics": ["Agile", "Scrum", "User Stories", "Sprint Planning"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=17)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_014",
            "transcript": "Họp về data analytics. Metrics: DAU 10k, MAU 50k, Retention 40%, Churn 15%, ARPU $5. Goals: Tăng retention lên 50%, Giảm churn xuống 10%, Tăng ARPU lên $7. Strategies: Improve onboarding, Add premium features, Email campaigns. Action: Analyze user behavior (Data team, 05/12), A/B test onboarding (Product, 10/12), Design premium tier (Product, 15/12).",
            "analysis": {"summary": "Review analytics, focus tăng retention và ARPU.", "topics": ["Analytics", "Retention", "Churn", "ARPU", "Metrics"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=18)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_015",
            "transcript": "Họp về compliance & GDPR. Requirements: User consent, Data encryption, Right to deletion, Data portability, Privacy policy. Current status: 60% compliant. Gaps: No consent management, Weak encryption, No deletion flow. Action: Implement consent banner (Dev, 05/12), Upgrade encryption (Security, 08/12), Add delete account (Dev, 12/12), Update privacy policy (Legal, 03/12).",
            "analysis": {"summary": "GDPR compliance review, cần implement consent và encryption.", "topics": ["GDPR", "Compliance", "Privacy", "Security", "Legal"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=19)).isoformat()}
        },
        {
            "meeting_id": "demo_brainstorm_005",
            "transcript": "Brainstorming: Gamification cho app. Ideas: Points system, Badges, Leaderboards, Daily challenges, Streak rewards, Level up, Achievements, Referral bonuses. Voting: Points (14 votes), Badges (11 votes), Daily challenges (9 votes). Concerns: Gamification có thể annoying, Cần balance giữa fun và utility. Quyết định: Start với points và badges, test với small user group. Action: Design gamification system (Product, 10/12), Implement MVP (Dev, 20/12).",
            "analysis": {"summary": "Brainstorm gamification, chọn points và badges để test.", "topics": ["Gamification", "User Engagement", "Points", "Badges"], "action_items": []},
            "metadata": {"meeting_type": "brainstorming", "language": "vi", "timestamp": (datetime.now() - timedelta(days=20)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_016",
            "transcript": "Họp về mobile app strategy. Platforms: iOS và Android. Approach: Native vs Cross-platform (React Native, Flutter). Decision: Dùng React Native (faster development, shared codebase, good performance). Features: Login, Browse products, Cart, Checkout, Profile. Timeline: 3 tháng. Action: Setup React Native project (Mobile team, 02/12), Design mobile UI (Designer, 08/12), Develop MVP (Mobile team, Jan-Mar).",
            "analysis": {"summary": "Mobile strategy, chọn React Native, timeline 3 tháng.", "topics": ["Mobile App", "React Native", "iOS", "Android"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=21)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_006",
            "transcript": "Workshop: SQL & Database Design. Topics: SQL basics (SELECT, INSERT, UPDATE, DELETE), Joins (INNER, LEFT, RIGHT), Indexes, Normalization, Transactions, Query optimization. Hands-on: Design database schema cho blog system, Write complex queries, Optimize slow queries. Q&A: NoSQL vs SQL? When to denormalize? Action: Complete database exercises (All, 15/12).",
            "analysis": {"summary": "Workshop SQL, cover queries, joins, và optimization.", "topics": ["SQL", "Database", "Joins", "Optimization", "Schema Design"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=22)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_017",
            "transcript": "Họp về email marketing campaign. Campaign: Holiday sale 2025. Target: 50k subscribers. Content: 20% discount, Free shipping, Gift with purchase. Schedule: 3 emails (teaser, launch, reminder). Metrics: Open rate >25%, Click rate >5%, Conversion >2%. Action: Design email templates (Designer, 05/12), Write copy (Marketing, 06/12), Setup automation (Marketing, 08/12), Send test emails (Marketing, 10/12).",
            "analysis": {"summary": "Email campaign holiday sale, target 50k subscribers.", "topics": ["Email Marketing", "Holiday Sale", "Discount", "Automation"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=23)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_018",
            "transcript": "Họp về SEO strategy. Current: Organic traffic 5k/month, Ranking keywords 50, Backlinks 100. Goals: Traffic 20k/month, Keywords 200, Backlinks 500. Tactics: Content marketing, Link building, Technical SEO, On-page optimization. Action: SEO audit (Marketing, 05/12), Keyword research (Marketing, 08/12), Create content plan (Marketing, 10/12), Fix technical issues (Dev, 12/12).",
            "analysis": {"summary": "SEO strategy, target tăng traffic từ 5k lên 20k/month.", "topics": ["SEO", "Content Marketing", "Link Building", "Keywords"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=24)).isoformat()}
        },
        {
            "meeting_id": "demo_brainstorm_006",
            "transcript": "Brainstorming: Partnership opportunities. Ideas: Integrate với Shopee, Lazada, TikTok Shop, Facebook Marketplace, Zalo, Momo, VNPay, Banks. Voting: Shopee (16 votes), Momo (14 votes), TikTok Shop (12 votes). Benefits: Reach more customers, Increase sales, Brand awareness. Concerns: Integration complexity, Revenue sharing. Quyết định: Start với Momo integration (easiest), then Shopee. Action: Contact Momo (BD, 05/12), Prepare integration docs (Dev, 10/12).",
            "analysis": {"summary": "Brainstorm partnerships, priority Momo và Shopee.", "topics": ["Partnership", "Integration", "Momo", "Shopee", "TikTok"], "action_items": []},
            "metadata": {"meeting_type": "brainstorming", "language": "vi", "timestamp": (datetime.now() - timedelta(days=25)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_019",
            "transcript": "Họp về customer support. Channels: Email, Chat, Phone, Social media. Metrics: Response time 2h, Resolution time 24h, CSAT 85%. Issues: High volume, Slow response, Repetitive questions. Solutions: Add chatbot, Create FAQ, Hire more agents, Use ticketing system. Action: Implement chatbot (Dev, 10/12), Write FAQ (Support, 05/12), Hire 2 agents (HR, 15/12), Setup Zendesk (IT, 08/12).",
            "analysis": {"summary": "Customer support improvements, add chatbot và FAQ.", "topics": ["Customer Support", "Chatbot", "FAQ", "Zendesk"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=26)).isoformat()}
        },
        {
            "meeting_id": "demo_workshop_007",
            "transcript": "Workshop: UI/UX Design Principles. Topics: Design thinking, User research, Wireframing, Prototyping, Usability testing, Design systems, Accessibility. Tools: Figma, Adobe XD, Sketch. Exercises: Create wireframes cho mobile app, Design high-fidelity mockups, Conduct usability test. Q&A: Mobile-first vs Desktop-first? Design trends 2026? Action: Complete design project (All, 20/12).",
            "analysis": {"summary": "Workshop UI/UX, cover design thinking và prototyping.", "topics": ["UI/UX", "Design Thinking", "Figma", "Prototyping", "Usability"], "action_items": []},
            "metadata": {"meeting_type": "workshop", "language": "vi", "timestamp": (datetime.now() - timedelta(days=27)).isoformat()}
        },
        {
            "meeting_id": "demo_meeting_020",
            "transcript": "Họp về social media strategy. Platforms: Facebook, Instagram, TikTok, LinkedIn, YouTube. Content types: Posts, Stories, Reels, Videos, Lives. Frequency: Daily posts, 3 stories/day, 2 reels/week, 1 video/week. Goals: Followers 100k, Engagement rate 5%, Traffic 10k/month. Action: Create content calendar (Marketing, 05/12), Hire social media manager (HR, 10/12), Setup analytics (Marketing, 08/12).",
            "analysis": {"summary": "Social media strategy, target 100k followers và 5% engagement.", "topics": ["Social Media", "Facebook", "Instagram", "TikTok", "Content"], "action_items": []},
            "metadata": {"meeting_type": "meeting", "language": "vi", "timestamp": (datetime.now() - timedelta(days=28)).isoformat()}
        }
    ]
    
    # Add each meeting to ChromaDB
    success_count = 0
    for meeting in sample_meetings:
        try:
            print(f"Adding: {meeting['meeting_id']}...")
            
            manager.store_meeting(
                meeting_id=meeting['meeting_id'],
                transcript=meeting['transcript'],
                analysis=meeting['analysis'],
                meeting_type=meeting['metadata']['meeting_type'],
                language=meeting['metadata']['language']
            )
            
            print(f"  ✓ Added successfully")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print()
    print("=" * 70)
    print(f"COMPLETED: {success_count}/{len(sample_meetings)} meetings added")
    print("=" * 70)
    print()
    
    # Show statistics
    stats = manager.get_statistics()
    print("📊 ChromaDB Statistics:")
    print(f"  Total meetings: {stats['total_meetings']}")
    print(f"  By type: {stats['by_type']}")
    print(f"  By language: {stats['by_language']}")
    print()
    
    print("✅ Sample data populated successfully!")
    print()
    print("🔍 Try searching for:")
    print("  - 'ngân sách' (budget)")
    print("  - 'payment' (thanh toán)")
    print("  - 'Python' (lập trình)")
    print("  - 'mobile app' (ứng dụng)")
    print("  - 'website' (trang web)")
    print()


if __name__ == "__main__":
    populate_sample_data()
