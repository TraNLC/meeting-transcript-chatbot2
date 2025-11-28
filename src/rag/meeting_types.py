"""Meeting type detection and specialized functions."""

import re
from typing import Dict, List, Any
from enum import Enum


class MeetingType(Enum):
    """Supported meeting types."""
    MEETING = "meeting"
    WORKSHOP = "workshop"
    BRAINSTORMING = "brainstorming"


class MeetingTypeDetector:
    """Detect meeting type from transcript."""
    
    # Keywords for each meeting type
    KEYWORDS = {
        MeetingType.WORKSHOP: [
            "workshop", "training", "exercise", "activity", "practice",
            "learning", "tutorial", "hands-on", "lab", "demo",
            "hội thảo", "đào tạo", "bài tập", "thực hành", "học"
        ],
        MeetingType.BRAINSTORMING: [
            "brainstorm", "idea", "suggest", "propose", "creative",
            "innovation", "concept", "vote", "prioritize",
            "động não", "ý tưởng", "đề xuất", "sáng tạo", "bỏ phiếu"
        ],
        MeetingType.MEETING: [
            "meeting", "agenda", "action item", "decision", "discuss",
            "update", "status", "progress", "review",
            "cuộc họp", "chương trình", "nhiệm vụ", "quyết định", "thảo luận"
        ]
    }
    
    @classmethod
    def detect(cls, transcript: str) -> MeetingType:
        """Auto-detect meeting type from transcript.
        
        Args:
            transcript: Meeting transcript text
            
        Returns:
            Detected meeting type
        """
        transcript_lower = transcript.lower()
        scores = {}
        
        for meeting_type, keywords in cls.KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in transcript_lower)
            scores[meeting_type] = score
        
        # Return type with highest score, default to MEETING
        if not scores or max(scores.values()) == 0:
            return MeetingType.MEETING
        
        return max(scores, key=scores.get)
    
    @classmethod
    def get_available_types(cls) -> Dict[str, str]:
        """Get available meeting types with descriptions.
        
        Returns:
            Dict mapping type codes to descriptions
        """
        return {
            "meeting": "Regular Meeting - Action items, decisions, discussions",
            "workshop": "Workshop/Training - Exercises, Q&A, key learnings",
            "brainstorming": "Brainstorming Session - Ideas, voting, creativity"
        }


