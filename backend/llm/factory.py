"""LLM Factory for creating different LLM providers (Sprint 2)."""

from typing import Optional
from .base import BaseLLM
from .gemini_model import GeminiModel
from .openai_model import OpenAIModel


class LLMFactory:
    """Factory for creating LLM instances.
    
    Sprint 2: Supports multiple providers (Gemini, OpenAI, Llama).
    """
    
    @staticmethod
    def create(
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseLLM:
        """Create LLM instance based on provider.
        
        Args:
            provider: Provider name ('gemini', 'openai', 'llama')
            api_key: API key for the provider
            model: Model name (optional, uses default if not provided)
            **kwargs: Additional configuration
            
        Returns:
            BaseLLM instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()
        
        if provider == "gemini":
            model = model or "gemini-2.5-flash"
            return GeminiModel(api_key=api_key, model=model, **kwargs)
        
        elif provider == "openai":
            model = model or "gpt-3.5-turbo"
            return OpenAIModel(api_key=api_key, model=model, **kwargs)
        
        elif provider == "llama":
            # Sprint 2: Will implement Llama 3
            raise NotImplementedError(
                "Llama provider will be implemented in Sprint 2 workshop"
            )
        
        else:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: gemini, openai (Sprint 2), llama (Sprint 2)"
            )
    
    @staticmethod
    def get_supported_providers() -> list:
        """Get list of supported providers.
        
        Returns:
            List of provider names
        """
        return ["gemini", "openai", "llama"]
    
    @staticmethod
    def get_default_model(provider: str) -> str:
        """Get default model for a provider.
        
        Args:
            provider: Provider name
            
        Returns:
            Default model name
        """
        defaults = {
            "gemini": "gemini-2.5-flash",
            "openai": "gpt-3.5-turbo",
            "llama": "llama-3-8b"
        }
        return defaults.get(provider.lower(), "")


# Backward compatibility wrapper
class LLMManager:
    """LLM Manager with backward compatibility (Sprint 1 → Sprint 2).
    
    This class maintains Sprint 1 API while using new architecture.
    """
    
    def __init__(
        self,
        provider: str = "gemini",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """Initialize LLM Manager (Sprint 1 compatible).
        
        Args:
            provider: LLM provider name
            model_name: Model name to use
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            api_key: API key for the provider
            **kwargs: Additional provider-specific parameters (e.g., base_url for OpenAI)
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self.provider = provider
        self.model_name = model_name or LLMFactory.get_default_model(provider)
        
        # Create LLM instance using factory
        self.model = LLMFactory.create(
            provider=provider,
            api_key=api_key,
            model=self.model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def generate(self, prompt: str, system_message: str = "") -> str:
        """Generate text (Sprint 1 compatible API).
        
        Args:
            prompt: User prompt
            system_message: System message for context
            
        Returns:
            Generated text
        """
        return self.model.generate(prompt, system_message)
    
    def chat_completion(self, messages: list, **kwargs) -> str:
        """Generate chat completion (Sprint 2 feature).
        
        Args:
            messages: List of message dicts
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        return self.model.chat_completion(messages, **kwargs)
