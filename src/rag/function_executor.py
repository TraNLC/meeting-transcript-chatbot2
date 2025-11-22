"""Function executor for function calling feature (Sprint 2)."""

import json
import re
from typing import Dict, List, Any, Optional


class FunctionExecutor:
    """Execute functions called by LLM during conversation.
    
    Sprint 2: Implements function calling for meeting transcript analysis.
    """
    
    def __init__(self, transcript: str):
        """Initialize function executor.
        
        Args:
            transcript: Meeting transcript text
        """
        self.transcript = transcript
        self.function_map = {
            "extract_action_items": self.extract_action_items,
            "get_meeting_participants": self.get_meeting_participants,
            "search_transcript": self.search_transcript,
            "extract_decisions": self.extract_decisions
        }
    
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
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def extract_action_items(self, assignee: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Extract action items from transcript.
        
        Args:
            assignee: Filter by assignee name (optional)
            
        Returns:
            Dict with action_items list
        """
        action_items = []
        
        # Enhanced patterns for action items
        patterns = [
            # English patterns
            r"([A-Z][a-z]+)\s+(?:will|needs to|should|must|has to)\s+(.+?)(?:\.|by|before|$)",
            r"([A-Z][a-z]+)\s+(?:is responsible for|is assigned to|will handle)\s+(.+?)(?:\.|$)",
            r"Action item:\s*([A-Z][a-z]+)\s*[-:]\s*(.+?)(?:\.|$)",
            r"TODO:\s*([A-Z][a-z]+)\s*[-:]\s*(.+?)(?:\.|$)",
            
            # Vietnamese patterns
            r"([A-Z][a-z]+)\s+(?:sẽ|cần|phải|được giao)\s+(.+?)(?:\.|vào|trước|$)",
            r"Nhiệm vụ:\s*([A-Z][a-z]+)\s*[-:]\s*(.+?)(?:\.|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, self.transcript, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                person = match.group(1).strip()
                task = match.group(2).strip()
                
                # Skip if person is a common word
                if person.lower() in ['the', 'this', 'that', 'team', 'we', 'they']:
                    continue
                
                # Filter by assignee if specified
                if assignee and person.lower() != assignee.lower():
                    continue
                
                # Extract deadline if present
                deadline = "Not specified"
                deadline_patterns = [
                    r"by\s+(\w+\s+\d+|\w+day)",
                    r"before\s+(\w+\s+\d+)",
                    r"vào\s+(\w+\s+\d+|\w+)",
                    r"trước\s+(\w+\s+\d+)",
                ]
                
                for dl_pattern in deadline_patterns:
                    dl_match = re.search(dl_pattern, task, re.IGNORECASE)
                    if dl_match:
                        deadline = dl_match.group(1)
                        break
                
                action_items.append({
                    "task": task,
                    "assignee": person,
                    "deadline": deadline,
                    "priority": "medium"
                })
        
        # Look for "Action Items" section
        action_section_match = re.search(
            r"(?:Action Items?|Nhiệm vụ|TODO):\s*\n((?:[-*•]\s*.+\n?)+)",
            self.transcript,
            re.IGNORECASE | re.MULTILINE
        )
        
        if action_section_match:
            section_text = action_section_match.group(1)
            # Parse bullet points
            bullet_items = re.findall(r"[-*•]\s*(.+)", section_text)
            
            for item in bullet_items:
                # Try to extract person from item
                person_match = re.match(r"([A-Z][a-z]+)\s*[-:]\s*(.+)", item)
                if person_match:
                    person = person_match.group(1)
                    task = person_match.group(2)
                else:
                    person = "Not assigned"
                    task = item
                
                # Filter by assignee if specified
                if assignee and person.lower() != assignee.lower():
                    continue
                
                action_items.append({
                    "task": task.strip(),
                    "assignee": person,
                    "deadline": "Not specified",
                    "priority": "medium"
                })
        
        return {"action_items": action_items}
    
    def get_meeting_participants(self) -> Dict[str, List[Dict]]:
        """Extract meeting participants.
        
        Returns:
            Dict with participants list
        """
        participants = []
        names_found = set()
        
        # STEP 1: Try to find "Attendees:" line (most reliable)
        # Pattern: "Attendees: Alice, Bob, Charlie, Diana"
        attendees_match = re.search(
            r'(?:Attendees|Participants|Present|Members|Người tham gia|Thành viên):\s*([^\n]+)',
            self.transcript,
            re.IGNORECASE
        )
        
        if attendees_match:
            # Found attendees line - parse it
            names_text = attendees_match.group(1).strip()
            
            # Split by comma, "and", "và"
            name_parts = re.split(r',|\sand\s|\svà\s', names_text)
            
            for name in name_parts:
                name = name.strip()
                # Remove anything in parentheses: "Alice (Manager)" -> "Alice"
                name = re.sub(r'\([^)]*\)', '', name).strip()
                # Only keep if it's a valid name (not empty, not too short)
                if name and len(name) >= 2 and not name.isdigit():
                    names_found.add(name)
            
            # Build result from attendees line
            for name in sorted(names_found):
                spoke_count = len(re.findall(r'^' + re.escape(name) + r':', self.transcript, re.MULTILINE))
                participants.append({
                    "name": name,
                    "role": "Participant",
                    "contribution": f"Spoke {spoke_count} times" if spoke_count > 0 else "Attended meeting"
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
            'blocker', 'blockers', 'issue', 'issues'
        }
        
        lines = self.transcript.split('\n')
        for line in lines:
            line = line.strip()
            # Match "Name: something"
            match = re.match(r'^([A-Z][a-z]+):\s', line)
            if match:
                name = match.group(1)
                # Check if it's not in blacklist
                if name.lower() not in blacklist:
                    names_found.add(name)
        
        # Build result
        for name in sorted(names_found):
            spoke_count = len(re.findall(r'^' + re.escape(name) + r':', self.transcript, re.MULTILINE))
            participants.append({
                "name": name,
                "role": "Participant",
                "contribution": f"Spoke {spoke_count} times"
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


# Example usage
if __name__ == "__main__":
    sample_transcript = """
    Meeting Notes - Nov 22, 2025
    
    Alice: We need to finalize the design by Friday.
    Bob: I will review the code before the deadline.
    Charlie: The team decided to use React for the new project.
    
    Action items:
    - Alice will complete the mockups
    - Bob needs to fix the critical bug
    - Charlie should prepare the demo
    
    Decisions:
    - Agreed to postpone the release to next week
    - Decided to hire two more developers
    """
    
    executor = FunctionExecutor(sample_transcript)
    
    print("=== Available Functions ===")
    print(executor.get_available_functions())
    
    print("\n=== Extract Action Items ===")
    result = executor.execute("extract_action_items", {})
    print(result)
    
    print("\n=== Get Participants ===")
    result = executor.execute("get_meeting_participants", {})
    print(result)
    
    print("\n=== Search 'design' ===")
    result = executor.execute("search_transcript", {"keyword": "design"})
    print(result)
    
    print("\n=== Extract Decisions ===")
    result = executor.execute("extract_decisions", {})
    print(result)
