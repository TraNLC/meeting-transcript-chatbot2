"""Gemini LLM implementation (Sprint 1).

Refactored from chat_model.py to support multi-provider architecture (Sprint 2).
"""

from typing import Optional, List, Dict
import google.generativeai as genai
from .base import BaseLLM


class GeminiModel(BaseLLM):
    """Google Gemini LLM implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs
    ):
        """Initialize Gemini model.
        
        Args:
            api_key: Gemini API key
            model: Model name (default: gemini-2.5-flash)
            temperature: Temperature for generation (0-2)
            max_tokens: Maximum tokens to generate
        """
        super().__init__(api_key, model, **kwargs)
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)

    def generate(self, prompt: str, system_message: str = "", **kwargs) -> str:
        """Generate text using Gemini.
        
        Args:
            prompt: User prompt
            system_message: System message for context
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If generation fails
        """
        try:
            # Combine system message and prompt
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"
            
            generation_config = genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
            
            # Configure safety settings to be less restrictive
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check if response was blocked
            if not response.parts:
                # Check finish reason
                if hasattr(response, 'candidates') and response.candidates:
                    finish_reason = response.candidates[0].finish_reason
                    if finish_reason == 2:  # SAFETY
                        return "⚠️ Response was blocked by safety filters. Please try rephrasing your question."
                    elif finish_reason == 3:  # RECITATION
                        return "⚠️ Response was blocked due to recitation. Please try a different question."
                    else:
                        return f"⚠️ Response generation stopped (reason: {finish_reason}). Please try again."
                return "⚠️ No response generated. Please try again with a different prompt."
            
            return response.text
            
        except AttributeError as e:
            # Handle response.text access error
            if "response.text" in str(e):
                return "⚠️ Response was blocked by safety filters. Please try rephrasing your question."
            raise RuntimeError(f"Gemini API call failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {str(e)}")
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """Generate chat completion (Sprint 2 feature).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        # Convert messages to Gemini format
        # Gemini doesn't have native chat format, so we concatenate
        prompt_parts = []
        system_msg = ""
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                system_msg = content
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts)
        return self.generate(prompt, system_msg, **kwargs)
    
    def generate_with_context(
        self, 
        context: str, 
        question: str,
        system_message: str = ""
    ) -> str:
        """Generate response with context (Sprint 1 feature).
        
        Args:
            context: Context from transcript
            question: User question
            system_message: System message
            
        Returns:
            Generated response
        """
        prompt = f"""Dựa trên ngữ cảnh sau từ transcript cuộc họp:

{context}

Câu hỏi: {question}

Hãy trả lời câu hỏi dựa trên thông tin trong ngữ cảnh. Nếu không tìm thấy thông tin, hãy nói rõ."""

        return self.generate(prompt, system_message)
