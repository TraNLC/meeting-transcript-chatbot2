"""Gradio UI for Meeting Transcript Chatbot."""

import gradio as gr
import sys
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import Settings
from src.data import TranscriptLoader, TranscriptPreprocessor
from src.llm import LLMManager
from src.rag import Chatbot


# Global variables
chatbot = None
transcript_text = ""
last_summary = ""
last_topics = []
last_actions = []
last_decisions = []
current_language = "vi"


def process_file(file):
    """Process uploaded transcript file."""
    global chatbot, transcript_text, last_summary, last_topics, last_actions, last_decisions, current_language
    
    # Fixed configuration
    provider = "gemini"
    model = "gemini-2.5-flash"
    language = "vi"
    
    upload_msg = {
        "vi": "❌ Vui lòng upload file!",
        "en": "❌ Please upload a file!",
        "ja": "❌ ファイルをアップロードしてください！",
        "ko": "❌ 파일을 업로드해주세요!",
        "zh": "❌ 请上传文件！"
    }
    
    if file is None:
        return upload_msg.get(language, upload_msg["vi"]), "", "", "", ""
    
    # Save current language
    current_language = language
    
    try:
        # Load transcript
        loader = TranscriptLoader()
        transcript = loader.load_file(file.name)
        
        # Clean and truncate
        preprocessor = TranscriptPreprocessor()
        transcript = preprocessor.clean_text(transcript)
        transcript = preprocessor.truncate_text(transcript, max_length=15000)
        transcript_text = transcript
        
        # Initialize LLM and chatbot with Gemini
        llm_manager = LLMManager(
            provider=provider,
            model_name=model,
            temperature=Settings.TEMPERATURE,
            max_tokens=Settings.MAX_TOKENS,
            api_key=Settings.GEMINI_API_KEY,
        )
        
        chatbot = Chatbot(llm_manager=llm_manager, transcript=transcript, language=language)
        
        # Generate summary
        summary = chatbot.generate_summary()
        
        # Extract information
        topics = chatbot.extract_topics()
        action_items = chatbot.extract_action_items()
        decisions = chatbot.extract_decisions()
        
        # Save results globally for export
        last_summary = summary
        last_topics = topics
        last_actions = action_items
        last_decisions = decisions
        
        # Format outputs
        topics_text = format_topics(topics, language)
        actions_text = format_actions(action_items, language)
        decisions_text = format_decisions(decisions, language)
        
        success_msgs = {
            "vi": "✅ Transcript đã được xử lý thành công!",
            "en": "✅ Transcript processed successfully!",
            "ja": "✅ トランスクリプトが正常に処理されました！",
            "ko": "✅ 트랜스크립트가 성공적으로 처리되었습니다!",
            "zh": "✅ 记录处理成功！"
        }
        
        return (
            success_msgs.get(language, success_msgs["vi"]),
            summary,
            topics_text,
            actions_text,
            decisions_text
        )
        
    except Exception as e:
        error_prefixes = {
            "vi": "❌ Lỗi:",
            "en": "❌ Error:",
            "ja": "❌ エラー:",
            "ko": "❌ 오류:",
            "zh": "❌ 错误:"
        }
        return f"{error_prefixes.get(language, error_prefixes['vi'])} {str(e)}", "", "", "", ""


def format_topics(topics, language="vi"):
    """Format topics for display."""
    no_topics_msg = {
        "vi": "Không tìm thấy chủ đề rõ ràng",
        "en": "No clear topics found",
        "ja": "明確なトピックが見つかりません",
        "ko": "명확한 주제를 찾을 수 없습니다",
        "zh": "未找到明确的主题"
    }
    no_desc_msg = {
        "vi": "Không có mô tả",
        "en": "No description",
        "ja": "説明なし",
        "ko": "설명 없음",
        "zh": "无描述"
    }
    
    if not topics:
        return no_topics_msg.get(language, no_topics_msg["vi"])
    
    result = []
    for i, topic in enumerate(topics, 1):
        result.append(f"**{i}. {topic.get('topic', 'N/A')}**")
        result.append(f"   {topic.get('description', no_desc_msg.get(language, no_desc_msg['vi']))}")
        result.append("")
    
    return "\n".join(result)


