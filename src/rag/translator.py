"""Translation module for multilingual output support."""

from typing import Dict, Any, Optional, List
from deep_translator import GoogleTranslator
import json


class ContentTranslator:
    """Translate content to any language using Google Translate."""
    
    # Supported languages with their codes
    SUPPORTED_LANGUAGES = {
        "vi": "Vietnamese",
        "en": "English",
        "zh-CN": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ar": "Arabic",
        "th": "Thai",
        "id": "Indonesian",
        "ms": "Malay",
        "hi": "Hindi",
        "tr": "Turkish",
        "nl": "Dutch",
        "pl": "Polish"
    }
    
    def __init__(self, target_language: str = "vi"):
        """Initialize translator.
        
        Args:
            target_language: Target language code (e.g., 'vi', 'en', 'ja')
        """
        self.target_language = target_language
        self.translator = None
        
        if target_language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Language '{target_language}' not supported. "
                f"Supported: {list(self.SUPPORTED_LANGUAGES.keys())}"
            )
    
    def translate_text(self, text: str, source: str = "auto") -> str:
        """Translate a single text.
        
        Args:
            text: Text to translate
            source: Source language (default: auto-detect)
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # Skip if already in target language (simple check)
        if len(text.strip()) < 3:
            return text
        
        try:
            translator = GoogleTranslator(source=source, target=self.target_language)
            result = translator.translate(text)
            return result if result else text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original if translation fails
    
    def translate_dict(self, data: Dict[str, Any], fields_to_translate: List[str]) -> Dict[str, Any]:
        """Translate specific fields in a dictionary.
        
        Args:
            data: Dictionary to translate
            fields_to_translate: List of field names to translate
            
        Returns:
            Dictionary with translated fields
        """
        result = data.copy()
        
        for field in fields_to_translate:
            if field in result and isinstance(result[field], str):
                result[field] = self.translate_text(result[field])
        
        return result
    
    def translate_list_of_dicts(
        self, 
        data_list: List[Dict[str, Any]], 
        fields_to_translate: List[str]
    ) -> List[Dict[str, Any]]:
        """Translate specific fields in a list of dictionaries.
        
        Args:
            data_list: List of dictionaries
            fields_to_translate: List of field names to translate
            
        Returns:
            List with translated fields
        """
        return [
            self.translate_dict(item, fields_to_translate) 
            for item in data_list
        ]
    
    def translate_result(self, result: Dict[str, Any], result_type: str) -> Dict[str, Any]:
        """Translate function execution result based on type.
        
        Args:
            result: Result dictionary from function execution
            result_type: Type of result ('participants', 'action_items', 'decisions', 'search')
            
        Returns:
            Translated result
        """
        if result_type == "participants":
            # Translate: role, contribution
            if "participants" in result:
                result["participants"] = self.translate_list_of_dicts(
                    result["participants"],
                    ["role", "contribution"]
                )
        
        elif result_type == "action_items":
            # Translate: task, deadline, priority
            if "action_items" in result:
                result["action_items"] = self.translate_list_of_dicts(
                    result["action_items"],
                    ["task", "deadline", "priority"]
                )
        
        elif result_type == "decisions":
            # Translate: decision, context, impact
            if "decisions" in result:
                result["decisions"] = self.translate_list_of_dicts(
                    result["decisions"],
                    ["decision", "context", "impact"]
                )
        
        elif result_type == "search":
            # Translate: matched_line, context
            if "results" in result:
                result["results"] = self.translate_list_of_dicts(
                    result["results"],
                    ["matched_line", "context"]
                )
        
        return result
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """Get dictionary of supported languages.
        
        Returns:
            Dict mapping language codes to language names
        """
        return cls.SUPPORTED_LANGUAGES.copy()
