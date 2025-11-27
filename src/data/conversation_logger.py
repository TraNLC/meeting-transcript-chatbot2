"""Conversation logger for testing and debugging."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class ConversationLogger:
    """Log conversations for testing and analysis."""
    
    def __init__(self, log_dir: str = "data/conversation_logs"):
        """Initialize conversation logger.
        
        Args:
            log_dir: Directory to store conversation logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_session = None
        self.session_file = None
    
    def start_session(self, session_name: Optional[str] = None) -> str:
        """Start a new conversation session.
        
        Args:
            session_name: Custom session name
            
        Returns:
            Session ID
        """
        session_id = session_name or datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.current_session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "conversations": [],
            "metadata": {}
        }
        
        self.session_file = self.log_dir / f"{session_id}.json"
        
        return session_id
    
    def log_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a message in the conversation.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Additional metadata
        """
        if not self.current_session:
            self.start_session()
        
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        
        self.current_session["conversations"].append(message)
        self._save_session()
    
    def log_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Log user message."""
        self.log_message("user", content, metadata)
    
    def log_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Log assistant message."""
        self.log_message("assistant", content, metadata)
    
    def log_system_message(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Log system message."""
        self.log_message("system", content, metadata)
    
    def log_error(self, error: str, metadata: Optional[Dict[str, Any]] = None):
        """Log error message."""
        self.log_message("error", error, metadata)
    
    def add_metadata(self, key: str, value: Any):
        """Add metadata to current session.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        if not self.current_session:
            self.start_session()
        
        self.current_session["metadata"][key] = value
        self._save_session()
    
    def end_session(self):
        """End current session."""
        if self.current_session:
            self.current_session["end_time"] = datetime.now().isoformat()
            self._save_session()
            self.current_session = None
            self.session_file = None
    
    def _save_session(self):
        """Save current session to file."""
        if self.current_session and self.session_file:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_session, f, ensure_ascii=False, indent=2)
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None
        """
        session_file = self.log_dir / f"{session_id}.json"
        
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions.
        
        Returns:
            List of session summaries
        """
        sessions = []
        
        for file in self.log_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "session_id": data.get("session_id"),
                        "start_time": data.get("start_time"),
                        "end_time": data.get("end_time"),
                        "message_count": len(data.get("conversations", [])),
                        "metadata": data.get("metadata", {})
                    })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        # Sort by start time (newest first)
        sessions.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        
        return sessions
    
    def export_session_to_markdown(self, session_id: str, output_path: Optional[str] = None) -> str:
        """Export session to markdown format.
        
        Args:
            session_id: Session ID
            output_path: Output file path (optional)
            
        Returns:
            Markdown content
        """
        session = self.load_session(session_id)
        
        if not session:
            return ""
        
        lines = []
        lines.append(f"# Conversation Log: {session_id}\n")
        lines.append(f"**Start Time:** {session.get('start_time')}")
        lines.append(f"**End Time:** {session.get('end_time', 'In progress')}\n")
        
        # Metadata
        if session.get('metadata'):
            lines.append("## Metadata\n")
            for key, value in session['metadata'].items():
                lines.append(f"- **{key}:** {value}")
            lines.append("")
        
        # Conversations
        lines.append("## Conversation\n")
        
        for msg in session.get('conversations', []):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            if role == 'user':
                lines.append(f"### 👤 User ({timestamp})\n")
            elif role == 'assistant':
                lines.append(f"### 🤖 Assistant ({timestamp})\n")
            elif role == 'system':
                lines.append(f"### ⚙️ System ({timestamp})\n")
            elif role == 'error':
                lines.append(f"### ❌ Error ({timestamp})\n")
            
            lines.append(f"{content}\n")
        
        markdown = "\n".join(lines)
        
        # Save to file if requested
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
        
        return markdown
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about logged conversations.
        
        Returns:
            Statistics dictionary
        """
        sessions = self.list_sessions()
        
        total_sessions = len(sessions)
        total_messages = sum(s.get('message_count', 0) for s in sessions)
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "average_messages_per_session": total_messages / total_sessions if total_sessions > 0 else 0,
            "recent_sessions": sessions[:5]
        }