def format_actions(actions, language="vi"):
    """Format action items for display."""
    no_actions_msg = {
        "vi": "Không tìm thấy action items",
        "en": "No action items found",
        "ja": "アクションアイテムが見つかりません",
        "ko": "액션 아이템을 찾을 수 없습니다",
        "zh": "未找到行动项"
    }
    assignee_labels = {
        "vi": "Người phụ trách",
        "en": "Assignee",
        "ja": "担当者",
        "ko": "담당자",
        "zh": "负责人"
    }
    not_assigned_msg = {
        "vi": "Chưa phân công",
        "en": "Not assigned",
        "ja": "未割り当て",
        "ko": "미할당",
        "zh": "未分配"
    }
    not_specified_msg = {
        "vi": "Chưa xác định",
        "en": "Not specified",
        "ja": "未指定",
        "ko": "미지정",
        "zh": "未指定"
    }
    
    if not actions:
        return no_actions_msg.get(language, no_actions_msg["vi"])
    
    result = []
    for i, item in enumerate(actions, 1):
        result.append(f"**{i}. {item.get('task', 'N/A')}**")
        result.append(f"   👤 {assignee_labels.get(language, assignee_labels['vi'])}: {item.get('assignee', not_assigned_msg.get(language, not_assigned_msg['vi']))}")
        result.append(f"   📅 Deadline: {item.get('deadline', not_specified_msg.get(language, not_specified_msg['vi']))}")
        result.append("")
    
    return "\n".join(result)


def format_decisions(decisions, language="vi"):
    """Format decisions for display."""
    no_decisions_msg = {
        "vi": "Không tìm thấy quyết định",
        "en": "No decisions found",
        "ja": "決定が見つかりません",
        "ko": "결정을 찾을 수 없습니다",
        "zh": "未找到决定"
    }
    context_labels = {
        "vi": "Bối cảnh",
        "en": "Context",
        "ja": "文脈",
        "ko": "맥락",
        "zh": "背景"
    }
    
    if not decisions:
        return no_decisions_msg.get(language, no_decisions_msg["vi"])
    
    result = []
    for i, decision in enumerate(decisions, 1):
        result.append(f"**{i}. {decision.get('decision', 'N/A')}**")
        result.append(f"   📝 {context_labels.get(language, context_labels['vi'])}: {decision.get('context', 'N/A')}")
        result.append("")
    
    return "\n".join(result)


