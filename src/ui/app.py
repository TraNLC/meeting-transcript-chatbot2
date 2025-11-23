"""Streamlit UI for Meeting Transcript Chatbot."""

import streamlit as st
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import Settings
from src.data import TranscriptLoader, TranscriptPreprocessor
from src.llm import LLMManager
from src.rag import Chatbot


# Page configuration
st.set_page_config(
    page_title="Meeting Transcript Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border-color: #FF6B6B;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .info-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    h1 {
        color: #FF4B4B;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    if "transcript_loaded" not in st.session_state:
        st.session_state.transcript_loaded = False
    if "transcript_text" not in st.session_state:
        st.session_state.transcript_text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "action_items" not in st.session_state:
        st.session_state.action_items = []
    if "decisions" not in st.session_state:
        st.session_state.decisions = []
    if "topics" not in st.session_state:
        st.session_state.topics = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def process_transcript(uploaded_file):
    """Process uploaded transcript file."""
    try:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(uploaded_file.name).suffix
        ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # Load transcript
        with st.spinner("📖 Đang đọc file..."):
            loader = TranscriptLoader()
            transcript = loader.load_file(tmp_path)
            
            # Clean and truncate transcript
            preprocessor = TranscriptPreprocessor()
            transcript = preprocessor.clean_text(transcript)
            transcript = preprocessor.truncate_text(transcript, max_length=15000)
            
            st.session_state.transcript_text = transcript

        # Initialize LLM
        with st.spinner("🤖 Đang khởi tạo AI..."):
            llm_manager = LLMManager(
                model_name=Settings.LLM_MODEL,
                temperature=Settings.TEMPERATURE,
                max_tokens=Settings.MAX_TOKENS,
            )

            # Initialize chatbot
            st.session_state.chatbot = Chatbot(
                llm_manager=llm_manager,
                transcript=transcript
            )

        # Generate summary
        with st.spinner("📝 Đang tạo tóm tắt..."):
            summary = st.session_state.chatbot.generate_summary()
            st.session_state.summary = summary

        # Extract key information
        with st.spinner("🔎 Đang trích xuất thông tin quan trọng..."):
            st.session_state.topics = st.session_state.chatbot.extract_topics()
            st.session_state.action_items = st.session_state.chatbot.extract_action_items_initially()
            st.session_state.decisions = st.session_state.chatbot.extract_decisions()

        st.session_state.transcript_loaded = True
        st.session_state.chat_history = []

        return True, "✅ Transcript đã được xử lý thành công!"

    except Exception as e:
        return False, f"❌ Lỗi: {str(e)}"


def main():
    """Main application."""
    initialize_session_state()

    # Header
    st.title("💬 Meeting Transcript Chatbot")
    st.markdown(
        "### Trợ lý AI thông minh giúp bạn phân tích và trả lời câu hỏi về cuộc họp"
    )
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/000000/chat.png",
            width=80,
        )
        st.title("📁 Upload Transcript")
        st.markdown("Tải lên file transcript cuộc họp của bạn")

        uploaded_file = st.file_uploader(
            "Chọn file",
            type=["txt", "docx"],
            help="Hỗ trợ file TXT và DOCX",
            label_visibility="collapsed",
        )

        if uploaded_file:
            st.success(f"📄 {uploaded_file.name}")

            if st.button("🚀 Xử lý Transcript", use_container_width=True):
                success, message = process_transcript(uploaded_file)
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

        st.markdown("---")

        # Settings
        with st.expander("⚙️ Cài đặt"):
            st.info(f"**Model:** {Settings.LLM_MODEL}")
            st.info(f"**Temperature:** {Settings.TEMPERATURE}")
            st.info(f"**Max Tokens:** {Settings.MAX_TOKENS}")

        st.markdown("---")
        st.markdown("### 📖 Hướng dẫn")
        st.markdown(
            """
        1. Upload file transcript (.txt hoặc .docx)
        2. Nhấn "Xử lý Transcript"
        3. Xem tóm tắt và thông tin quan trọng
        4. Đặt câu hỏi về cuộc họp
        
        **Lưu ý:** Sử dụng GPT-4 cho kết quả tốt nhất!
        """
        )

    # Main content
    if not st.session_state.transcript_loaded:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "https://img.icons8.com/clouds/400/000000/meeting.png",
                width=300,
            )
            st.markdown(
                """
                <div style='text-align: center'>
                    <h2>Chào mừng đến với Meeting Transcript Chatbot!</h2>
                    <p style='font-size: 1.2em; color: #666;'>
                        Hãy bắt đầu bằng cách upload transcript cuộc họp ở sidebar bên trái 👈
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### ✨ Tính năng")
            col_a, col_b = st.columns(2)
            with col_a:
                st.info("📝 **Tóm tắt tự động**\n\nTạo tóm tắt ngắn gọn về cuộc họp")
                st.info(
                    "✅ **Trích xuất Action Items**\n\nTìm tất cả nhiệm vụ cần làm"
                )
            with col_b:
                st.info("🎯 **Phát hiện Quyết định**\n\nXác định các quyết định quan trọng")
                st.info("❓ **Hỏi & Đáp**\n\nTrả lời câu hỏi về cuộc họp")

    else:
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📝 Tóm tắt", "🔍 Thông tin Quan trọng", "💬 Hỏi & Đáp", "📄 Transcript"]
        )

        # Tab 1: Summary
        with tab1:
            st.markdown("## 📝 Tóm tắt Cuộc họp")
            st.markdown(
                f"""
                <div class='info-card'>
                    <p style='font-size: 1.1em; line-height: 1.6;'>
                        {st.session_state.summary}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Tab 2: Key Information
        with tab2:
            st.markdown("## 🔍 Thông tin Quan trọng")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎯 Chủ đề Chính")
                if st.session_state.topics:
                    for i, topic in enumerate(st.session_state.topics, 1):
                        with st.expander(f"📌 {topic.get('topic', 'N/A')}", expanded=True):
                            st.write(topic.get("description", "Không có mô tả"))
                else:
                    st.info("Không tìm thấy chủ đề rõ ràng")

                st.markdown("### 🎯 Quyết định")
                if st.session_state.decisions:
                    for i, decision in enumerate(st.session_state.decisions, 1):
                        with st.expander(
                            f"✓ {decision.get('decision', 'N/A')[:50]}...",
                            expanded=True,
                        ):
                            st.markdown(f"**Quyết định:** {decision.get('decision', 'N/A')}")
                            st.markdown(f"**Bối cảnh:** {decision.get('context', 'N/A')}")
                else:
                    st.info("Không tìm thấy quyết định")

            with col2:
                st.markdown("### ✅ Action Items")
                if st.session_state.action_items:
                    for i, item in enumerate(st.session_state.action_items, 1):
                        with st.expander(
                            f"📋 {item.get('task', 'N/A')[:50]}...", expanded=True
                        ):
                            st.markdown(f"**Nhiệm vụ:** {item.get('task', 'N/A')}")
                            st.markdown(
                                f"**Người phụ trách:** {item.get('assignee', 'Chưa phân công')}"
                            )
                            st.markdown(
                                f"**Deadline:** {item.get('deadline', 'Chưa xác định')}"
                            )
                else:
                    st.info("Không tìm thấy action items")

        # Tab 3: Q&A
        with tab3:
            st.markdown("## 💬 Hỏi & Đáp")

            # Display chat history
            for chat in st.session_state.chat_history:
                # User message
                st.markdown(
                    f"""
                    <div class='chat-message user-message'>
                        <strong>🙋 Bạn:</strong><br>
                        {chat['question']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Bot message
                st.markdown(
                    f"""
                    <div class='chat-message bot-message'>
                        <strong>🤖 Trợ lý:</strong><br>
                        {chat['answer']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Question input
            st.markdown("---")
            col1, col2 = st.columns([5, 1])

            with col1:
                question = st.text_input(
                    "Đặt câu hỏi về cuộc họp:",
                    placeholder="Ví dụ: Ai phụ trách task marketing?",
                    label_visibility="collapsed",
                )

            with col2:
                ask_button = st.button("Gửi", use_container_width=True)

            if ask_button and question:
                with st.spinner("🤔 Đang suy nghĩ..."):
                    result = st.session_state.chatbot.ask_question(question)

                    # Add to chat history in correct format for Gradio/LLM
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": result["answer"]
                    })

                    st.rerun()

            if st.button("🗑️ Xóa lịch sử chat"):
                st.session_state.chat_history = []
                st.rerun()

        # Tab 4: Original Transcript
        with tab4:
            st.markdown("## 📄 Transcript Gốc")
            st.text_area(
                "Nội dung transcript",
                st.session_state.transcript_text,
                height=500,
                label_visibility="collapsed",
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Đã xảy ra lỗi: {str(e)}")
        st.info("💡 Hãy đảm bảo bạn đã cấu hình OPENAI_API_KEY trong file .env")