class WorkshopFunctions:
    """Specialized functions for workshop transcripts."""
    
    @staticmethod
    def extract_key_learnings(transcript: str) -> Dict[str, List[str]]:
        """Extract key learnings from workshop.
        
        Args:
            transcript: Workshop transcript
            
        Returns:
            Dict with key learnings
        """
        learnings = []
        
        # Patterns for learnings
        patterns = [
            r"(?:key learning|learned that|takeaway|important point):\s*(.+?)(?:\.|$)",
            r"(?:remember|note that|keep in mind):\s*(.+?)(?:\.|$)",
            r"(?:học được|ghi nhớ|điểm quan trọng):\s*(.+?)(?:\.|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, transcript, re.IGNORECASE)
            for match in matches:
                learning = match.group(1).strip()
                if len(learning) > 10:  # Filter out too short
                    learnings.append(learning)
        
        return {"key_learnings": learnings}
    
    @staticmethod
    def extract_exercises(transcript: str) -> Dict[str, List[Dict]]:
        """Extract exercises/activities from workshop.
        
        Args:
            transcript: Workshop transcript
            
        Returns:
            Dict with exercises
        """
        exercises = []
        
        # Pattern: "Exercise: Build a todo app"
        patterns = [
            r"(?:Exercise|Activity|Task|Practice)\s*\d*:\s*(.+?)(?:\n|$)",
            r"(?:Bài tập|Hoạt động|Thực hành)\s*\d*:\s*(.+?)(?:\n|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, transcript, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                exercise_text = match.group(1).strip()
                exercises.append({
                    "title": exercise_text,
                    "type": "exercise"
                })
        
        return {"exercises": exercises}
    
    @staticmethod
    def extract_qa_pairs(transcript: str) -> Dict[str, List[Dict]]:
        """Extract Q&A pairs from workshop.
        
        Args:
            transcript: Workshop transcript
            
        Returns:
            Dict with Q&A pairs
        """
        qa_pairs = []
        lines = transcript.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if line is a question
            is_question = (
                line.endswith('?') or
                line.lower().startswith(('question:', 'q:', 'câu hỏi:'))
            )
            
            if is_question:
                question = line
                # Look for answer in next few lines
                answer = ""
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line.lower().startswith(('answer:', 'a:', 'trả lời:')):
                        answer = next_line
                        break
                    elif next_line and not next_line.endswith('?'):
                        answer = next_line
                        break
                
                if answer:
                    qa_pairs.append({
                        "question": question,
                        "answer": answer
                    })
            
            i += 1
        
        return {"qa_pairs": qa_pairs}


class BrainstormingFunctions:
    """Specialized functions for brainstorming transcripts."""
    
    @staticmethod
    def extract_ideas(transcript: str) -> Dict[str, List[Dict]]:
        """Extract ideas from brainstorming session.
        
        Args:
            transcript: Brainstorming transcript
            
        Returns:
            Dict with ideas
        """
        ideas = []
        
        # Patterns for ideas
        patterns = [
            r"(?:idea|suggestion|propose|what if|how about):\s*(.+?)(?:\.|$)",
            r"(?:I suggest|I propose|We could|Let's):\s*(.+?)(?:\.|$)",
            r"(?:ý tưởng|đề xuất|gợi ý):\s*(.+?)(?:\.|$)",
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, transcript, re.IGNORECASE)
            for match in matches:
                idea_text = match.group(1).strip()
                if len(idea_text) > 10:
                    ideas.append({
                        "idea": idea_text,
                        "category": "general"
                    })
        
        # Also look for bullet points with ideas
        bullet_pattern = r"[-•*]\s*(.+?)(?:\n|$)"
        matches = re.finditer(bullet_pattern, transcript, re.MULTILINE)
        for match in matches:
            idea_text = match.group(1).strip()
            if len(idea_text) > 10 and not idea_text.startswith(('Action', 'Decision')):
                ideas.append({
                    "idea": idea_text,
                    "category": "general"
                })
        
        return {"ideas": ideas}
    
    @staticmethod
    def extract_concerns(transcript: str) -> Dict[str, List[str]]:
        """Extract concerns/challenges from brainstorming.
        
        Args:
            transcript: Brainstorming transcript
            
        Returns:
            Dict with concerns
        """
        concerns = []
        
        # Patterns for concerns - more flexible
        patterns = [
            r"(?:Concern|concern|Worry|worry|Problem|problem|Challenge|challenge|Issue|issue|Risk|risk):\s*(.+?)(?:\n|$)",
            r"(?:Raised by|raised by):\s*.+?\n",  # Skip "Raised by" lines
            r"(?:Lo ngại|lo ngại|Vấn đề|vấn đề|Thách thức|thách thức|Rủi ro|rủi ro):\s*(.+?)(?:\n|$)",
        ]
        
        # Split by lines and look for concern markers
        lines = transcript.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if line starts with concern keywords
            concern_keywords = [
                'Concern:', 'concern:', 'Challenge:', 'challenge:', 
                'Problem:', 'problem:', 'Risk:', 'risk:',
                'Lo ngại:', 'Vấn đề:', 'Thách thức:', 'Rủi ro:'
            ]
            
            for keyword in concern_keywords:
                if line.startswith(keyword):
                    concern_text = line.replace(keyword, '').strip()
                    if len(concern_text) > 10 and 'Raised by' not in concern_text:
                        concerns.append(concern_text)
                    break
        
        return {"concerns": concerns}
    
    @staticmethod
    def categorize_ideas(ideas_result: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """Categorize ideas by topic.
        
        Args:
            ideas_result: Result from extract_ideas
            
        Returns:
            Dict with categorized ideas
        """
        categories = {
            "UI/UX": [],
            "Features": [],
            "Technical": [],
            "Business": [],
            "Other": []
        }
        
        # Simple keyword-based categorization
        category_keywords = {
            "UI/UX": ["design", "interface", "user", "ui", "ux", "layout"],
            "Features": ["feature", "functionality", "add", "new"],
            "Technical": ["api", "database", "code", "architecture", "performance"],
            "Business": ["revenue", "cost", "market", "customer", "sales"]
        }
        
        for idea in ideas_result.get("ideas", []):
            idea_text = idea["idea"].lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword in idea_text for keyword in keywords):
                    categories[category].append(idea)
                    categorized = True
                    break
            
            if not categorized:
                categories["Other"].append(idea)
        
        return {"categorized_ideas": categories}