def export_to_txt():
    """Export analysis results to TXT file."""
    global last_summary, last_topics, last_actions, last_decisions, current_language
    
    if not last_summary:
        return None
    
    # Get labels based on language
    labels = {
        "vi": {
            "title": "BÁO CÁO PHÂN TÍCH CUỘC HỌP",
            "summary": "TÓM TẮT CUỘC HỌP",
            "topics": "CHỦ ĐỀ CHÍNH",
            "actions": "ACTION ITEMS",
            "decisions": "QUYẾT ĐỊNH QUAN TRỌNG",
            "task": "Nhiệm vụ",
            "assignee": "Người phụ trách",
            "deadline": "Deadline",
            "decision": "Quyết định",
            "context": "Bối cảnh"
        },
        "en": {
            "title": "MEETING ANALYSIS REPORT",
            "summary": "MEETING SUMMARY",
            "topics": "MAIN TOPICS",
            "actions": "ACTION ITEMS",
            "decisions": "IMPORTANT DECISIONS",
            "task": "Task",
            "assignee": "Assignee",
            "deadline": "Deadline",
            "decision": "Decision",
            "context": "Context"
        },
        "ja": {
            "title": "会議分析レポート",
            "summary": "会議要約",
            "topics": "主要トピック",
            "actions": "アクションアイテム",
            "decisions": "重要な決定",
            "task": "タスク",
            "assignee": "担当者",
            "deadline": "期限",
            "decision": "決定",
            "context": "文脈"
        },
        "ko": {
            "title": "회의 분석 보고서",
            "summary": "회의 요약",
            "topics": "주요 주제",
            "actions": "액션 아이템",
            "decisions": "중요한 결정",
            "task": "작업",
            "assignee": "담당자",
            "deadline": "마감일",
            "decision": "결정",
            "context": "맥락"
        },
        "zh": {
            "title": "会议分析报告",
            "summary": "会议摘要",
            "topics": "主要主题",
            "actions": "行动项",
            "decisions": "重要决定",
            "task": "任务",
            "assignee": "负责人",
            "deadline": "截止日期",
            "decision": "决定",
            "context": "背景"
        }
    }
    
    lang = labels.get(current_language, labels["vi"])
    
    # Create content
    content = []
    content.append("=" * 80)
    content.append(lang["title"].center(80))
    content.append("=" * 80)
    content.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("=" * 80)
    
    # Summary
    content.append(f"\n{lang['summary']}")
    content.append("-" * 80)
    content.append(last_summary)
    
    # Topics
    if last_topics:
        content.append(f"\n\n{lang['topics']}")
        content.append("-" * 80)
        for i, topic in enumerate(last_topics, 1):
            content.append(f"\n{i}. {topic.get('topic', 'N/A')}")
            content.append(f"   {topic.get('description', '')}")
    
    # Action Items
    if last_actions:
        content.append(f"\n\n{lang['actions']}")
        content.append("-" * 80)
        for i, action in enumerate(last_actions, 1):
            content.append(f"\n{i}. {lang['task']}: {action.get('task', 'N/A')}")
            content.append(f"   {lang['assignee']}: {action.get('assignee', 'N/A')}")
            content.append(f"   {lang['deadline']}: {action.get('deadline', 'N/A')}")
    
    # Decisions
    if last_decisions:
        content.append(f"\n\n{lang['decisions']}")
        content.append("-" * 80)
        for i, decision in enumerate(last_decisions, 1):
            content.append(f"\n{i}. {lang['decision']}: {decision.get('decision', 'N/A')}")
            content.append(f"   {lang['context']}: {decision.get('context', 'N/A')}")
    
    content.append("\n\n" + "=" * 80)
    
    # Save to file
    filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = Path(filename)
    filepath.write_text("\n".join(content), encoding='utf-8')
    
    return str(filepath)


