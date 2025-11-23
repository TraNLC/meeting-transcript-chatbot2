"""Final Gradio UI - Best of both worlds: Working logic + Beautiful design."""

import gradio as gr
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import Settings
from src.data import TranscriptLoader, TranscriptPreprocessor
from src.data.history_manager import HistoryManager
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
current_filename = ""
history_manager = HistoryManager()


def process_file(file, meeting_type, output_language):
    """Process uploaded transcript file - Using working logic from gradio_app.py."""
    global chatbot, transcript_text, last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    provider = "gemini"
    model = "gemini-2.5-flash"
    language = output_language
    
    upload_msg = {
        "vi": "❌ Vui lòng upload file!",
        "en": "❌ Please upload a file!",
        "ja": "❌ ファイルをアップロードしてください！",
        "ko": "❌ 파일을 업로드해주세요!",
        "zh-CN": "❌ 请上传文件！",
        "es": "❌ Por favor sube un archivo!",
        "fr": "❌ Veuillez télécharger un fichier!",
        "de": "❌ Bitte laden Sie eine Datei hoch!"
    }
    
    if file is None:
        return upload_msg.get(language, upload_msg["vi"]), "", "", "", ""
    
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
        
        # Initialize LLM and chatbot
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
        action_items = chatbot.extract_action_items_initially()
        decisions = chatbot.extract_decisions()
        
        # Save results globally
        last_summary = summary
        last_topics = topics
        last_actions = action_items
        last_decisions = decisions
        current_filename = Path(file.name).name
        
        # Save to history
        try:
            history_manager.save_analysis(
                filename=file.name,
                summary=summary,
                topics=topics,
                action_items=action_items,
                decisions=decisions,
                metadata={"language": language, "meeting_type": meeting_type}
            )
        except Exception as e:
            print(f"Failed to save history: {e}")
        
        # Format outputs
        topics_text = format_topics(topics, language)
        actions_text = format_actions(action_items, language)
        decisions_text = format_decisions(decisions, language)
        
        success_msgs = {
            "vi": f"✅ Đã xử lý: {current_filename} | Loại: {meeting_type} | Ngôn ngữ: {language}",
            "en": f"✅ Processed: {current_filename} | Type: {meeting_type} | Language: {language}",
            "ja": f"✅ 処理完了: {current_filename} | タイプ: {meeting_type} | 言語: {language}",
            "ko": f"✅ 처리 완료: {current_filename} | 유형: {meeting_type} | 언어: {language}",
            "zh-CN": f"✅ 已处理: {current_filename} | 类型: {meeting_type} | 语言: {language}",
            "es": f"✅ Procesado: {current_filename} | Tipo: {meeting_type} | Idioma: {language}",
            "fr": f"✅ Traité: {current_filename} | Type: {meeting_type} | Langue: {language}",
            "de": f"✅ Verarbeitet: {current_filename} | Typ: {meeting_type} | Sprache: {language}"
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
            "zh-CN": "❌ 错误:",
            "es": "❌ Error:",
            "fr": "❌ Erreur:",
            "de": "❌ Fehler:"
        }
        return f"{error_prefixes.get(language, error_prefixes['vi'])} {str(e)}", "", "", "", ""


def format_topics(topics, language="vi"):
    """Format topics for display."""
    labels = {
        "vi": {"no_data": "_Không tìm thấy chủ đề_", "description": "Mô tả"},
        "en": {"no_data": "_No topics found_", "description": "Description"},
        "ja": {"no_data": "_トピックが見つかりません_", "description": "説明"},
        "ko": {"no_data": "_주제를 찾을 수 없습니다_", "description": "설명"},
        "zh-CN": {"no_data": "_未找到主题_", "description": "描述"},
        "es": {"no_data": "_No se encontraron temas_", "description": "Descripción"},
        "fr": {"no_data": "_Aucun sujet trouvé_", "description": "Description"},
        "de": {"no_data": "_Keine Themen gefunden_", "description": "Beschreibung"}
    }
    lang = labels.get(language, labels["vi"])
    
    if not topics:
        return lang["no_data"]
    
    result = []
    for i, topic in enumerate(topics, 1):
        result.append(f"### {i}. {topic.get('topic', 'N/A')}")
        result.append(f"{topic.get('description', '')}\n")
    
    return "\n".join(result)


