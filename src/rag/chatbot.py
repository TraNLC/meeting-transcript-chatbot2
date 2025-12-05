"""Chatbot implementation without vector database."""

import json
from typing import Dict, List, Any
from src.llm import LLMManager, PromptTemplates


class Chatbot:
    """Chatbot chính hỗ trợ nhiều LLM provider."""

    def __init__(self, llm_manager: LLMManager, transcript: str = "", language: str = "vi", meeting_type: str = "meeting"):
        """
        Initialize chatbot.

        Args:
            llm_manager: LLM manager
            transcript: Nội dung transcript đầy đủ
            language: Ngôn ngữ output (vi hoặc en)
            meeting_type: Loại cuộc họp (meeting, workshop, brainstorming)
        """
        self.llm_manager = llm_manager
        self.transcript = transcript
        self.language = language
        self.meeting_type = meeting_type
        self.conversation_history: List[Dict[str, str]] = []

    def set_transcript(self, transcript: str) -> None:
        """
        Set transcript mới.

        Args:
            transcript: Nội dung transcript
        """
        self.transcript = transcript
        self.conversation_history = []

    def set_language(self, language: str) -> None:
        """
        Set ngôn ngữ output.

        Args:
            language: Ngôn ngữ (vi hoặc en)
        """
        self.language = language

    def generate_summary(self) -> str:
        """
        Tạo tóm tắt cuộc họp.

        Returns:
            Bản tóm tắt
        """
        if not self.transcript:
            return "Chưa có transcript để tóm tắt." if self.language == "vi" else "No transcript to summarize."

        # Add meeting type context to prompt (in correct language)
        if self.language == "vi":
            meeting_type_context = {
                "meeting": "Đây là cuộc họp thường.",
                "workshop": "Đây là buổi workshop/đào tạo. Tập trung vào các bài học chính và bài tập thực hành.",
                "brainstorming": "Đây là buổi động não. Tập trung vào các ý tưởng và sự sáng tạo."
            }
        else:
            meeting_type_context = {
                "meeting": "This is a regular business meeting.",
                "workshop": "This is a workshop/training session. Focus on key learnings and exercises.",
                "brainstorming": "This is a brainstorming session. Focus on ideas and creativity."
            }
        
        context = meeting_type_context.get(self.meeting_type, "")
        prompt = PromptTemplates.get_summary_prompt(self.transcript, self.language)
        
        # Prepend context if not regular meeting
        if self.meeting_type != "meeting" and context:
            prompt = f"{context}\n\n{prompt}"
        
        system_message = PromptTemplates.get_system_message_for_task("summary", self.language)
        
        summary = self.llm_manager.generate(prompt, system_message)
        return summary

    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Trả lời câu hỏi về cuộc họp.

        Args:
            question: Câu hỏi của user

        Returns:
            Dict chứa answer
        """
        if not self.transcript:
            msg = "Chưa có transcript để trả lời câu hỏi." if self.language == "vi" else "No transcript to answer questions."
            return {
                "answer": msg,
                "source": ""
            }

        prompt = PromptTemplates.get_qa_prompt(self.transcript, question, self.language)
        system_message = PromptTemplates.get_system_message_for_task("qa", self.language)
        
        answer = self.llm_manager.generate(prompt, system_message)

        # Add to conversation history in correct format for Gradio/LLM
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return {
            "answer": answer,
            "source": "Toàn bộ transcript" if self.language == "vi" else "Full transcript"
        }

    def extract_action_items_initially(self) -> List[Dict]:
        """
        Trích xuất action items từ transcript.

        Returns:
            List các action items
        """
        if not self.transcript:
            return []

        prompt = PromptTemplates.get_action_items_prompt(self.transcript, self.language)
        system_message = PromptTemplates.get_system_message_for_task("action_items", self.language)
        
        response = self.llm_manager.generate(prompt, system_message)

        # Parse JSON response
        return self._parse_json_response(response)

    def extract_decisions(self) -> List[Dict]:
        """
        Trích xuất decisions từ transcript.

        Returns:
            List các decisions
        """
        if not self.transcript:
            return []

        prompt = PromptTemplates.get_decisions_prompt(self.transcript, self.language)
        system_message = PromptTemplates.get_system_message_for_task("decisions", self.language)
        
        response = self.llm_manager.generate(prompt, system_message)

        # Parse JSON response
        return self._parse_json_response(response)

    def extract_topics(self) -> List[Dict]:
        """
        Trích xuất key topics từ transcript.

        Returns:
            List các topics
        """
        if not self.transcript:
            return []

        prompt = PromptTemplates.get_topics_prompt(self.transcript, self.language)
        system_message = PromptTemplates.get_system_message_for_task("topics", self.language)
        
        response = self.llm_manager.generate(prompt, system_message)

        # Parse JSON response
        return self._parse_json_response(response)

    def _parse_json_response(self, response: str) -> List[Dict]:
        """
        Parse JSON response từ LLM.

        Args:
            response: Response string từ LLM

        Returns:
            List of dicts hoặc empty list
        """
        try:
            # Try to extract JSON from response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                return data if isinstance(data, list) else []
            return []
        except (json.JSONDecodeError, ValueError):
            return []

    def clear_history(self) -> None:
        """Xóa lịch sử hội thoại."""
        self.conversation_history = []
