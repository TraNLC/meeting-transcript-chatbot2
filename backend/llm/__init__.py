"""LLM module.

Sprint 1: Basic Gemini support
Sprint 2: Multi-provider architecture
"""

# Sprint 1 (backward compatible)
from .chat_model import LLMManager as LLMManagerV1

# Sprint 2 (new architecture)
from .base import BaseLLM
from .gemini_model import GeminiModel
from .factory import LLMFactory, LLMManager
from .prompts import PromptTemplates

# Export Sprint 2 by default, but keep Sprint 1 available
__all__ = [
    # Sprint 2 (recommended)
    "LLMManager",
    "LLMFactory",
    "BaseLLM",
    "GeminiModel",
    "PromptTemplates",
    # Sprint 1 (backward compatible)
    "LLMManagerV1",
]