def format_actions(actions, language="vi"):
    """Format action items for display."""
    labels = {
        "vi": {
            "no_data": "_Không có action items_", 
            "assignee": "👤 Người phụ trách", 
            "deadline": "📅 Hạn chót",
            "not_assigned": "Chưa phân công",
            "not_specified": "Chưa xác định"
        },
        "en": {
            "no_data": "_No action items_", 
            "assignee": "👤 Assignee", 
            "deadline": "📅 Deadline",
            "not_assigned": "Not assigned",
            "not_specified": "Not specified"
        },
        "ja": {
            "no_data": "_アクションアイテムなし_", 
            "assignee": "👤 担当者", 
            "deadline": "📅 期限",
            "not_assigned": "未割り当て",
            "not_specified": "未指定"
        },
        "ko": {
            "no_data": "_액션 아이템 없음_", 
            "assignee": "👤 담당자", 
            "deadline": "📅 마감일",
            "not_assigned": "미할당",
            "not_specified": "미지정"
        },
        "zh-CN": {
            "no_data": "_无行动项_", 
            "assignee": "👤 负责人", 
            "deadline": "📅 截止日期",
            "not_assigned": "未分配",
            "not_specified": "未指定"
        },
        "es": {
            "no_data": "_Sin elementos de acción_", 
            "assignee": "👤 Responsable", 
            "deadline": "📅 Fecha límite",
            "not_assigned": "No asignado",
            "not_specified": "No especificado"
        },
        "fr": {
            "no_data": "_Aucun élément d'action_", 
            "assignee": "👤 Responsable", 
            "deadline": "📅 Date limite",
            "not_assigned": "Non assigné",
            "not_specified": "Non spécifié"
        },
        "de": {
            "no_data": "_Keine Aktionselemente_", 
            "assignee": "👤 Verantwortlich", 
            "deadline": "📅 Frist",
            "not_assigned": "Nicht zugewiesen",
            "not_specified": "Nicht angegeben"
        }
    }
    lang = labels.get(language, labels["vi"])
    
    if not actions:
        return lang["no_data"]
    
    result = []
    for i, item in enumerate(actions, 1):
        task = item.get('task', 'N/A')
        assignee = item.get('assignee', lang['not_assigned'])
        deadline = item.get('deadline', lang['not_specified'])
        
        result.append(f"### {i}. {task}")
        result.append(f"- {lang['assignee']}: **{assignee}**")
        result.append(f"- {lang['deadline']}: {deadline}\n")
    
    return "\n".join(result)


def format_decisions(decisions, language="vi"):
    """Format decisions for display."""
    labels = {
        "vi": {
            "no_data": "_Không có quyết định_", 
            "context": "📝 Bối cảnh",
            "no_context": "Không có bối cảnh"
        },
        "en": {
            "no_data": "_No decisions_", 
            "context": "📝 Context",
            "no_context": "No context"
        },
        "ja": {
            "no_data": "_決定なし_", 
            "context": "📝 文脈",
            "no_context": "文脈なし"
        },
        "ko": {
            "no_data": "_결정 없음_", 
            "context": "📝 맥락",
            "no_context": "맥락 없음"
        },
        "zh-CN": {
            "no_data": "_无决定_", 
            "context": "📝 背景",
            "no_context": "无背景"
        },
        "es": {
            "no_data": "_Sin decisiones_", 
            "context": "📝 Contexto",
            "no_context": "Sin contexto"
        },
        "fr": {
            "no_data": "_Aucune décision_", 
            "context": "📝 Contexte",
            "no_context": "Pas de contexte"
        },
        "de": {
            "no_data": "_Keine Entscheidungen_", 
            "context": "📝 Kontext",
            "no_context": "Kein Kontext"
        }
    }
    lang = labels.get(language, labels["vi"])
    
    if not decisions:
        return lang["no_data"]
    
    result = []
    for i, decision in enumerate(decisions, 1):
        decision_text = decision.get('decision', 'N/A')
        context = decision.get('context', lang['no_context'])
        
        result.append(f"### {i}. {decision_text}")
        result.append(f"- {lang['context']}: {context}\n")
    
    return "\n".join(result)