def export_to_docx():
    """Export analysis results to DOCX file."""
    global last_summary, last_topics, last_actions, last_decisions, current_language
    
    if not last_summary:
        return None
    
    # Get labels based on language
    labels = {
        "vi": {
            "title": "BÁO CÁO PHÂN TÍCH CUỘC HỌP",
            "summary": "TÓM TẮT CUỘC HỌP",
            "topics": "CHỦ ĐỀ CHÍNH",
            "actions": "ACTION ITEMS",
            "decisions": "QUYẾT ĐỊNH QUAN TRỌNG",
            "task": "Nhiệm vụ",
            "assignee": "Người phụ trách",
            "deadline": "Deadline",
            "decision": "Quyết định",
            "context": "Bối cảnh"
        },
        "en": {
            "title": "MEETING ANALYSIS REPORT",
            "summary": "MEETING SUMMARY",
            "topics": "MAIN TOPICS",
            "actions": "ACTION ITEMS",
            "decisions": "IMPORTANT DECISIONS",
            "task": "Task",
            "assignee": "Assignee",
            "deadline": "Deadline",
            "decision": "Decision",
            "context": "Context"
        },
        "ja": {
            "title": "会議分析レポート",
            "summary": "会議要約",
            "topics": "主要トピック",
            "actions": "アクションアイテム",
            "decisions": "重要な決定",
            "task": "タスク",
            "assignee": "担当者",
            "deadline": "期限",
            "decision": "決定",
            "context": "文脈"
        },
        "ko": {
            "title": "회의 분석 보고서",
            "summary": "회의 요약",
            "topics": "주요 주제",
            "actions": "액션 아이템",
            "decisions": "중요한 결정",
            "task": "작업",
            "assignee": "담당자",
            "deadline": "마감일",
            "decision": "결정",
            "context": "맥락"
        },
        "zh": {
            "title": "会议分析报告",
            "summary": "会议摘要",
            "topics": "主要主题",
            "actions": "行动项",
            "decisions": "重要决定",
            "task": "任务",
            "assignee": "负责人",
            "deadline": "截止日期",
            "decision": "决定",
            "context": "背景"
        }
    }
    
    lang = labels.get(current_language, labels["vi"])
    
    # Create document
    doc = Document()
    
    # Title
    title = doc.add_heading(lang["title"], 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Date
    date_para = doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Summary
    doc.add_heading(lang["summary"], 1)
    doc.add_paragraph(last_summary)
    
    # Topics
    if last_topics:
        doc.add_heading(lang["topics"], 1)
        for i, topic in enumerate(last_topics, 1):
            p = doc.add_paragraph(style='List Number')
            p.add_run(f"{topic.get('topic', 'N/A')}").bold = True
            doc.add_paragraph(topic.get('description', ''), style='List Bullet 2')
    
    # Action Items
    if last_actions:
        doc.add_heading(lang["actions"], 1)
        for i, action in enumerate(last_actions, 1):
            p = doc.add_paragraph(style='List Number')
            p.add_run(f"{action.get('task', 'N/A')}").bold = True
            doc.add_paragraph(f"{lang['assignee']}: {action.get('assignee', 'N/A')}", style='List Bullet 2')
            doc.add_paragraph(f"{lang['deadline']}: {action.get('deadline', 'N/A')}", style='List Bullet 2')
    
    # Decisions
    if last_decisions:
        doc.add_heading(lang["decisions"], 1)
        for i, decision in enumerate(last_decisions, 1):
            p = doc.add_paragraph(style='List Number')
            p.add_run(f"{decision.get('decision', 'N/A')}").bold = True
            doc.add_paragraph(f"{lang['context']}: {decision.get('context', 'N/A')}", style='List Bullet 2')
    
    # Save to file
    filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    filepath = Path(filename)
    doc.save(str(filepath))
    
    return str(filepath)


# Simple and clean Gradio interface
with gr.Blocks(title="Meeting Transcript Chatbot", theme=gr.themes.Default()) as demo:
    
    gr.Markdown("""
    # 💬 Meeting Transcript Chatbot
    ### Phân tích cuộc họp bằng AI
    """)
    

    
    # Step 1: Upload
    gr.Markdown("## 📤 Bước 1: Upload File Transcript")
    with gr.Row():
        file_input = gr.File(
            label="Chọn file TXT hoặc DOCX",
            file_types=[".txt", ".docx"]
        )
        process_btn = gr.Button("🚀 Xử lý Transcript", variant="primary", size="lg")
    
    status_output = gr.Textbox(label="Trạng thái", interactive=False)
    
    gr.Markdown("---")
    
    # Step 2: View Results
    gr.Markdown("## 📊 Bước 2: Xem Kết quả Phân tích")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📝 Tóm tắt Cuộc họp")
            summary_output = gr.Textbox(
                lines=5,
                interactive=False,
                placeholder="Tóm tắt sẽ hiển thị ở đây sau khi xử lý..."
            )
        
        with gr.Column():
            gr.Markdown("### ✅ Action Items")
            actions_output = gr.Markdown("_Chưa có dữ liệu_")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎯 Chủ đề Chính")
            topics_output = gr.Markdown("_Chưa có dữ liệu_")
        
        with gr.Column():
            gr.Markdown("### 🎯 Quyết định Quan trọng")
            decisions_output = gr.Markdown("_Chưa có dữ liệu_")
    
    gr.Markdown("---")
    
    # Step 3: Export Results
    gr.Markdown("## 💾 Bước 3: Xuất Kết quả")
    
    with gr.Row():
        export_txt_btn = gr.Button("📄 Xuất file TXT", variant="secondary", size="lg", scale=1)
        export_docx_btn = gr.Button("📝 Xuất file DOCX", variant="secondary", size="lg", scale=1)
    
    export_output = gr.File(label="File đã xuất")
    
    gr.Markdown("""
    ---
    **💡 Hướng dẫn:** Upload file → Nhấn "Xử lý" → Xem kết quả → Xuất file
    """)
    
    # Event handlers
    process_btn.click(
        fn=process_file,
        inputs=[file_input],
        outputs=[status_output, summary_output, topics_output, actions_output, decisions_output]
    )
    
    export_txt_btn.click(
        fn=export_to_txt,
        outputs=[export_output]
    )
    
    export_docx_btn.click(
        fn=export_to_docx,
        outputs=[export_output]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False
    )
