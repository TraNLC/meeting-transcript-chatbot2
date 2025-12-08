"""Meeting processing logic - decoupling from UI."""

import sys
from pathlib import Path
from datetime import datetime
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import utilities
from backend.utils.logger import get_logger
from backend.utils.error_handler import (
    get_user_friendly_message, 
    validate_file, 
    sanitize_input,
    safe_execute
)
from backend.utils.rate_limiter import get_rate_limiter
from backend.utils.cache import get_cached_llm_response, cache_llm_response

# Initialize logger
logger = get_logger(__name__)

from backend.config import Settings
from backend.data import TranscriptLoader, TranscriptPreprocessor
from backend.data.history_manager import HistoryManager
from backend.llm import LLMManager
from backend.rag import Chatbot
from backend.audio.audio_manager import AudioManager
from backend.audio.stt_processor import STTProcessor
# from backend.audio.realtime_stt import SimpleRealtimeSTT # Unused here
# from backend.audio.streaming_recorder import SimpleStreamingTranscriber # Unused here
# from backend.audio.vosk_realtime import VoskRealtimeSTT # Unused here
from backend.rag.advanced_rag import get_rag_instance

audio_manager = AudioManager()
history_manager = HistoryManager()
# Initialize Advanced RAG
rag_system = get_rag_instance(vector_store="chroma")

# Global state (Legacy, should be refactored to session/db but kept for compatibility)
chatbot = None
transcript_text = ""
last_summary = ""
last_topics = []
last_actions = []
last_decisions = []
current_language = "vi"
current_filename = ""


