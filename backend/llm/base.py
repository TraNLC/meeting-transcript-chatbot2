"""Base LLM interface for multi-provider support (Sprint 2)."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLM(ABC):
    """Abstract base class for LLM providers.
    
    Sprint 2: Enables multi-LLM support (Gemini, OpenAI, Llama).
    """
    
    def __init__(self, api_key: str, model: str, **kwargs):
        """Initialize LLM provider.
        
        Args:
            api_key: API key for the provider
            model: Model name to use
            **kwargs: Additional configuration
        """
        self.api_key = api_key
        self.model = model
        self.config = kwargs
    
    @abstractmethod
    def generate(self, prompt: str, system_message: str = "", **kwargs) -> str:
        """Generate text completion.
        
        Args:
            prompt: User prompt
            system_message: System message for context
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """Generate chat completion (Sprint 2).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        pass
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return self.__class__.__name__.replace("Model", "")
