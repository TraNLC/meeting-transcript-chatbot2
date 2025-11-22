"""History manager for saving and loading analysis results."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class HistoryManager:
    """Manage analysis history - save and load results."""
    
    def __init__(self, history_dir: str = "data/history"):
        """Initialize history manager.
        
        Args:
            history_dir: Directory to store history files
        """
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def save_analysis(
        self,
        filename: str,
        summary: str,
        topics: List[Dict],
        action_items: List[Dict],
        decisions: List[Dict],
        metadata: Optional[Dict] = None
    ) -> str:
        """Save analysis results to history.
        
        Args:
            filename: Original transcript filename
            summary: Meeting summary
            topics: List of topics
            action_items: List of action items
            decisions: List of decisions
            metadata: Additional metadata
            
        Returns:
            History file ID
        """
        # Generate unique ID based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_id = f"{timestamp}_{Path(filename).stem}"
        
        # Prepare data
        data = {
            "id": history_id,
            "timestamp": datetime.now().isoformat(),
            "original_file": filename,
            "summary": summary,
            "topics": topics,
            "action_items": action_items,
            "decisions": decisions,
            "metadata": metadata or {}
        }
        
        # Save to JSON file
        history_file = self.history_dir / f"{history_id}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return history_id
    
    def load_analysis(self, history_id: str) -> Optional[Dict[str, Any]]:
        """Load analysis results from history.
        
        Args:
            history_id: History file ID
            
        Returns:
            Analysis data or None if not found
        """
        history_file = self.history_dir / f"{history_id}.json"
        
        if not history_file.exists():
            return None
        
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def list_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent analysis history.
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of history items (metadata only)
        """
        history_files = sorted(
            self.history_dir.glob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        history_list = []
        for file in history_files[:limit]:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Return metadata only
                history_list.append({
                    "id": data.get("id"),
                    "timestamp": data.get("timestamp"),
                    "original_file": data.get("original_file"),
                    "summary_preview": data.get("summary", "")[:100] + "..."
                })
            except Exception:
                continue
        
        return history_list
    
    def delete_analysis(self, history_id: str) -> bool:
        """Delete analysis from history.
        
        Args:
            history_id: History file ID
            
        Returns:
            True if deleted, False if not found
        """
        history_file = self.history_dir / f"{history_id}.json"
        
        if history_file.exists():
            history_file.unlink()
            return True
        
        return False
    
    def clear_all_history(self) -> int:
        """Clear all history files.
        
        Returns:
            Number of files deleted
        """
        count = 0
        for file in self.history_dir.glob("*.json"):
            file.unlink()
            count += 1
        
        return count
    
    def export_to_json(self, history_id: str, output_path: str) -> bool:
        """Export analysis to a custom location.
        
        Args:
            history_id: History file ID
            output_path: Output file path
            
        Returns:
            True if successful
        """
        data = self.load_analysis(history_id)
        
        if not data:
            return False
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True


# Example usage
if __name__ == "__main__":
    manager = HistoryManager()
    
    # Save analysis
    history_id = manager.save_analysis(
        filename="meeting_2025.txt",
        summary="Team discussed sprint planning and assigned tasks.",
        topics=[
            {"topic": "Sprint Planning", "description": "Discussed goals for next sprint"}
        ],
        action_items=[
            {"task": "Complete API", "assignee": "Alice", "deadline": "Friday"}
        ],
        decisions=[
            {"decision": "Use React", "context": "After discussion"}
        ]
    )
    
    print(f"Saved with ID: {history_id}")
    
    # List history
    print("\nRecent history:")
    for item in manager.list_history(limit=5):
        print(f"  - {item['id']}: {item['original_file']}")
    
    # Load analysis
    data = manager.load_analysis(history_id)
    print(f"\nLoaded: {data['summary']}")
