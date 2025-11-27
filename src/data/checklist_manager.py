"""Checklist Manager - Manage action items and tasks."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class ChecklistManager:
    """Manager for checklist/tasks storage and operations."""
    
    def __init__(self, data_dir: str = "data/checklists"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.checklist_file = self.data_dir / "tasks.json"
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from JSON file."""
        if self.checklist_file.exists():
            with open(self.checklist_file, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
    
    def _save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.checklist_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(
        self,
        description: str,
        assignee: str = "",
        deadline: str = "",
        priority: str = "medium",
        source: str = "manual"
    ) -> Dict:
        """Add a new task."""
        task = {
            "id": f"T{len(self.tasks) + 1:03d}",
            "description": description,
            "assignee": assignee,
            "deadline": deadline,
            "priority": priority,
            "status": "pending",
            "source": source,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def update_status(self, task_id: str, status: str) -> bool:
        """Update task status (pending/completed)."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                if status == "completed":
                    task["completed_at"] = datetime.now().isoformat()
                else:
                    task["completed_at"] = None
                self._save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self._save_tasks()
                return True
        return False
    
    def get_tasks(self, filter_status: str = "all") -> List[Dict]:
        """Get tasks with optional filter."""
        if filter_status == "all":
            return self.tasks
        return [t for t in self.tasks if t["status"] == filter_status]
    
    def get_statistics(self) -> Dict:
        """Get checklist statistics."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completed"])
        pending = total - completed
        rate = (completed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round(rate, 1)
        }
    
    def import_from_analysis(self, action_items_text: str, source: str = "analysis") -> int:
        """Import action items from analysis text."""
        if not action_items_text or action_items_text == "_Chưa có dữ liệu_":
            return 0
        
        imported = 0
        lines = action_items_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Remove bullet points and numbers
            for prefix in ['- ', '• ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ',
                          '6. ', '7. ', '8. ', '9. ', '10. ']:
                if line.startswith(prefix):
                    line = line[len(prefix):]
                    break
            
            if len(line) > 5:  # Minimum length for valid task
                # Try to extract assignee and deadline
                assignee = ""
                deadline = ""
                description = line
                
                # Look for patterns like "- Task (Assignee, Deadline)"
                if "(" in line and ")" in line:
                    parts = line.split("(")
                    description = parts[0].strip()
                    meta = parts[1].replace(")", "").strip()
                    if "," in meta:
                        meta_parts = meta.split(",")
                        assignee = meta_parts[0].strip()
                        deadline = meta_parts[1].strip() if len(meta_parts) > 1 else ""
                
                self.add_task(
                    description=description,
                    assignee=assignee,
                    deadline=deadline,
                    source=source
                )
                imported += 1
        
        return imported
    
    def to_dataframe_data(self, filter_status: str = "all") -> List[List]:
        """Convert tasks to dataframe format."""
        tasks = self.get_tasks(filter_status)
        data = []
        for t in tasks:
            status_icon = "✅" if t["status"] == "completed" else "⏳"
            data.append([
                t["id"],
                t["description"][:50] + "..." if len(t["description"]) > 50 else t["description"],
                t["assignee"] or "-",
                t["deadline"] or "-",
                status_icon,
                t["source"]
            ])
        return data


# Global instance
_checklist_manager = None

def get_checklist_manager() -> ChecklistManager:
    """Get or create checklist manager instance."""
    global _checklist_manager
    if _checklist_manager is None:
        _checklist_manager = ChecklistManager()
    return _checklist_manager