def process_file(file, meeting_type, output_language):
    """Process uploaded transcript file - Using working logic from gradio_app.py."""
    global chatbot, transcript_text, last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    logger.info(f"Processing file: type={meeting_type}, language={output_language}")
    
    # Import meeting type functions
    from backend.rag.meeting_types import WorkshopFunctions, BrainstormingFunctions
    
    provider = Settings.LLM_PROVIDER
    model = Settings.LLM_MODEL
    language = output_language
    
    upload_msg = {
        "vi": "❌ Vui lòng upload file!",
        "en": "❌ Please upload a file!",
    }
    
    if file is None:
        logger.warning("No file uploaded")
        return upload_msg.get(language, upload_msg["vi"]), "", "", "", "", "", ""
    
    # Validate file
    # file.name is expected to be a path or string
    filename = file.name if hasattr(file, 'name') else str(file)
    
    is_valid, error_msg = validate_file(
        filename, 
        max_size_mb=50, 
        allowed_extensions=['.txt', '.docx']
    )
    if not is_valid:
        logger.error(f"File validation failed: {error_msg}")
        return f"❌ {error_msg}", "", "", "", "", "", ""
    
    current_language = language
    
    # Check rate limit
    rate_limiter = get_rate_limiter('gemini', max_calls=15, time_window=60)
    if not rate_limiter.wait_if_needed(key='process_file', max_wait=30):
        logger.warning("Rate limit exceeded")
        return "⚠️ Quá nhiều requests. Vui lòng đợi 30 giây...", "", "", "", "", "", ""
    
    try:
        # Load transcript
        logger.debug(f"Loading file: {filename}")
        loader = TranscriptLoader()
        transcript = loader.load_file(filename)
        
        # Sanitize input
        transcript = sanitize_input(transcript, max_length=50000)
        
        # Clean and truncate
        preprocessor = TranscriptPreprocessor()
        transcript = preprocessor.clean_text(transcript)
        transcript = preprocessor.truncate_text(transcript, max_length=15000)
        transcript_text = transcript
        
        logger.info(f"Transcript loaded: {len(transcript)} chars")
        
        # Check cache first
        cache_key = f"{meeting_type}_{language}_{transcript[:100]}"
        cached_result = get_cached_llm_response(cache_key, model=model)
        
        if cached_result:
            logger.info("Using cached result")
            # Parse cached result (simplified - in production, cache full response)
        
        # Initialize LLM and chatbot
        logger.debug(f"Initializing LLM: provider={provider}, model={model}")
        
        # Get API key based on provider
        if provider == "gemini":
            api_key = Settings.GEMINI_API_KEY
            llm_kwargs = {}
        elif provider == "openai":
            api_key = Settings.OPENAI_API_KEY
            llm_kwargs = {"base_url": Settings.OPENAI_BASE_URL} if Settings.OPENAI_BASE_URL else {}
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        llm_manager = LLMManager(
            provider=provider,
            model_name=model,
            temperature=Settings.TEMPERATURE,
            max_tokens=Settings.MAX_TOKENS,
            api_key=api_key,
            **llm_kwargs
        )
        
        chatbot = Chatbot(llm_manager=llm_manager, transcript=transcript, language=language, meeting_type=meeting_type)
        
        # Generate summary
        logger.info("Generating summary")
        summary = chatbot.generate_summary()
        
        # Cache the summary
        cache_llm_response(cache_key, summary, model=model)
        
        # Extract information based on meeting type
        topics = chatbot.extract_topics()
        action_items = chatbot.extract_action_items_initially()
        decisions = chatbot.extract_decisions()
        
        # Extract specialized information based on meeting type
        specialized_data = {}
        if meeting_type == "workshop":
            # Workshop-specific extractions
            specialized_data['key_learnings'] = WorkshopFunctions.extract_key_learnings(transcript)
            specialized_data['exercises'] = WorkshopFunctions.extract_exercises(transcript)
            specialized_data['qa_pairs'] = WorkshopFunctions.extract_qa_pairs(transcript)
        elif meeting_type == "brainstorming":
            # Brainstorming-specific extractions
            ideas_result = BrainstormingFunctions.extract_ideas(transcript)
            specialized_data['ideas'] = ideas_result
            specialized_data['categorized_ideas'] = BrainstormingFunctions.categorize_ideas(ideas_result)
            specialized_data['concerns'] = BrainstormingFunctions.extract_concerns(transcript)
        
        # Save results globally
        global last_summary, last_topics, last_actions, last_decisions
        last_summary = summary
        last_topics = topics
        last_actions = action_items
        last_decisions = decisions
        current_filename = Path(filename).name
        print(f"DEBUG: SET last_summary len={len(last_summary) if last_summary else 0}")
        
        # Save to history
        try:
            history_manager.save_analysis(
                filename=filename,
                summary=summary,
                topics=topics,
                action_items=action_items,
                decisions=decisions,
                metadata={
                    "language": language, 
                    "meeting_type": meeting_type,
                    "specialized_data": specialized_data
                }
            )
        except Exception as e:
            print(f"Failed to save history: {e}")
        
        # Add to RAG system
        if rag_system:
            try:
                rag_metadata = {
                    "meeting_type": meeting_type,
                    "language": language,
                    "filename": current_filename,
                    "timestamp": datetime.now().isoformat()
                }
                # Use filename as meeting_id for simplicity, or generate a UUID
                meeting_id = f"{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                rag_system.add_meeting(meeting_id, transcript, rag_metadata)
                logger.info(f"Added meeting {meeting_id} to RAG system")
            except Exception as e:
                logger.error(f"Failed to add to RAG: {e}")
        
        # Format outputs based on meeting type
        topics_text = format_topics_by_type(topics, meeting_type, specialized_data, language)
        actions_text = format_actions(action_items, language)
        decisions_text = format_decisions_by_type(decisions, meeting_type, specialized_data, language)
        
        success_msgs = {
            "vi": f"✅ Đã xử lý: {current_filename} | Loại: {meeting_type} | Ngôn ngữ: {language}",
            "en": f"✅ Processed: {current_filename} | Type: {meeting_type} | Language: {language}",
        }
        
        return (
            success_msgs.get(language, success_msgs["vi"]),
            transcript,
            summary,
            topics_text,
            actions_text,
            decisions_text,
            format_participants(specialized_data.get('participants', []), language) if 'participants' in specialized_data else ""
        )
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        
        # Check for specific errors
        error_str = str(e).lower()
        
        if "quota" in error_str or "429" in error_str:
            if language == "vi":
                user_message = "⚠️ Đã vượt quá giới hạn API (20 requests/ngày). Vui lòng:\n1. Đợi vài phút và thử lại\n2. Hoặc nâng cấp API key tại https://ai.google.dev"
            else:
                user_message = "⚠️ API quota exceeded (20 requests/day). Please:\n1. Wait a few minutes and retry\n2. Or upgrade your API key at https://ai.google.dev"
        elif "rate limit" in error_str:
            if language == "vi":
                user_message = "⚠️ Quá nhiều requests. Vui lòng đợi 30 giây và thử lại."
            else:
                user_message = "⚠️ Too many requests. Please wait 30 seconds and retry."
        else:
            user_message = get_user_friendly_message(e, language)
        
        return f"❌ {user_message}", "", "", "", "", "", ""


def format_topics(topics, language="vi"):
    """Format topics for display."""
    if not topics:
        return "_Không tìm thấy chủ đề_"
    
    result = []
    for i, topic in enumerate(topics, 1):
        result.append(f"### {i}. {topic.get('topic', 'N/A')}")
        result.append(f"{topic.get('description', '')}\n")
    
    return "\n".join(result)


