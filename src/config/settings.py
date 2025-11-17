"""Configuration settings for the chatbot."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""

    # API Key
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # LLM Configuration (Fixed to Gemini)
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    
    # Output Language (Fixed to Vietnamese)
    OUTPUT_LANGUAGE: str = "vi"

    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in .env file."
            )


# Validate settings on import
Settings.validate()
