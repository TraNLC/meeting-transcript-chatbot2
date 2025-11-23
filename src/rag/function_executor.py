"""Function executor for function calling feature (Sprint 2)."""

import json
import re
from typing import Dict, List, Any, Optional, Literal

try:
    from .translator import ContentTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("Warning: Translation module not available. Install 'deep-translator' for full translation support.")


class FunctionExecutor:
    """Execute functions called by LLM during conversation.
    
    Sprint 2: Implements function calling for meeting transcript analysis.
    """
    
    def __init__(
        self, 
        transcript: str, 
        output_language: str = "vi",
        enable_translation: bool = True
    ):
        """Initialize function executor.
        
        Args:
            transcript: Meeting transcript text
            output_language: Output language code (vi, en, ja, ko, zh-CN, es, fr, de, etc.)
            enable_translation: Enable full content translation (requires deep-translator)
        """
        self.transcript = transcript
        self.output_language = output_language
        self.enable_translation = enable_translation and TRANSLATION_AVAILABLE
        
        # Initialize translator if enabled
        if self.enable_translation:
            try:
                self.translator = ContentTranslator(output_language)
            except Exception as e:
                print(f"Translation initialization failed: {e}")
                self.enable_translation = False
                self.translator = None
        else:
            self.translator = None
        self.function_map = {
            "extract_action_items": self.extract_action_items,
            "get_meeting_participants": self.get_meeting_participants,
            "search_transcript": self.search_transcript,
            "extract_decisions": self.extract_decisions
        }
        
        # Translation dictionaries
        self.translations = {
            "vi": {
                "participants": "participants",
                "name": "name",
                "role": "role",
                "contribution": "contribution",
                "spoke_times": "Phát biểu {count} lần",
                "attended_meeting": "Tham dự cuộc họp",
                "action_items": "action_items",
                "task": "task",
                "assignee": "assignee",
                "deadline": "deadline",
                "priority": "priority",
                "not_specified": "Chưa xác định",
                "not_assigned": "Chưa phân công",
                "medium": "trung bình",
                "high": "cao",
                "low": "thấp",
                "decisions": "decisions",
                "decision": "decision",
                "context": "context",
                "impact": "impact",
                "mentioned_in_discussion": "Được đề cập trong cuộc thảo luận",
                "to_be_determined": "Cần xác định",
                "keyword": "keyword",
                "total_matches": "total_matches",
                "results": "results",
                "line_number": "line_number",
                "matched_line": "matched_line",
                "participant": "Người tham gia"
            },
            "en": {
                "participants": "participants",
                "name": "name",
                "role": "role",
                "contribution": "contribution",
                "spoke_times": "Spoke {count} times",
                "attended_meeting": "Attended meeting",
                "action_items": "action_items",
                "task": "task",
                "assignee": "assignee",
                "deadline": "deadline",
                "priority": "priority",
                "not_specified": "Not specified",
                "not_assigned": "Not assigned",
                "medium": "medium",
                "high": "high",
                "low": "low",
                "decisions": "decisions",
                "decision": "decision",
                "context": "context",
                "impact": "impact",
                "mentioned_in_discussion": "Mentioned in meeting discussion",
                "to_be_determined": "To be determined",
                "keyword": "keyword",
                "total_matches": "total_matches",
                "results": "results",
                "line_number": "line_number",
                "matched_line": "matched_line",
                "participant": "Participant"
            }
        }
    
    def _translate(self, key: str) -> str:
        """Get translated text for a key.
        
        Args:
            key: Translation key
            
        Returns:
            Translated text
        """
        return self.translations[self.output_language].get(key, key)
    
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a function by name.
        
        Args:
            function_name: Name of function to execute
            arguments: Function arguments as dict
            
        Returns:
            Function result as JSON string
            
        Raises:
            ValueError: If function not found
        """
        if function_name not in self.function_map:
            raise ValueError(f"Function '{function_name}' not found")
        
        func = self.function_map[function_name]
        result = func(**arguments)
        
        # Apply translation if enabled
        if self.enable_translation and self.translator:
            result = self._translate_result(result, function_name)
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _translate_result(self, result: Dict[str, Any], function_name: str) -> Dict[str, Any]:
        """Translate result based on function type.
        
        Args:
            result: Function result
            function_name: Name of the function
            
        Returns:
            Translated result
        """
        # Map function names to result types
        type_map = {
            "get_meeting_participants": "participants",
            "extract_action_items": "action_items",
            "extract_decisions": "decisions",
            "search_transcript": "search"
        }
        
        result_type = type_map.get(function_name)
        if result_type:
            return self.translator.translate_result(result, result_type)
        
        return result
    
    def extract_action_items(self, assignee: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Extract action items from transcript.
        
        Args:
            assignee: Filter by assignee name (optional)
            
        Returns:
            Dict with action_items list
        """
        action_items = []
        seen_tasks = set()  # To avoid duplicates
        
        # Get list of known participants first
        participants_result = self.get_meeting_participants()
        known_names = {p['name'] for p in participants_result['participants']}
        
        # Enhanced patterns for action items - only match known participant names
        patterns = [
            # English patterns
            r"\b(" + "|".join(re.escape(name) for name in known_names) + r")\s+(?:will|needs to|should|must|has to)\s+(.+?)(?:\.|by|before|$)",
            r"\b(" + "|".join(re.escape(name) for name in known_names) + r")\s+(?:is responsible for|is assigned to|will handle)\s+(.+?)(?:\.|$)",
            
            # Vietnamese patterns - match known names
            r"\b(" + "|".join(re.escape(name) for name in known_names) + r")\s+(?:sẽ|cần|phải|được giao)\s+(.+?)(?:\.|vào|trước|$)",
        ]
        
        for pattern in patterns:
            if not known_names:  # Skip if no names found
                continue
                
            matches = re.finditer(pattern, self.transcript, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                person = match.group(1).strip()
                task = match.group(2).strip()
                
                # Skip very short tasks
                if len(task) < 5:
                    continue
                
                # Filter by assignee if specified
                if assignee and person.lower() != assignee.lower():
                    continue
                
                # Extract deadline if present
                deadline = "Not specified"
                deadline_patterns = [
                    r"(?:by|before)\s+(\w+\s+\d+(?:/\d+)?|\w+day)",
                    r"(?:vào|trước)\s+(\w+\s+\w+\s+(?:này|sau|tới)|ngày\s+\d+/\d+|\d+/\d+)",
                ]
                
                for dl_pattern in deadline_patterns:
                    dl_match = re.search(dl_pattern, task, re.IGNORECASE)
                    if dl_match:
                        deadline = dl_match.group(1)
                        break
                
                # Create unique key to avoid duplicates
                task_key = f"{person}:{task[:50]}"
                if task_key not in seen_tasks:
                    seen_tasks.add(task_key)
                    action_items.append({
                        "task": task,
                        "assignee": person,
                        "deadline": deadline,
                        "priority": "medium"
                    })
        
        # Look for summary section with action items (more reliable)
        summary_patterns = [
            r"[-•]\s*(" + "|".join(re.escape(name) for name in known_names) + r")\s+(?:sẽ|cần|phải)\s+(.+?)(?:\n|$)",
            r"[-•]\s*(" + "|".join(re.escape(name) for name in known_names) + r")\s+(?:will|needs to|should)\s+(.+?)(?:\n|$)",
        ]
        
        for pattern in summary_patterns:
            if not known_names:
                continue
                
            matches = re.finditer(pattern, self.transcript, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                person = match.group(1).strip()
                task = match.group(2).strip()
                
                # Filter by assignee if specified
                if assignee and person.lower() != assignee.lower():
                    continue
                
                # Extract deadline
                deadline = "Not specified"
                deadline_patterns = [
                    r"(?:trước|vào)\s+(thứ\s+\w+|ngày\s+\d+/\d+|\d+/\d+)",
                    r"(?:by|before)\s+(\w+\s+\d+|\w+day)",
                ]
                
                for dl_pattern in deadline_patterns:
                    dl_match = re.search(dl_pattern, task, re.IGNORECASE)
                    if dl_match:
                        deadline = dl_match.group(1)
                        break
                
                task_key = f"{person}:{task[:50]}"
                if task_key not in seen_tasks:
                    seen_tasks.add(task_key)
                    action_items.append({
                        "task": task.strip(),
                        "assignee": person,
                        "deadline": deadline,
                        "priority": "medium"
                    })
        
        return {"action_items": action_items}
    
    def get_meeting_participants(self) -> Dict[str, List[Dict]]:
        """Extract meeting participants.
        
        Returns:
            Dict with participants list
        """
        participants = []
        participant_info = {}  # name -> role mapping
        
        # STEP 1: Try to find "Attendees:" line with roles in parentheses
        attendees_match = re.search(
            r'(?:Attendees|Participants|Present|Members|Người tham gia|Thành viên):\s*([^\n]+)',
            self.transcript,
            re.IGNORECASE
        )
        
        if attendees_match:
            # Found attendees line - parse it
            names_text = attendees_match.group(1).strip()
            
            # Split by comma, "and"
            name_parts = re.split(r',|\sand\s|\svà\s', names_text)
            
            for part in name_parts:
                part = part.strip()
                
                # Try to extract name and role from parentheses
                role_match = re.match(r'([^(]+)\s*\(([^)]+)\)', part)
                if role_match:
                    name = role_match.group(1).strip()
                    role = role_match.group(2).strip()
                    participant_info[name] = role
                else:
                    # No role in parentheses, just name
                    name = part.strip()
                    if name and len(name) >= 2 and not name.isdigit():
                        participant_info[name] = "Participant"
            
            # Build result from attendees line
            for name, role in sorted(participant_info.items()):
                spoke_count = len(re.findall(r'^' + re.escape(name) + r':', self.transcript, re.MULTILINE))
                
                # Use simple format, will be translated later if needed
                if spoke_count > 0:
                    contribution = f"Spoke {spoke_count} times"
                else:
                    contribution = "Attended meeting"
                
                participants.append({
                    "name": name,
                    "role": role,
                    "contribution": contribution
                })
            
            return {"participants": participants}
        
        # STEP 2: No "Attendees:" line found - extract from speaker format
        # Look for lines starting with "Name: ..."
        
        # Blacklist of words that are NOT names
        blacklist = {
            'date', 'time', 'location', 'venue', 'subject', 'topic', 'agenda',
            'note', 'notes', 'action', 'actions', 'decision', 'decisions',
            'attendees', 'participants', 'present', 'members',
            'summary', 'conclusion', 'next', 'follow', 'meeting',
            'discussion', 'item', 'items', 'task', 'tasks', 'todo',
            'blocker', 'blockers', 'issue', 'issues', 'ngày', 'thời'
        }
        
        names_found = set()
        lines = self.transcript.split('\n')
        for line in lines:
            line = line.strip()
            # Match "Name: something" - support Vietnamese names with multiple capital letters
            # Must be 2+ letters, start with capital letter, followed by lowercase
            match = re.match(r'^([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{1,}(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)?):\s', line)
            if match:
                name = match.group(1).strip()
                # Additional validation: name should be 2-30 chars and not contain numbers
                if (len(name) >= 2 and len(name) <= 30 and 
                    not any(char.isdigit() for char in name) and
                    name.lower() not in blacklist):
                    names_found.add(name)
        
        # Build result
        for name in sorted(names_found):
            spoke_count = len(re.findall(r'^' + re.escape(name) + r':', self.transcript, re.MULTILINE))
            contribution = f"Spoke {spoke_count} times"
            participants.append({
                "name": name,
                "role": "Participant",
                "contribution": contribution
            })
        
        return {"participants": participants}
    
    def search_transcript(self, keyword: str, context_lines: int = 2) -> Dict[str, List[Dict]]:
        """Search for keyword in transcript.
        
        Args:
            keyword: Keyword to search for
            context_lines: Number of context lines around match
            
        Returns:
            Dict with search results
        """
        results = []
        lines = self.transcript.split('\n')
        
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                # Get context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = '\n'.join(lines[start:end])
                
                results.append({
                    "line_number": i + 1,
                    "matched_line": line.strip(),
                    "context": context,
                    "keyword": keyword
                })
        
        return {
            "keyword": keyword,
            "total_matches": len(results),
            "results": results
        }
    
    def extract_decisions(self) -> Dict[str, List[Dict]]:
        """Extract decisions from transcript.
        
        Returns:
            Dict with decisions list
        """
        decisions = []
        
        # Pattern: "decided to", "agreed to", "conclusion"
        patterns = [
            r"(?:decided|agreed|concluded)\s+(?:to|that)\s+(.+?)(?:\.|,|$)",
            r"(?:quyết định|đồng ý|kết luận)\s+(.+?)(?:\.|,|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, self.transcript, re.IGNORECASE)
            for match in matches:
                decision_text = match.group(1).strip()
                
                decisions.append({
                    "decision": decision_text,
                    "context": "Mentioned in meeting discussion",
                    "impact": "To be determined"
                })
        
        return {"decisions": decisions}
    
    def get_available_functions(self) -> List[str]:
        """Get list of available function names.
        
        Returns:
            List of function names
        """
        return list(self.function_map.keys())
