"""Prompt templates for the chatbot."""


class PromptTemplates:
    """Các prompt templates với system messages tối ưu."""

    # System Messages - Vietnamese
    SYSTEM_ANALYST_VI = """Bạn là một trợ lý AI chuyên nghiệp, chuyên phân tích transcript cuộc họp.

Nhiệm vụ của bạn:
- Đọc và hiểu toàn bộ nội dung cuộc họp
- Trích xuất thông tin chính xác và quan trọng
- Trả lời câu hỏi dựa trên dữ liệu có sẵn
- Luôn trung thực, nếu không biết thì nói không biết

Phong cách:
- Chuyên nghiệp, rõ ràng, ngắn gọn
- Sử dụng tiếng Việt
- Trích dẫn nguồn khi có thể"""

    SYSTEM_SUMMARIZER_VI = """Bạn là chuyên gia tóm tắt cuộc họp.

Kỹ năng của bạn:
- Nắm bắt ý chính nhanh chóng
- Tóm tắt ngắn gọn nhưng đầy đủ
- Làm nổi bật các điểm quan trọng

Yêu cầu:
- Tóm tắt trong 3-5 câu
- Bao gồm các chủ đề chính
- Sử dụng tiếng Việt"""

    SYSTEM_EXTRACTOR_VI = """Bạn là chuyên gia trích xuất thông tin từ cuộc họp.

Nhiệm vụ:
- Tìm và trích xuất thông tin cụ thể
- Phân loại thông tin chính xác
- Trả về dữ liệu có cấu trúc (JSON)

Nguyên tắc:
- Chỉ trích xuất thông tin có trong transcript
- Không bịa đặt hoặc suy đoán
- Trả về [] nếu không tìm thấy"""

    # System Messages - English
    SYSTEM_ANALYST_EN = """You are a professional AI assistant specialized in analyzing meeting transcripts.

Your responsibilities:
- Read and understand the entire meeting content
- Extract accurate and important information
- Answer questions based on available data
- Always be truthful, if you don't know, say you don't know

Style:
- Professional, clear, concise
- Use English
- Cite sources when possible"""

    SYSTEM_SUMMARIZER_EN = """You are a meeting summarization expert.

Your skills:
- Quickly grasp main ideas
- Summarize concisely but comprehensively
- Highlight important points

Requirements:
- Summarize in 3-5 sentences
- Include main topics
- Use English"""

    SYSTEM_EXTRACTOR_EN = """You are an expert in extracting information from meetings.

Tasks:
- Find and extract specific information
- Classify information accurately
- Return structured data (JSON)

Principles:
- Only extract information present in the transcript
- Do not fabricate or speculate
- Return [] if nothing found"""

    # System Messages - Japanese
    SYSTEM_ANALYST_JA = """あなたは会議の議事録を分析する専門的なAIアシスタントです。

あなたの責任:
- 会議の内容全体を読んで理解する
- 正確で重要な情報を抽出する
- 利用可能なデータに基づいて質問に答える
- 常に誠実であり、わからない場合はわからないと言う

スタイル:
- プロフェッショナル、明確、簡潔
- 日本語を使用
- 可能な限り出典を引用"""

    SYSTEM_SUMMARIZER_JA = """あなたは会議要約の専門家です。

あなたのスキル:
- 主要なアイデアを素早く把握
- 簡潔かつ包括的に要約
- 重要なポイントを強調

要件:
- 3-5文で要約
- 主要なトピックを含める
- 日本語を使用"""

    SYSTEM_EXTRACTOR_JA = """あなたは会議から情報を抽出する専門家です。

タスク:
- 特定の情報を見つけて抽出
- 情報を正確に分類
- 構造化されたデータ（JSON）を返す

原則:
- 議事録に存在する情報のみを抽出
- 捏造や推測をしない
- 何も見つからない場合は[]を返す"""

    # System Messages - Korean
    SYSTEM_ANALYST_KO = """당신은 회의 기록을 분석하는 전문 AI 어시스턴트입니다.

당신의 책임:
- 회의 내용 전체를 읽고 이해하기
- 정확하고 중요한 정보 추출하기
- 사용 가능한 데이터를 기반으로 질문에 답하기
- 항상 정직하며, 모르면 모른다고 말하기

스타일:
- 전문적이고 명확하며 간결하게
- 한국어 사용
- 가능한 경우 출처 인용"""

    SYSTEM_SUMMARIZER_KO = """당신은 회의 요약 전문가입니다.

당신의 기술:
- 주요 아이디어를 빠르게 파악
- 간결하지만 포괄적으로 요약
- 중요한 포인트 강조

요구사항:
- 3-5문장으로 요약
- 주요 주제 포함
- 한국어 사용"""

    SYSTEM_EXTRACTOR_KO = """당신은 회의에서 정보를 추출하는 전문가입니다.

작업:
- 특정 정보를 찾아 추출
- 정보를 정확하게 분류
- 구조화된 데이터(JSON) 반환

원칙:
- 기록에 있는 정보만 추출
- 조작하거나 추측하지 않기
- 아무것도 찾지 못하면 [] 반환"""

    # System Messages - Chinese
    SYSTEM_ANALYST_ZH = """您是一位专业的AI助手，专门分析会议记录。

您的职责：
- 阅读并理解整个会议内容
- 提取准确和重要的信息
- 根据可用数据回答问题
- 始终诚实，如果不知道就说不知道

风格：
- 专业、清晰、简洁
- 使用中文
- 尽可能引用来源"""

    SYSTEM_SUMMARIZER_ZH = """您是会议总结专家。

您的技能：
- 快速掌握主要思想
- 简洁而全面地总结
- 突出重要要点

要求：
- 用3-5句话总结
- 包括主要主题
- 使用中文"""

    SYSTEM_EXTRACTOR_ZH = """您是从会议中提取信息的专家。

任务：
- 查找并提取特定信息
- 准确分类信息
- 返回结构化数据（JSON）

原则：
- 仅提取记录中存在的信息
- 不要捏造或推测
- 如果没有找到任何内容，返回[]"""

    @staticmethod
    def get_summary_prompt(transcript: str, language: str = "vi") -> str:
        """Prompt cho tóm tắt cuộc họp."""
        prompts = {
            "en": f"""Read the following meeting transcript and create a concise summary.

TRANSCRIPT:
{transcript}

REQUIREMENTS:
- Summarize in 3-5 sentences
- State the meeting purpose clearly
- List main topics discussed
- Highlight important points

SUMMARY:""",
            "vi": f"""Hãy đọc transcript cuộc họp sau và tạo bản tóm tắt ngắn gọn.

TRANSCRIPT:
{transcript}

YÊU CẦU:
- Tóm tắt trong 3-5 câu
- Nêu rõ mục đích cuộc họp
- Liệt kê các chủ đề chính được thảo luận
- Highlight các điểm quan trọng

TÓM TẮT:""",
            "ja": f"""以下の会議の議事録を読んで、簡潔な要約を作成してください。

議事録:
{transcript}

要件:
- 3-5文で要約
- 会議の目的を明確に述べる
- 議論された主要なトピックをリストアップ
- 重要なポイントを強調

要約:""",
            "ko": f"""다음 회의 기록을 읽고 간결한 요약을 작성하세요.

회의 기록:
{transcript}

요구사항:
- 3-5문장으로 요약
- 회의 목적을 명확히 기술
- 논의된 주요 주제 나열
- 중요한 포인트 강조

요약:""",
            "zh": f"""请阅读以下会议记录并创建简洁的摘要。

会议记录:
{transcript}

要求:
- 用3-5句话总结
- 明确说明会议目的
- 列出讨论的主要主题
- 突出重要要点

摘要:"""
        }
        return prompts.get(language, prompts["vi"])

    @staticmethod
    def get_qa_prompt(transcript: str, question: str, language: str = "vi") -> str:
        """Prompt cho Q&A."""
        prompts = {
            "en": f"""Based on the meeting transcript below, answer the user's question.

TRANSCRIPT:
{transcript}

QUESTION: {question}

ANSWER GUIDELINES:
1. Read the transcript carefully to find relevant information
2. Answer accurately based on available information
3. If information is not found, clearly state "I cannot find this information in the transcript"
4. Quote relevant parts if possible
5. Answer in English, clearly and concisely

ANSWER:""",
            "vi": f"""Dựa trên transcript cuộc họp dưới đây, hãy trả lời câu hỏi của người dùng.

TRANSCRIPT:
{transcript}

CÂU HỎI: {question}

HƯỚNG DẪN TRẢ LỜI:
1. Đọc kỹ transcript để tìm thông tin liên quan
2. Trả lời chính xác dựa trên thông tin có sẵn
3. Nếu không tìm thấy thông tin, nói rõ "Tôi không tìm thấy thông tin này trong transcript"
4. Trích dẫn phần liên quan nếu có thể
5. Trả lời bằng tiếng Việt, rõ ràng và ngắn gọn

TRẢ LỜI:""",
            "ja": f"""以下の会議の議事録に基づいて、ユーザーの質問に答えてください。

議事録:
{transcript}

質問: {question}

回答ガイドライン:
1. 議事録を注意深く読んで関連情報を見つける
2. 利用可能な情報に基づいて正確に答える
3. 情報が見つからない場合は、「この情報は議事録に見つかりません」と明確に述べる
4. 可能であれば関連部分を引用する
5. 日本語で明確かつ簡潔に答える

回答:""",
            "ko": f"""아래 회의 기록을 바탕으로 사용자의 질문에 답하세요.

회의 기록:
{transcript}

질문: {question}

답변 가이드라인:
1. 기록을 주의 깊게 읽어 관련 정보를 찾기
2. 사용 가능한 정보를 기반으로 정확하게 답변
3. 정보를 찾을 수 없는 경우 "이 정보는 기록에서 찾을 수 없습니다"라고 명확히 말하기
4. 가능한 경우 관련 부분 인용
5. 한국어로 명확하고 간결하게 답변

답변:""",
            "zh": f"""根据以下会议记录回答用户的问题。

会议记录:
{transcript}

问题: {question}

回答指南:
1. 仔细阅读记录以查找相关信息
2. 根据可用信息准确回答
3. 如果找不到信息，请明确说明"我在记录中找不到此信息"
4. 如果可能，引用相关部分
5. 用中文清晰简洁地回答

回答:"""
        }
        return prompts.get(language, prompts["vi"])

    @staticmethod
    def _get_language_text(language: str, texts: dict) -> str:
        """Helper to get text in specified language."""
        return texts.get(language, texts.get("vi", texts["en"]))

    @staticmethod
    def get_action_items_prompt(transcript: str, language: str = "vi") -> str:
        """Prompt cho trích xuất action items."""
        prompts = {
            "en": f"""Analyze the meeting transcript and extract ALL action items (tasks to be done).

TRANSCRIPT:
{transcript}

ACTION ITEM DEFINITION:
- Specific task to be performed
- Has assigned person
- May or may not have deadline

REQUIREMENTS:
- Find all mentioned tasks
- Identify responsible person (if any)
- Note deadline (if any)
- Return exact JSON format

JSON FORMAT:
[
    {{
        "task": "Specific task description",
        "assignee": "Person responsible",
        "deadline": "Completion deadline"
    }}
]

NOTES:
- If no assignee: "assignee": "Not assigned"
- If no deadline: "deadline": "Not specified"
- If no action items found: return []

ACTION ITEMS:""",
            "vi": f"""Phân tích transcript cuộc họp và trích xuất TẤT CẢ các action items (nhiệm vụ cần làm).

TRANSCRIPT:
{transcript}

ĐỊNH NGHĨA ACTION ITEM:
- Nhiệm vụ cụ thể cần thực hiện
- Có người được giao trách nhiệm
- Có thể có hoặc không có deadline

YÊU CẦU:
- Tìm tất cả các nhiệm vụ được đề cập
- Xác định người phụ trách (nếu có)
- Ghi nhận deadline (nếu có)
- Trả về định dạng JSON chính xác

ĐỊNH DẠNG JSON:
[
    {{
        "task": "Mô tả nhiệm vụ cụ thể",
        "assignee": "Tên người phụ trách",
        "deadline": "Thời hạn hoàn thành"
    }}
]

LƯU Ý:
- Nếu không có người phụ trách: "assignee": "Chưa phân công"
- Nếu không có deadline: "deadline": "Chưa xác định"
- Nếu không tìm thấy action items: trả về []

ACTION ITEMS:""",
            "ja": f"""会議の議事録を分析し、すべてのアクションアイテム（実行すべきタスク）を抽出してください。

議事録:
{transcript}

アクションアイテムの定義:
- 実行すべき具体的なタスク
- 担当者が割り当てられている
- 期限がある場合とない場合がある

要件:
- 言及されたすべてのタスクを見つける
- 担当者を特定（該当する場合）
- 期限を記録（該当する場合）
- 正確なJSON形式で返す

JSON形式:
[
    {{
        "task": "具体的なタスクの説明",
        "assignee": "担当者",
        "deadline": "完了期限"
    }}
]

注意:
- 担当者がいない場合: "assignee": "未割り当て"
- 期限がない場合: "deadline": "未指定"
- アクションアイテムが見つからない場合: []を返す

アクションアイテム:""",
            "ko": f"""회의 기록을 분석하고 모든 액션 아이템(수행할 작업)을 추출하세요.

회의 기록:
{transcript}

액션 아이템 정의:
- 수행해야 할 구체적인 작업
- 담당자가 할당됨
- 마감일이 있을 수도 있고 없을 수도 있음

요구사항:
- 언급된 모든 작업 찾기
- 담당자 식별(해당하는 경우)
- 마감일 기록(해당하는 경우)
- 정확한 JSON 형식으로 반환

JSON 형식:
[
    {{
        "task": "구체적인 작업 설명",
        "assignee": "담당자",
        "deadline": "완료 마감일"
    }}
]

참고:
- 담당자가 없는 경우: "assignee": "미할당"
- 마감일이 없는 경우: "deadline": "미지정"
- 액션 아이템을 찾지 못한 경우: [] 반환

액션 아이템:""",
            "zh": f"""分析会议记录并提取所有行动项（需要完成的任务）。

会议记录:
{transcript}

行动项定义:
- 需要执行的具体任务
- 有指定负责人
- 可能有或没有截止日期

要求:
- 找到所有提到的任务
- 识别负责人（如果有）
- 记录截止日期（如果有）
- 返回准确的JSON格式

JSON格式:
[
    {{
        "task": "具体任务描述",
        "assignee": "负责人",
        "deadline": "完成截止日期"
    }}
]

注意:
- 如果没有负责人: "assignee": "未分配"
- 如果没有截止日期: "deadline": "未指定"
- 如果没有找到行动项: 返回[]

行动项:"""
        }
        return prompts.get(language, prompts["vi"])

    @staticmethod
    def get_decisions_prompt(transcript: str, language: str = "vi") -> str:
        """Prompt cho trích xuất decisions."""
        base_prompts = {
            "en": ("Analyze the meeting transcript and extract ALL important decisions.", "DECISION DEFINITION:", "REQUIREMENTS:", "JSON FORMAT:", "NOTES:", "DECISIONS:"),
            "vi": ("Phân tích transcript cuộc họp và trích xuất TẤT CẢ các quyết định quan trọng.", "ĐỊNH NGHĨA QUYẾT ĐỊNH:", "YÊU CẦU:", "ĐỊNH DẠNG JSON:", "LƯU Ý:", "QUYẾT ĐỊNH:"),
            "ja": ("会議の議事録を分析し、すべての重要な決定を抽出してください。", "決定の定義:", "要件:", "JSON形式:", "注意:", "決定:"),
            "ko": ("회의 기록을 분석하고 모든 중요한 결정을 추출하세요.", "결정 정의:", "요구사항:", "JSON 형식:", "참고:", "결정:"),
            "zh": ("分析会议记录并提取所有重要决定。", "决定定义:", "要求:", "JSON格式:", "注意:", "决定:")
        }
        
        lang_map = {
            "en": ["Official conclusion made", "Changes to plans, strategies", "Approval or rejection of proposals", "Agreements between parties",
                   "Find all mentioned decisions", "Clearly state decision content", "Explain context/reason (if any)",
                   "Clear decision content", "Context or reason for the decision",
                   "Only record official decisions", "Do not include personal opinions", "If no decisions found: return []"],
            "vi": ["Kết luận chính thức được đưa ra", "Thay đổi về kế hoạch, chiến lược", "Phê duyệt hoặc từ chối đề xuất", "Thỏa thuận giữa các bên",
                   "Tìm tất cả các quyết định được đề cập", "Ghi rõ nội dung quyết định", "Giải thích bối cảnh/lý do (nếu có)",
                   "Nội dung quyết định rõ ràng", "Bối cảnh hoặc lý do đưa ra quyết định",
                   "Chỉ ghi nhận quyết định chính thức", "Không bao gồm ý kiến cá nhân", "Nếu không tìm thấy quyết định: trả về []"],
            "ja": ["正式な結論が出された", "計画や戦略の変更", "提案の承認または却下", "当事者間の合意",
                   "言及されたすべての決定を見つける", "決定内容を明確に述べる", "文脈/理由を説明（該当する場合）",
                   "明確な決定内容", "決定の文脈または理由",
                   "正式な決定のみを記録", "個人的な意見を含めない", "決定が見つからない場合: []を返す"],
            "ko": ["공식적인 결론이 내려짐", "계획, 전략의 변경", "제안의 승인 또는 거부", "당사자 간의 합의",
                   "언급된 모든 결정 찾기", "결정 내용을 명확히 기술", "맥락/이유 설명(해당하는 경우)",
                   "명확한 결정 내용", "결정의 맥락 또는 이유",
                   "공식 결정만 기록", "개인 의견 포함하지 않기", "결정을 찾지 못한 경우: [] 반환"],
            "zh": ["做出的正式结论", "计划、策略的变更", "提案的批准或拒绝", "各方之间的协议",
                   "找到所有提到的决定", "明确说明决定内容", "解释背景/原因（如果有）",
                   "明确的决定内容", "决定的背景或原因",
                   "仅记录正式决定", "不包括个人意见", "如果没有找到决定: 返回[]"]
        }
        
        lang = language if language in base_prompts else "vi"
        headers = base_prompts[lang]
        texts = lang_map[lang]
        
        return f"""{headers[0]}

TRANSCRIPT:
{transcript}

{headers[1]}
- {texts[0]}
- {texts[1]}
- {texts[2]}
- {texts[3]}

{headers[2]}
- {texts[4]}
- {texts[5]}
- {texts[6]}

{headers[3]}
[
    {{
        "decision": "{texts[7]}",
        "context": "{texts[8]}"
    }}
]

{headers[4]}
- {texts[9]}
- {texts[10]}
- {texts[11]}

{headers[5]}"""

    @staticmethod
    def get_topics_prompt(transcript: str, language: str = "vi") -> str:
        """Prompt cho trích xuất key topics."""
        base_prompts = {
            "en": ("Analyze the meeting transcript and extract MAIN TOPICS discussed.", "TOPIC DEFINITION:", "REQUIREMENTS:", "JSON FORMAT:", "NOTES:", "TOPICS:"),
            "vi": ("Phân tích transcript cuộc họp và trích xuất các CHỦ ĐỀ CHÍNH được thảo luận.", "ĐỊNH NGHĨA CHỦ ĐỀ:", "YÊU CẦU:", "ĐỊNH DẠNG JSON:", "LƯU Ý:", "CHỦ ĐỀ:"),
            "ja": ("会議の議事録を分析し、議論された主要なトピックを抽出してください。", "トピックの定義:", "要件:", "JSON形式:", "注意:", "トピック:"),
            "ko": ("회의 기록을 분석하고 논의된 주요 주제를 추출하세요.", "주제 정의:", "요구사항:", "JSON 형식:", "참고:", "주제:"),
            "zh": ("分析会议记录并提取讨论的主要主题。", "主题定义:", "要求:", "JSON格式:", "注意:", "主题:")
        }
        
        lang_map = {
            "en": ["Issue or content discussed", "Has significant discussion time", "Important to meeting purpose",
                   "Identify 3-5 main topics", "Name concisely and clearly", "Briefly describe content",
                   "Concise topic name", "Detailed description of discussion content",
                   "Prioritize important topics", "Do not list too detailed", "If no clear topics found: return []"],
            "vi": ["Vấn đề hoặc nội dung được bàn luận", "Có thời lượng thảo luận đáng kể", "Quan trọng với mục đích cuộc họp",
                   "Xác định 3-5 chủ đề chính", "Đặt tên ngắn gọn, dễ hiểu", "Mô tả ngắn gọn nội dung",
                   "Tên chủ đề ngắn gọn", "Mô tả chi tiết về nội dung thảo luận",
                   "Ưu tiên chủ đề quan trọng", "Không liệt kê quá chi tiết", "Nếu không tìm thấy chủ đề rõ ràng: trả về []"],
            "ja": ["議論された問題または内容", "かなりの議論時間がある", "会議の目的に重要",
                   "3-5つの主要なトピックを特定", "簡潔かつ明確に名前を付ける", "内容を簡単に説明",
                   "簡潔なトピック名", "議論内容の詳細な説明",
                   "重要なトピックを優先", "詳細すぎるリストにしない", "明確なトピックが見つからない場合: []を返す"],
            "ko": ["논의된 문제 또는 내용", "상당한 논의 시간이 있음", "회의 목적에 중요",
                   "3-5개의 주요 주제 식별", "간결하고 명확하게 이름 지정", "내용을 간략히 설명",
                   "간결한 주제 이름", "논의 내용의 상세한 설명",
                   "중요한 주제 우선순위", "너무 상세하게 나열하지 않기", "명확한 주제를 찾지 못한 경우: [] 반환"],
            "zh": ["讨论的问题或内容", "有大量讨论时间", "对会议目的很重要",
                   "识别3-5个主要主题", "简洁明确地命名", "简要描述内容",
                   "简洁的主题名称", "讨论内容的详细描述",
                   "优先考虑重要主题", "不要列得太详细", "如果没有找到明确的主题: 返回[]"]
        }
        
        lang = language if language in base_prompts else "vi"
        headers = base_prompts[lang]
        texts = lang_map[lang]
        
        return f"""{headers[0]}

TRANSCRIPT:
{transcript}

{headers[1]}
- {texts[0]}
- {texts[1]}
- {texts[2]}

{headers[2]}
- {texts[3]}
- {texts[4]}
- {texts[5]}

{headers[3]}
[
    {{
        "topic": "{texts[6]}",
        "description": "{texts[7]}"
    }}
]

{headers[4]}
- {texts[8]}
- {texts[9]}
- {texts[10]}

{headers[5]}"""

    @staticmethod
    def get_system_message_for_task(task: str, language: str = "vi") -> str:
        """
        Lấy system message phù hợp cho từng task.
        
        Args:
            task: Loại task (summary, qa, extract)
            language: Ngôn ngữ output (vi, en, ja, ko, zh)
            
        Returns:
            System message phù hợp
        """
        lang_map = {"en": "_EN", "vi": "_VI", "ja": "_JA", "ko": "_KO", "zh": "_ZH"}
        suffix = lang_map.get(language, "_VI")
        
        if task == "summary":
            return getattr(PromptTemplates, f"SYSTEM_SUMMARIZER{suffix}")
        elif task == "qa":
            return getattr(PromptTemplates, f"SYSTEM_ANALYST{suffix}")
        elif task in ["action_items", "decisions", "topics"]:
            return getattr(PromptTemplates, f"SYSTEM_EXTRACTOR{suffix}")
        else:
            return getattr(PromptTemplates, f"SYSTEM_ANALYST{suffix}")