def chat_with_ai(message, history):
    """Chat with AI."""
    global chatbot
    
    if history is None:
        history = []
    
    if not chatbot:
        new_history = history.copy()
        new_history.append([message, "⚠️ Vui lòng xử lý transcript trước!"])
        return new_history
    
    try:
        result = chatbot.ask_question(message)
        response = result.get("answer", "Xin lỗi, tôi không hiểu câu hỏi.")
        
        new_history = history.copy()
        new_history.append([message, response])
        return new_history
    except Exception as e:
        new_history = history.copy()
        new_history.append([message, f"❌ Lỗi: {str(e)}"])
        return new_history


def export_to_txt():
    """Export analysis results to TXT file."""
    global last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    if not last_summary:
        return None
    
    labels = {
        "vi": {"title": "BÁO CÁO PHÂN TÍCH CUỘC HỌP", "summary": "TÓM TẮT", "topics": "CHỦ ĐỀ", "actions": "ACTION ITEMS", "decisions": "QUYẾT ĐỊNH"},
        "en": {"title": "MEETING ANALYSIS REPORT", "summary": "SUMMARY", "topics": "TOPICS", "actions": "ACTION ITEMS", "decisions": "DECISIONS"}
    }
    lang = labels.get(current_language, labels["vi"])
    
    content = []
    content.append("=" * 80)
    content.append(lang["title"].center(80))
    content.append("=" * 80)
    content.append(f"\nFile: {current_filename}")
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("=" * 80)
    
    content.append(f"\n{lang['summary']}")
    content.append("-" * 80)
    content.append(last_summary)
    
    if last_topics:
        content.append(f"\n\n{lang['topics']}")
        content.append("-" * 80)
        for i, topic in enumerate(last_topics, 1):
            content.append(f"\n{i}. {topic.get('topic', 'N/A')}")
            content.append(f"   {topic.get('description', '')}")
    
    if last_actions:
        content.append(f"\n\n{lang['actions']}")
        content.append("-" * 80)
        for i, action in enumerate(last_actions, 1):
            content.append(f"\n{i}. {action.get('task', 'N/A')}")
            content.append(f"   Assignee: {action.get('assignee', 'N/A')}")
            content.append(f"   Deadline: {action.get('deadline', 'N/A')}")
    
    if last_decisions:
        content.append(f"\n\n{lang['decisions']}")
        content.append("-" * 80)
        for i, decision in enumerate(last_decisions, 1):
            content.append(f"\n{i}. {decision.get('decision', 'N/A')}")
            content.append(f"   Context: {decision.get('context', 'N/A')}")
    
    content.append("\n\n" + "=" * 80)
    
    filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = Path(filename)
    filepath.write_text("\n".join(content), encoding='utf-8')
    
    return str(filepath)


def refresh_history():
    """Refresh history dropdown."""
    history_list = history_manager.list_history(limit=20)
    
    if not history_list:
        return gr.Dropdown(choices=[], value=None), "_Chưa có lịch sử_"
    
    choices = [
        (f"{item['timestamp'][:10]} - {item['original_file']}", item['id'])
        for item in history_list
    ]
    
    info = f"📊 Tìm thấy {len(history_list)} phân tích đã lưu"
    
    return gr.Dropdown(choices=choices, value=None), info


