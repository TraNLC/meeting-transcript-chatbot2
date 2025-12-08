"""
Multi-Key Manager with Automatic Fallback
Automatically switches to backup keys when primary key fails
"""

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


class MultiKeyManager:
    """Manages multiple API keys with automatic fallback."""
    
    def __init__(self):
        """Initialize with all available keys."""
        self.keys = self._load_all_keys()
        self.current_key_index = {}
    
    def _load_all_keys(self) -> Dict[str, List[Dict]]:
        """Load all API keys from environment."""
        keys = {
            'openai': [],
            'azure_llm': [],
            'gemini': []
        }
        
        # OpenAI keys
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            keys['openai'].append({
                'key': openai_key,
                'base_url': os.getenv('OPENAI_BASE_URL'),
                'name': 'OpenAI Primary'
            })
        
        # Azure LLM keys
        azure_key_1 = os.getenv('AZURE_OPENAI_LLM_API_KEY')
        azure_key_2 = os.getenv('AZURE_OPENAI_LLM_API_KEY_2')
        azure_endpoint = os.getenv('AZURE_OPENAI_LLM_ENDPOINT')
        
        if azure_key_1:
            keys['azure_llm'].append({
                'key': azure_key_1,
                'base_url': azure_endpoint,
                'name': 'Azure LLM Key 1'
            })
        
        if azure_key_2:
            keys['azure_llm'].append({
                'key': azure_key_2,
                'base_url': azure_endpoint,
                'name': 'Azure LLM Key 2'
            })
        
        # Gemini keys
        gemini_key = os.getenv('GEMINI_API_KEY')
        gemini_portal_key = os.getenv('GEMINI_PORTAL_API_KEY')
        
        if gemini_key:
            keys['gemini'].append({
                'key': gemini_key,
                'type': 'google',
                'name': 'Gemini Google'
            })
        
        if gemini_portal_key:
            keys['gemini'].append({
                'key': gemini_portal_key,
                'base_url': os.getenv('GEMINI_PORTAL_ENDPOINT'),
                'type': 'portal',
                'name': 'Gemini Portal'
            })
        
        return keys
    
    def get_key(self, provider: str) -> Optional[Dict]:
        """Get current key for provider."""
        if provider not in self.keys or not self.keys[provider]:
            return None
        
        if provider not in self.current_key_index:
            self.current_key_index[provider] = 0
        
        index = self.current_key_index[provider]
        return self.keys[provider][index]
    
    def switch_to_next_key(self, provider: str) -> Optional[Dict]:
        """Switch to next available key for provider."""
        if provider not in self.keys or not self.keys[provider]:
            return None
        
        if provider not in self.current_key_index:
            self.current_key_index[provider] = 0
        
        # Move to next key
        self.current_key_index[provider] = (self.current_key_index[provider] + 1) % len(self.keys[provider])
        
        return self.get_key(provider)
    
    def get_all_keys(self, provider: str) -> List[Dict]:
        """Get all keys for provider."""
        return self.keys.get(provider, [])
    
    def has_backup_keys(self, provider: str) -> bool:
        """Check if provider has backup keys."""
        return len(self.keys.get(provider, [])) > 1
    
    def get_key_info(self) -> Dict:
        """Get summary of all available keys."""
        info = {}
        for provider, keys in self.keys.items():
            info[provider] = {
                'count': len(keys),
                'keys': [k['name'] for k in keys]
            }
        return info


# Global instance
_key_manager = None


def get_key_manager() -> MultiKeyManager:
    """Get global key manager instance."""
    global _key_manager
    if _key_manager is None:
        _key_manager = MultiKeyManager()
    return _key_manager


def test_all_keys():
    """Test all keys and report status."""
    manager = get_key_manager()
    
    print("\n" + "="*60)
    print("Multi-Key Manager - Available Keys")
    print("="*60)
    
    info = manager.get_key_info()
    
    for provider, data in info.items():
        print(f"\n{provider.upper()}:")
        print(f"  Total keys: {data['count']}")
        for key_name in data['keys']:
            print(f"  - {key_name}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_all_keys()
