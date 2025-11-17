"""LLM manager using Google Gemini."""

from typing import Optional
import google.generativeai as genai


class LLMManager:
    """Quản lý Google Gemini LLM."""

    def __init__(
        self,
        provider: str = "gemini",
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        api_key: Optional[str] = None,
    ):
        """
        Initialize LLM manager.

        Args:
            provider: LLM provider (always 'gemini')
            model_name: Tên model Gemini
            temperature: Temperature cho generation (0-2)
            max_tokens: Số tokens tối đa
            api_key: API key (optional, sẽ lấy từ env nếu không có)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if api_key:
            genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, system_message: str = None) -> str:
        """
        Generate response từ Gemini.

        Args:
            prompt: User prompt
            system_message: System message (optional)

        Returns:
            Generated response

        Raises:
            RuntimeError: Nếu generation thất bại
        """
        try:
            # Combine system message and prompt for Gemini
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"
            
            generation_config = genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
            
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            return response.text
        except Exception as e:
            raise RuntimeError(f"GEMINI API call failed: {str(e)}")

    def generate_with_context(
        self, 
        context: str, 
        question: str,
        system_message: str = None
    ) -> str:
        """
        Generate response với context.

        Args:
            context: Context từ transcript
            question: Câu hỏi của user
            system_message: System message

        Returns:
            Generated response
        """
        prompt = f"""Dựa trên ngữ cảnh sau từ transcript cuộc họp:

{context}

Câu hỏi: {question}

Hãy trả lời câu hỏi dựa trên thông tin trong ngữ cảnh. Nếu không tìm thấy thông tin, hãy nói rõ."""

        return self.generate(prompt, system_message)