def load_history(history_id):
    """Load analysis from history."""
    global last_summary, last_topics, last_actions, last_decisions, current_language
    
    if not history_id:
        return "⚠️ Vui lòng chọn phân tích từ danh sách", "", "", "", ""
    
    data = history_manager.load_analysis(history_id)
    
    if not data:
        return "❌ Không tìm thấy phân tích", "", "", "", ""
    
    # Load data
    last_summary = data.get("summary", "")
    last_topics = data.get("topics", [])
    last_actions = data.get("action_items", [])
    last_decisions = data.get("decisions", [])
    current_language = data.get("metadata", {}).get("language", "vi")
    
    # Format outputs
    topics_text = format_topics(last_topics, current_language)
    actions_text = format_actions(last_actions, current_language)
    decisions_text = format_decisions(last_decisions, current_language)
    
    status = f"✅ Đã tải phân tích: {data.get('original_file')} ({data.get('timestamp')[:10]})"
    
    return status, last_summary, topics_text, actions_text, decisions_text


def export_to_docx():
    """Export analysis results to DOCX file."""
    global last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    if not last_summary:
        return None
    
    try:
        from docx import Document
        from docx.shared import Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        doc = Document()
        
        # Title
        title = doc.add_heading("Meeting Analysis Report", 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Date
        date_para = doc.add_paragraph(f"File: {current_filename}")
        date_para.add_run(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()
        
        # Summary
        doc.add_heading("Summary", 1)
        doc.add_paragraph(last_summary)
        
        # Topics
        if last_topics:
            doc.add_heading("Main Topics", 1)
            for i, topic in enumerate(last_topics, 1):
                p = doc.add_paragraph(style='List Number')
                p.add_run(f"{topic.get('topic', 'N/A')}").bold = True
                doc.add_paragraph(topic.get('description', ''), style='List Bullet 2')
        
        # Action Items
        if last_actions:
            doc.add_heading("Action Items", 1)
            for i, action in enumerate(last_actions, 1):
                p = doc.add_paragraph(style='List Number')
                p.add_run(f"{action.get('task', 'N/A')}").bold = True
                doc.add_paragraph(f"Assignee: {action.get('assignee', 'N/A')}", style='List Bullet 2')
                doc.add_paragraph(f"Deadline: {action.get('deadline', 'N/A')}", style='List Bullet 2')
        
        # Decisions
        if last_decisions:
            doc.add_heading("Important Decisions", 1)
            for i, decision in enumerate(last_decisions, 1):
                p = doc.add_paragraph(style='List Number')
                p.add_run(f"{decision.get('decision', 'N/A')}").bold = True
                doc.add_paragraph(f"Context: {decision.get('context', 'N/A')}", style='List Bullet 2')
        
        filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = Path(filename)
        doc.save(str(filepath))
        
        return str(filepath)
    except Exception as e:
        print(f"Error exporting DOCX: {e}")
        return None


# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main-header {
    text-align: center;
    padding: 2.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.95;
}
"""

# Build UI
with gr.Blocks(css=custom_css, title="Meeting Analyzer Pro", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🎯 Meeting Transcript Analyzer Pro</h1>
        <p>Phân tích cuộc họp thông minh với AI - Hỗ trợ đa ngôn ngữ</p>
    </div>
    """)
    
    # History section
    with gr.Accordion("📚 Lịch sử phân tích", open=False):
        with gr.Row():
            history_dropdown = gr.Dropdown(
                label="Chọn phân tích đã lưu",
                choices=[],
                interactive=True,
                scale=3
            )
            refresh_history_btn = gr.Button("🔄 Làm mới", scale=1)
            load_history_btn = gr.Button("📂 Tải lại", variant="primary", scale=1)
        
        history_info = gr.Markdown("_Chưa có lịch sử_")
    
    # Main content in tabs
    with gr.Tabs() as tabs:
        
        # Tab 1: Upload & Analyze
        with gr.Tab("📤 Upload & Phân Tích"):
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### 📁 Upload Transcript")
                    file_input = gr.File(
                        label="Chọn file transcript (TXT, DOCX)",
                        file_types=[".txt", ".docx"]
                    )
                    
                    with gr.Row():
                        meeting_type = gr.Dropdown(
                            label="🎯 Loại Cuộc Họp",
                            choices=[
                                ("📋 Meeting - Cuộc họp thông thường", "meeting"),
                                ("🎓 Workshop - Hội thảo/Đào tạo", "workshop"),
                                ("💡 Brainstorming - Động não", "brainstorming")
                            ],
                            value="meeting"
                        )
                        
                        output_lang = gr.Dropdown(
                            label="🌍 Ngôn Ngữ Output",
                            choices=[
                                ("🇻🇳 Tiếng Việt", "vi"),
                                ("🇬🇧 English", "en"),
                                ("🇯🇵 日本語", "ja"),
                                ("🇰🇷 한국어", "ko"),
                                ("🇨🇳 中文", "zh-CN"),
                                ("🇪🇸 Español", "es"),
                                ("🇫🇷 Français", "fr"),
                                ("🇩🇪 Deutsch", "de")
                            ],
                            value="vi"
                        )
                    
                    process_btn = gr.Button(
                        "🚀 Phân Tích Ngay",
                        variant="primary",
                        size="lg"
                    )
                    
                    status_box = gr.Textbox(
                        label="Trạng thái",
                        interactive=False,
                        lines=2
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### 💡 Hướng Dẫn
                    
                    **Bước 1:** Upload file transcript
                    
                    **Bước 2:** Chọn loại cuộc họp
                    
                    **Bước 3:** Chọn ngôn ngữ output
                    
                    **Bước 4:** Click "Phân Tích Ngay"
                    
                    ---
                    
                    ✨ **Tính năng:**
                    - AI tự động tóm tắt
                    - Trích xuất chủ đề chính
                    - Phát hiện action items
                    - Ghi nhận quyết định quan trọng
                    - Hỗ trợ 8 ngôn ngữ
                    """)
            
            gr.Markdown("---")
            
            # Results section
            gr.Markdown("## 📊 Kết Quả Phân Tích")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📝 Tóm Tắt Cuộc Họp")
                    summary_output = gr.Textbox(
                        lines=6,
                        interactive=False,
                        placeholder="Tóm tắt sẽ hiển thị ở đây..."
                    )
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🎯 Chủ Đề Chính")
                    topics_output = gr.Markdown("_Chưa có dữ liệu_")
                
                with gr.Column():
                    gr.Markdown("### ✅ Action Items")
                    actions_output = gr.Markdown("_Chưa có dữ liệu_")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🎯 Quyết Định Quan Trọng")
                    decisions_output = gr.Markdown("_Chưa có dữ liệu_")
        
        # Tab 2: Export Results
        with gr.Tab("💾 Xuất Kết Quả"):
            gr.Markdown("### 📥 Tải xuống kết quả phân tích")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    #### 📄 Xuất file TXT
                    - Format đơn giản, dễ đọc
                    - Phù hợp để chia sẻ qua email
                    - Mở được trên mọi thiết bị
                    """)
                    export_txt_btn = gr.Button("📄 Xuất TXT", size="lg", variant="primary")
                
                with gr.Column():
                    gr.Markdown("""
                    #### 📝 Xuất file DOCX
                    - Format chuyên nghiệp
                    - Có thể chỉnh sửa trong Word
                    - Phù hợp cho báo cáo
                    """)
                    export_docx_btn = gr.Button("📝 Xuất DOCX", size="lg", variant="primary")
            
            export_file = gr.File(label="File đã xuất")
            
            gr.Markdown("""
            ---
            **💡 Lưu ý:**
            - Cần xử lý transcript trước khi xuất
            - File sẽ được lưu với timestamp
            - Hỗ trợ đa ngôn ngữ
            """)
        
        # Tab 3: Chat with AI
        with gr.Tab("💬 Chat với AI"):
            gr.Markdown("### 🤖 Hỏi đáp thông minh về cuộc họp")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot_display = gr.Chatbot(
                        height=500,
                        label="Cuộc trò chuyện"
                    )
                    
                    with gr.Row():
                        chat_input = gr.Textbox(
                            placeholder="Nhập câu hỏi của bạn...",
                            show_label=False,
                            scale=4
                        )
                        send_btn = gr.Button("📤 Gửi", scale=1, variant="primary")
                    
                    clear_btn = gr.Button("🗑️ Xóa lịch sử", size="sm")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 💡 Câu Hỏi Gợi Ý")
                    
                    q1 = gr.Button("📋 Tóm tắt cuộc họp", size="sm")
                    q2 = gr.Button("👥 Ai tham gia?", size="sm")
                    q3 = gr.Button("✅ Action items là gì?", size="sm")
                    q4 = gr.Button("🎯 Quyết định quan trọng?", size="sm")
                    q5 = gr.Button("📊 Chủ đề chính?", size="sm")
                    
                    gr.Markdown("""
                    ---
                    **💬 Bạn có thể hỏi:**
                    - Tóm tắt cuộc họp
                    - Ai tham gia meeting?
                    - Action items là gì?
                    - Quyết định nào được đưa ra?
                    - Chủ đề chính là gì?
                    """)
    
    # Footer
    gr.Markdown("""
    ---
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by Gemini AI | 🌍 Multi-language Support | 🎯 Smart Analysis</p>
        <p style="font-size: 0.9em;">Version 3.0 - Final Edition</p>
    </div>
    """)
    
    # Event handlers
    
    # History handlers
    refresh_history_btn.click(
        fn=refresh_history,
        outputs=[history_dropdown, history_info]
    )
    
    load_history_btn.click(
        fn=load_history,
        inputs=[history_dropdown],
        outputs=[status_box, summary_output, topics_output, actions_output, decisions_output]
    )
    
    # Auto-refresh history on page load
    demo.load(
        fn=refresh_history,
        outputs=[history_dropdown, history_info]
    )
    
    # Process handler
    process_btn.click(
        fn=process_file,
        inputs=[file_input, meeting_type, output_lang],
        outputs=[status_box, summary_output, topics_output, actions_output, decisions_output]
    ).then(
        fn=refresh_history,  # Refresh history after processing
        outputs=[history_dropdown, history_info]
    )
    
    # Export handlers
    export_txt_btn.click(
        fn=export_to_txt,
        outputs=[export_file]
    )
    
    export_docx_btn.click(
        fn=export_to_docx,
        outputs=[export_file]
    )
    
    # Chat handlers
    send_btn.click(
        fn=chat_with_ai,
        inputs=[chat_input, chatbot_display],
        outputs=[chatbot_display]
    ).then(
        fn=lambda: "",
        outputs=[chat_input]
    )
    
    chat_input.submit(
        fn=chat_with_ai,
        inputs=[chat_input, chatbot_display],
        outputs=[chatbot_display]
    ).then(
        fn=lambda: "",
        outputs=[chat_input]
    )
    
    clear_btn.click(
        fn=lambda: [],
        outputs=[chatbot_display]
    )
    
    # Quick questions
    def send_q(q, h):
        if h is None:
            h = []
        return chat_with_ai(q, h)
    
    q1.click(fn=lambda h: send_q("Tóm tắt cuộc họp này", h), inputs=[chatbot_display], outputs=[chatbot_display])
    q2.click(fn=lambda h: send_q("Ai tham gia cuộc họp?", h), inputs=[chatbot_display], outputs=[chatbot_display])
    q3.click(fn=lambda h: send_q("Action items là gì?", h), inputs=[chatbot_display], outputs=[chatbot_display])
    q4.click(fn=lambda h: send_q("Những quyết định quan trọng nào được đưa ra?", h), inputs=[chatbot_display], outputs=[chatbot_display])
    q5.click(fn=lambda h: send_q("Chủ đề chính của cuộc họp là gì?", h), inputs=[chatbot_display], outputs=[chatbot_display])


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=False
    )
