"""OpenAI LLM Manager - Enhanced LLM support."""

import os
from typing import Optional, Dict, Any, List
from openai import OpenAI


class OpenAIManager:
    """Manages OpenAI API interactions."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """Initialize OpenAI manager.
        
        Args:
            api_key: OpenAI API key (or from env OPENAI_API_KEY)
            model: Model name (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text completion.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.choices[0].message.content
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Multi-turn chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.choices[0].message.content
    
    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None) -> str:
        """Transcribe audio using Whisper API.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (optional, auto-detect if None)
            
        Returns:
            Transcribed text
        """
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
        
        return transcript.text
    
    def translate_audio(self, audio_file_path: str) -> str:
        """Translate audio to English using Whisper API.
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Translated text (in English)
        """
        with open(audio_file_path, "rb") as audio_file:
            translation = self.client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
        
        return translation.text
    
    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """Get text embedding.
        
        Args:
            text: Input text
            model: Embedding model name
            
        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            model=model,
            input=text
        )
        
        return response.data[0].embedding
