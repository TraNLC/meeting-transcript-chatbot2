"""OpenAI LLM implementation."""

from typing import Optional
from openai import OpenAI
from .base import BaseLLM
import os


class OpenAIModel(BaseLLM):
    """OpenAI LLM implementation using OpenAI API."""
    
    def __init__(
        self,
        api_key: str,
        model: str = os.getenv("AZURE_OPENAI_LLM_MODEL"),
        temperature: float = 0.7,
        max_tokens: int = 4000,
        base_url: Optional[str] = os.getenv("AZURE_OPENAI_LLM_ENDPOINT"),
        **kwargs
    ):
        """Initialize OpenAI model.
        
        Args:
            api_key: OpenAI API key
            model: Model name (e.g., gpt-3.5-turbo, gpt-4, GPT-5.1)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            base_url: Custom base URL for OpenAI-compatible APIs
            **kwargs: Additional configuration
        """
        super().__init__(api_key, model, **kwargs)
        
        # Initialize OpenAI client
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        
        self.client = OpenAI(**client_kwargs)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response using OpenAI API.
        
        Args:
            prompt: User prompt
            system_message: System message (optional)
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            messages = []
            
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate response
            response = self.client.chat.completions.create(
                model="GPT-4.1",
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens)
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")
    
    def chat_completion(self, messages: list, **kwargs) -> str:
        """Generate chat completion with message history.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens)
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")
    
    def generate_stream(self, prompt: str, system_message: Optional[str] = None, **kwargs):
        """Generate response using OpenAI API with streaming.
        
        Args:
            prompt: User prompt
            system_message: System message (optional)
            **kwargs: Additional generation parameters
            
        Yields:
            Text chunks as they are generated
        """
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            # Generate streaming response
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"
