"""
Conversation Manager for RAG Chat.

Manages conversation history to enable multi-turn, context-aware chat.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import threading

class ConversationManager:
    """Manage conversation history for RAG chat sessions."""
    
    def __init__(self, max_turns: int = 5):
        """
        Initialize Conversation Manager.
        
        Args:
            max_turns: Maximum number of Q&A pairs to keep in memory
        """
        self.max_turns = max_turns
        # Format: {session_id: {"messages": [...], "last_active": datetime}}
        self._sessions = {}
        self._lock = threading.Lock()
        
    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to conversation history.
        
        Args:
            session_id: Unique session identifier
            role: 'user' or 'assistant'
            content: Message content
        """
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = {
                    "messages": [],
                    "last_active": datetime.now()
                }
            
            self._sessions[session_id]["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            self._sessions[session_id]["last_active"] = datetime.now()
            
            # Keep only last N turns (2 messages per turn)
            max_messages = self.max_turns * 2
            if len(self._sessions[session_id]["messages"]) > max_messages:
                self._sessions[session_id]["messages"] = \
                    self._sessions[session_id]["messages"][-max_messages:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of message dicts
        """
        with self._lock:
            if session_id not in self._sessions:
                return []
            
            self._sessions[session_id]["last_active"] = datetime.now()
            return self._sessions[session_id]["messages"].copy()
    
    def get_formatted_context(self, session_id: str) -> str:
        """
        Get conversation history formatted for LLM prompt.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Formatted string of conversation history
        """
        history = self.get_history(session_id)
        
        if not history:
            return ""
        
        lines = ["Previous conversation:"]
        for msg in history:
            role_label = "User" if msg["role"] == "user" else "AI"
            lines.append(f"{role_label}: {msg['content']}")
        
        return "\n".join(lines)
    
    def clear_session(self, session_id: str):
        """Clear conversation history for a session."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """
        Remove sessions that haven't been active recently.
        
        Args:
            max_age_hours: Maximum age in hours before cleanup
        """
        with self._lock:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            sessions_to_remove = [
                sid for sid, data in self._sessions.items()
                if data["last_active"] < cutoff_time
            ]
            
            for sid in sessions_to_remove:
                del self._sessions[sid]
            
            if sessions_to_remove:
                print(f"[ConversationManager] Cleaned up {len(sessions_to_remove)} old sessions")


# Global singleton instance
_conversation_manager = None

def get_conversation_manager() -> ConversationManager:
    """Get global ConversationManager instance."""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager(max_turns=5)
    return _conversation_manager