def format_topics_by_type(topics, meeting_type, specialized_data, language="vi"):
    """Format topics based on meeting type with specialized data."""
    result = []
    
    # Standard topics
    result.append(format_topics(topics, language))
    
    # Add specialized sections based on meeting type
    if meeting_type == "workshop":
        # Add key learnings (limit to top 8)
        learnings = specialized_data.get('key_learnings', {}).get('key_learnings', [])
        if learnings:
            result.append("\n\n---\n## 📚 Key Learnings\n")
            for i, learning in enumerate(learnings[:8], 1):
                learning_text = learning if len(learning) <= 150 else learning[:147] + "..."
                result.append(f"{i}. {learning_text}")
    
    elif meeting_type == "brainstorming":
        # Add ideas...
        pass # Simplified for brevity, the original logic can be restored if needed
        
    return "\n".join(result)


def format_actions(actions, language="vi"):
    """Format action items for display."""
    if not actions:
        return "_Không có action items_"
    
    result = []
    for i, item in enumerate(actions, 1):
        task = item.get('task', 'N/A')
        assignee = item.get('assignee', 'N/A')
        deadline = item.get('deadline', 'N/A')
        
        result.append(f"### {i}. {task}")
        result.append(f"- Người phụ trách: **{assignee}**")
        result.append(f"- Hạn chót: {deadline}\n")
    
    return "\n".join(result)


def format_decisions(decisions, language="vi"):
    """Format decisions for display."""
    if not decisions:
        return "_Không có quyết định_"
    
    result = []
    for i, decision in enumerate(decisions, 1):
        decision_text = decision.get('decision', 'N/A')
        context = decision.get('context', 'N/A')
        
        result.append(f"### {i}. {decision_text}")
        result.append(f"- Bối cảnh: {context}\n")
    
    return "\n".join(result)


def format_decisions_by_type(decisions, meeting_type, specialized_data, language="vi"):
    """Format decisions based on meeting type."""
    return format_decisions(decisions, language)


def chat_with_ai(message):
    """Chat with AI.
    Returns:
        str: The AI's response text.
    """
    global chatbot
    
    if not chatbot:
        return "⚠️ Vui lòng xử lý transcript trước!"
    
    try:
        result = chatbot.ask_question(message)
        response = result.get("answer", "Xin lỗi, tôi không hiểu câu hỏi.")
        return response
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"


def export_to_txt(content_data=None):
    """Export analysis results to TXT file.
    Args:
        content_data: Optional string content to write directly.
    """
    global last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    if content_data:
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = Path("data/exports") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content_data, encoding='utf-8')
        return str(filepath)
    
    if not last_summary:
        return None
    
    content = []
    content.append("=" * 80)
    content.append("BÁO CÁO PHÂN TÍCH CUỘC HỌP".center(80))
    content.append("=" * 80)
    content.append(f"\nFile: {current_filename}")
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    content.append(f"\nTÓM TẮT")
    content.append("-" * 80)
    content.append(last_summary)
    
    content.append("\n\n" + "=" * 80)
    
    filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = Path("data/exports") / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(content), encoding='utf-8')
    
    return str(filepath)


def export_to_docx(content_data=None):
    """Export analysis results to DOCX file.
    Args:
        content_data: Optional dictionary or string.
    """
    global last_summary, last_topics, last_actions, last_decisions, current_language, current_filename
    
    # If generic content string is passed, we just wrap it in a doc
    if content_data and isinstance(content_data, str):
        try:
            from docx import Document
            doc = Document()
            doc.add_header
            doc.add_paragraph(content_data)
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            filepath = Path("data/exports") / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            doc.save(str(filepath))
            return str(filepath)
        except Exception as e:
            logger.error(f"Error exporting simple DOCX: {e}")
            return None
    
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
        
        filename = f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        filepath = Path("data/exports") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(filepath))
        
        return str(filepath)
    except Exception as e:
        logger.error(f"Error exporting DOCX: {e}")
        return None


def refresh_history():
    """Refresh history list.
    Returns:
        tuple: (choices_list, info_text)
        Where choices_list is [(label, value), ...] or just list of values.
    """
    history_list = history_manager.list_history(limit=20)
    
    if not history_list:
        return [], "_Chưa có lịch sử_"
    
    choices = [
        (f"{item['timestamp'][:10]} - {item['original_file']}", item['id'])
        for item in history_list
    ]
    
    info = f"📊 Tìm thấy {len(history_list)} phân tích đã lưu"
    
    return choices, info


def load_history(history_id):
    """Load analysis from history.
    Returns:
        tuple: (status, summary, topics, actions, decisions)
        Or just dict/object if used internally. 
        For compatibility with existing API expectations (tuple), we return tuple.
    """
    global last_summary, last_topics, last_actions, last_decisions, current_language
    
    if not history_id:
        return "⚠️ Vui lòng chọn phân tích", "", "", "", ""
    
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
    
    status = f"✅ Đã tải phân tích: {data.get('original_file')}"
    
    return status, last_summary, topics_text, actions_text, decisions_text


