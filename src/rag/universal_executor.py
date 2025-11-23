"""Universal executor supporting multiple meeting types."""

import json
from typing import Dict, List, Any, Optional
from .chunked_executor import ChunkedFunctionExecutor
from .meeting_types import (
    MeetingType, 
    MeetingTypeDetector,
    WorkshopFunctions,
    BrainstormingFunctions
)


class UniversalMeetingExecutor:
    """Execute functions based on meeting type."""
    
    def __init__(
        self,
        transcript: str,
        meeting_type: Optional[str] = None,
        output_language: str = "vi",
        enable_translation: bool = True,
        chunk_strategy: str = "smart",
        rate_limit_delay: float = 0.5
    ):
        """Initialize universal executor.
        
        Args:
            transcript: Meeting transcript text
            meeting_type: Type of meeting (meeting, workshop, brainstorming) or None for auto-detect
            output_language: Output language code
            enable_translation: Enable full content translation
            chunk_strategy: Chunking strategy
            rate_limit_delay: Delay between chunk processing
        """
        self.transcript = transcript
        self.output_language = output_language
        
        # Detect or set meeting type
        if meeting_type:
            self.meeting_type = MeetingType(meeting_type)
        else:
            self.meeting_type = MeetingTypeDetector.detect(transcript)
        
        # Create base executor
        self.base_executor = ChunkedFunctionExecutor(
            transcript,
            output_language=output_language,
            enable_translation=enable_translation,
            chunk_strategy=chunk_strategy,
            rate_limit_delay=rate_limit_delay
        )
        
        # Initialize specialized functions
        self.workshop_funcs = WorkshopFunctions()
        self.brainstorm_funcs = BrainstormingFunctions()
    
    def get_available_functions(self) -> List[str]:
        """Get available functions for current meeting type.
        
        Returns:
            List of function names
        """
        # Base functions available for all types
        base_functions = [
            "get_meeting_participants",
            "search_transcript"
        ]
        
        # Type-specific functions
        if self.meeting_type == MeetingType.MEETING:
            return base_functions + [
                "extract_action_items",
                "extract_decisions"
            ]
        
        elif self.meeting_type == MeetingType.WORKSHOP:
            return base_functions + [
                "extract_key_learnings",
                "extract_exercises",
                "extract_qa_pairs"
            ]
        
        elif self.meeting_type == MeetingType.BRAINSTORMING:
            return base_functions + [
                "extract_ideas",
                "extract_concerns",
                "categorize_ideas"
            ]
        
        return base_functions
    
    def execute(self, function_name: str, arguments: Dict[str, Any] = None) -> str:
        """Execute a function.
        
        Args:
            function_name: Name of function to execute
            arguments: Function arguments
            
        Returns:
            Function result as JSON string
        """
        if arguments is None:
            arguments = {}
        
        # Check if function is available for this meeting type
        available = self.get_available_functions()
        if function_name not in available:
            raise ValueError(
                f"Function '{function_name}' not available for {self.meeting_type.value}. "
                f"Available: {', '.join(available)}"
            )
        
        # Execute base functions
        if function_name in ["get_meeting_participants", "search_transcript", 
                             "extract_action_items", "extract_decisions"]:
            return self.base_executor.execute(function_name, arguments)
        
        # Execute workshop functions
        elif function_name == "extract_key_learnings":
            result = self.workshop_funcs.extract_key_learnings(self.transcript)
            return self._translate_and_format(result)
        
        elif function_name == "extract_exercises":
            result = self.workshop_funcs.extract_exercises(self.transcript)
            return self._translate_and_format(result)
        
        elif function_name == "extract_qa_pairs":
            result = self.workshop_funcs.extract_qa_pairs(self.transcript)
            return self._translate_and_format(result)
        
        # Execute brainstorming functions
        elif function_name == "extract_ideas":
            result = self.brainstorm_funcs.extract_ideas(self.transcript)
            return self._translate_and_format(result)
        
        elif function_name == "extract_concerns":
            result = self.brainstorm_funcs.extract_concerns(self.transcript)
            return self._translate_and_format(result)
        
        elif function_name == "categorize_ideas":
            # First extract ideas
            ideas_result = self.brainstorm_funcs.extract_ideas(self.transcript)
            result = self.brainstorm_funcs.categorize_ideas(ideas_result)
            return self._translate_and_format(result)
        
        else:
            raise ValueError(f"Unknown function: {function_name}")
    
    def _translate_and_format(self, result: Dict[str, Any]) -> str:
        """Translate and format result.
        
        Args:
            result: Result dictionary
            
        Returns:
            JSON string
        """
        # TODO: Add translation support for specialized functions
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def execute_all(self) -> Dict[str, Any]:
        """Execute all available functions for this meeting type.
        
        Returns:
            Dict with all results
        """
        results = {
            "meeting_type": self.meeting_type.value,
            "functions": {}
        }
        
        for function_name in self.get_available_functions():
            try:
                if function_name == "search_transcript":
                    continue  # Skip search as it needs keyword
                
                print(f"  Executing {function_name}...")
                result_json = self.execute(function_name, {})
                results["functions"][function_name] = json.loads(result_json)
            except Exception as e:
                results["functions"][function_name] = {"error": str(e)}
        
        return results
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the executor.
        
        Returns:
            Info dictionary
        """
        base_info = self.base_executor.get_info()
        return {
            **base_info,
            "meeting_type": self.meeting_type.value,
            "available_functions": self.get_available_functions()
        }
