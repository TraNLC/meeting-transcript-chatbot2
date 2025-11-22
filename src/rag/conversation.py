"""Conversation management for multi-turn dialogues (Sprint 2)."""

from typing import List, Dict, Optional
import json
from pathlib import Path


class ConversationManager:
    """Manage conversation history and context (Sprint 2 feature).
    
    Handles multi-turn conversations with context management.
    """
    
    def __init__(self, max_history: int = 10, max_tokens: int = 4000):
        """Initialize conversation manager.
        
        Args:
            max_history: Maximum number of messages to keep
            max_tokens: Approximate token limit for context
        """
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history
        self.max_tokens = max_tokens
    
    def add_system_message(self, content: str) -> None:
        """Add system message at the beginning.
        
        Args:
            content: System message content
        """
        # Remove existing system message if any
        self.messages = [msg for msg in self.messages if msg["role"] != "system"]
        # Add new system message at the beginning
        self.messages.insert(0, {"role": "system", "content": content})
    
    def add_user_message(self, content: str) -> None:
        """Add user message.
        
        Args:
            content: User message content
        """
        self.messages.append({"role": "user", "content": content})
        self._trim_history()
    
    def add_assistant_message(self, content: str) -> None:
        """Add assistant message.
        
        Args:
            content: Assistant message content
        """
        self.messages.append({"role": "assistant", "content": content})
        self._trim_history()
    
    def add_function_message(self, name: str, content: str) -> None:
        """Add function call result (Sprint 2 feature).
        
        Args:
            name: Function name
            content: Function result
        """
        self.messages.append({
            "role": "function",
            "name": name,
            "content": content
        })
        self._trim_history()
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages.
        
        Returns:
            List of message dicts
        """
        return self.messages.copy()
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """Get last N messages.
        
        Args:
            n: Number of messages to get
            
        Returns:
            List of last N messages
        """
        return self.messages[-n:] if n > 0 else []
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []
    
    def _trim_history(self) -> None:
        """Trim conversation history to stay within limits."""
        # Keep system message if exists
        system_msg = None
        if self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
            messages = self.messages[1:]
        else:
            messages = self.messages
        
        # Trim to max_history
        if len(messages) > self.max_history:
            messages = messages[-self.max_history:]
        
        # Rebuild messages list
        if system_msg:
            self.messages = [system_msg] + messages
        else:
            self.messages = messages
    
    def _estimate_tokens(self) -> int:
        """Estimate total tokens in conversation.
        
        Returns:
            Approximate token count
        """
        # Rough estimation: 1 token ≈ 4 characters
        total_chars = sum(len(msg["content"]) for msg in self.messages)
        return total_chars // 4
    
    def export_to_json(self, filepath: str) -> None:
        """Export conversation to JSON file.
        
        Args:
            filepath: Path to save JSON file
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)
    
    def import_from_json(self, filepath: str) -> None:
        """Import conversation from JSON file.
        
        Args:
            filepath: Path to JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            self.messages = json.load(f)
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation.
        
        Returns:
            Summary string
        """
        if not self.messages:
            return "No messages in conversation"
        
        user_msgs = sum(1 for msg in self.messages if msg["role"] == "user")
        assistant_msgs = sum(1 for msg in self.messages if msg["role"] == "assistant")
        
        return (
            f"Conversation: {len(self.messages)} messages "
            f"({user_msgs} user, {assistant_msgs} assistant)"
        )
    
    def __len__(self) -> int:
        """Get number of messages."""
        return len(self.messages)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"ConversationManager({len(self.messages)} messages)"