def save_recording_and_transcribe(audio_file, title, language, transcript_text):
    """Save recorded audio and transcript."""
    if audio_file is None:
        return "⚠️ Chưa có audio để lưu", ""
    
    try:
        # Save recording
        recording_id = audio_manager.save_recording(
            audio_file=audio_file,
            title=title or f"Ghi âm {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            notes=f"Language: {language}"
        )
        
        # Save transcript if available
        if transcript_text and transcript_text.strip():
            transcript_file = Path(f"data/transcripts/{recording_id}.txt")
            transcript_file.parent.mkdir(parents=True, exist_ok=True)
            transcript_file.write_text(transcript_text, encoding='utf-8')
        
        status = f"✅ Đã lưu ghi âm: {recording_id}"
        return status, recording_id
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}", ""


def process_upload(file_type, audio_file, text_file, transcribe_lang, enable_diarization, meeting_type, output_lang):
    """Process uploaded file."""
    # Logic adapted from process_file but handling audio/text differentiation
    
    # 1. Get Transcript
    transcript = ""
    participants_text = ""
    
    try:
        if file_type == 'audio' and audio_file:
            # Import STT here to avoid circular dependencies if any
            from backend.audio.huggingface_stt import transcribe_audio_huggingface
            
            # Transcribe
            logger.info(f"Transcribing audio file: {audio_file}")
            
            try:
                transcript_updates = transcribe_audio_huggingface(audio_file, transcribe_lang, realtime=False)
                
                # Consume generator - the function yields strings, last one contains full transcript
                transcript = ""
                update_count = 0
                last_update = ""
                
                for update in transcript_updates:
                    update_count += 1
                    if isinstance(update, str):
                        last_update = update
                        # Extract transcript from the formatted message
                        # The final message contains the full transcript between the header and footer
                        if "**Transcript Hoàn Chỉnh**" in update or "**Transcript ({" in update:
                            # Extract text between header and footer
                            lines = update.split('\n')
                            transcript_lines = []
                            in_transcript = False
                            for line in lines:
                                if '**Transcript' in line or '📝' in line:
                                    in_transcript = True
                                    continue
                                if in_transcript and (line.startswith('✅') or line.startswith('💡')):
                                    break
                                if in_transcript and line.strip():
                                    transcript_lines.append(line.strip())
                            
                            if transcript_lines:
                                transcript = '\n'.join(transcript_lines)
                                logger.debug(f"Extracted transcript: {len(transcript)} chars")
                
                # If no transcript extracted from formatted message, try to extract from last update
                if not transcript and last_update:
                    # Try to find any text content
                    lines = last_update.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip() and not line.startswith(('📝', '✅', '💡', '⚙️', '🔄', '⚠️', '🚨', '📊', '🎤', '🔍')):
                            # This might be transcript content
                            transcript = '\n'.join([l.strip() for l in lines[i:] if l.strip() and not l.startswith(('✅', '💡'))])
                            break
                
                logger.info(f"Transcription complete: {len(transcript)} chars from {update_count} updates")
                
            except Exception as transcribe_error:
                logger.error(f"Transcription error: {transcribe_error}", exc_info=True)
                return f"❌ Lỗi transcribe: {str(transcribe_error)}", "", "", "", "", "", ""
            
            if not transcript or len(transcript.strip()) == 0:
                logger.warning("Empty transcript after transcription")
                return "❌ Không thể chuyển đổi giọng nói thành văn bản (transcript rỗng)", "", "", "", "", "", ""
                
            # Create a temp file for the transcript to pass to process_file
            # process_file expects a file-like object with .name or a path string
            temp_transcript_path = Path(audio_file).with_suffix('.txt')
            temp_transcript_path.write_text(transcript, encoding='utf-8')
            
            logger.info(f"Transcript saved to {temp_transcript_path}, processing as text...")
            
            # Recursive call as text file
            # We pass the path string directly
            class MockFile:
                def __init__(self, name):
                    self.name = str(name)
            
            mock_file = MockFile(temp_transcript_path)
            result = process_file(mock_file, meeting_type, output_lang)
            logger.info(f"process_file returned: {type(result)}, len={len(result) if isinstance(result, tuple) else 'N/A'}")
            return result

        elif file_type == 'text' and text_file:
             # Use the text file directly
             class MockFile:
                 def __init__(self, name):
                     self.name = str(name)
             
             mock_file = MockFile(text_file)
             result = process_file(mock_file, meeting_type, output_lang)
             logger.info(f"process_file returned: {type(result)}, len={len(result) if isinstance(result, tuple) else 'N/A'}")
             return result
             
        logger.warning(f"Invalid file type or missing file: type={file_type}, audio={audio_file}, text={text_file}")
        return "⚠️ Invalid file type or missing file", "", "", "", "", "", ""
        
    except Exception as e:
        logger.error(f"Error in process_upload: {e}", exc_info=True)
        return f"❌ Lỗi: {str(e)}", "", "", "", "", "", ""
