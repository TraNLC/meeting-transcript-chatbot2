"""Chunked function executor for handling large transcripts."""

import time
from typing import Dict, List, Any, Optional
from .function_executor import FunctionExecutor
from .transcript_processor import TranscriptProcessor, TranscriptChunk


class ChunkedFunctionExecutor:
    """Execute functions on large transcripts by splitting into chunks."""
    
    def __init__(
        self,
        transcript: str,
        output_language: str = "vi",
        enable_translation: bool = True,
        chunk_strategy: str = "smart",
        rate_limit_delay: float = 0.5
    ):
        """Initialize chunked executor.
        
        Args:
            transcript: Meeting transcript text
            output_language: Output language code
            enable_translation: Enable full content translation
            chunk_strategy: Chunking strategy (smart, simple, balanced)
            rate_limit_delay: Delay between chunk processing (seconds)
        """
        self.transcript = transcript
        self.output_language = output_language
        self.enable_translation = enable_translation
        self.chunk_strategy = chunk_strategy
        self.rate_limit_delay = rate_limit_delay
        
        # Process transcript
        self.processor = TranscriptProcessor(transcript)
        self.validation = self.processor.validate()
        
        # Create chunks if needed
        if self.validation['needs_chunking']:
            self.chunks = self.processor.split_into_chunks(strategy=chunk_strategy)
            self.is_chunked = True
        else:
            self.chunks = [TranscriptChunk(
                index=0,
                content=transcript,
                start_line=0,
                end_line=len(transcript.split('\n')),
                char_count=len(transcript),
                word_count=len(transcript.split())
            )]
            self.is_chunked = False
    
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Execute function on transcript (with chunking if needed).
        
        Args:
            function_name: Name of function to execute
            arguments: Function arguments
            
        Returns:
            Merged result as JSON string
        """
        if not self.is_chunked:
            # Single chunk - execute directly
            executor = FunctionExecutor(
                self.transcript,
                output_language=self.output_language,
                enable_translation=self.enable_translation
            )
            return executor.execute(function_name, arguments)
        
        # Multiple chunks - execute on each and merge
        print(f"📦 Processing {len(self.chunks)} chunks...")
        
        chunk_results = []
        for i, chunk in enumerate(self.chunks):
            print(f"  Processing chunk {i+1}/{len(self.chunks)}...", end=" ")
            
            # Create executor for this chunk
            executor = FunctionExecutor(
                chunk.content,
                output_language=self.output_language,
                enable_translation=self.enable_translation
            )
            
            # Execute function
            result_json = executor.execute(function_name, arguments)
            chunk_results.append(result_json)
            
            print("✓")
            
            # Rate limiting
            if i < len(self.chunks) - 1:
                time.sleep(self.rate_limit_delay)
        
        # Merge results
        print("  Merging results...")
        merged = self._merge_results(chunk_results, function_name)
        
        import json
        return json.dumps(merged, ensure_ascii=False, indent=2)
    
    def _merge_results(
        self, 
        chunk_results: List[str], 
        function_name: str
    ) -> Dict[str, Any]:
        """Merge results from multiple chunks.
        
        Args:
            chunk_results: List of JSON result strings
            function_name: Name of the function
            
        Returns:
            Merged result dictionary
        """
        import json
        
        parsed_results = [json.loads(r) for r in chunk_results]
        
        if function_name == "get_meeting_participants":
            return self._merge_participants(parsed_results)
        elif function_name == "extract_action_items":
            return self._merge_action_items(parsed_results)
        elif function_name == "extract_decisions":
            return self._merge_decisions(parsed_results)
        elif function_name == "search_transcript":
            return self._merge_search_results(parsed_results)
        else:
            # Default: just concatenate lists
            return parsed_results[0] if parsed_results else {}
    
    def _merge_participants(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Merge participant results from chunks.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Merged participants
        """
        # Collect all participants
        all_participants = {}
        
        for result in results:
            for p in result.get('participants', []):
                name = p['name']
                if name in all_participants:
                    # Merge contribution counts
                    existing = all_participants[name]
                    # Extract count from contribution text
                    import re
                    existing_match = re.search(r'(\d+)', existing['contribution'])
                    new_match = re.search(r'(\d+)', p['contribution'])
                    
                    if existing_match and new_match:
                        total_count = int(existing_match.group(1)) + int(new_match.group(1))
                        # Update contribution with new count
                        if 'Spoke' in existing['contribution']:
                            existing['contribution'] = f"Spoke {total_count} times"
                        else:
                            existing['contribution'] = f"Phát biểu {total_count} lần"
                else:
                    all_participants[name] = p.copy()
        
        return {"participants": list(all_participants.values())}
    
    def _merge_action_items(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Merge action items from chunks.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Merged action items
        """
        all_items = []
        seen_tasks = set()
        
        for result in results:
            for item in result.get('action_items', []):
                # Create unique key to avoid duplicates
                task_key = f"{item['assignee']}:{item['task'][:50]}"
                if task_key not in seen_tasks:
                    seen_tasks.add(task_key)
                    all_items.append(item)
        
        return {"action_items": all_items}
    
    def _merge_decisions(self, results: List[Dict]) -> Dict[str, List[Dict]]:
        """Merge decisions from chunks.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Merged decisions
        """
        all_decisions = []
        seen_decisions = set()
        
        for result in results:
            for decision in result.get('decisions', []):
                # Create unique key
                decision_key = decision['decision'][:50]
                if decision_key not in seen_decisions:
                    seen_decisions.add(decision_key)
                    all_decisions.append(decision)
        
        return {"decisions": all_decisions}
    
    def _merge_search_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Merge search results from chunks.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Merged search results
        """
        all_results = []
        total_matches = 0
        keyword = results[0].get('keyword', '') if results else ''
        
        for result in results:
            total_matches += result.get('total_matches', 0)
            all_results.extend(result.get('results', []))
        
        return {
            "keyword": keyword,
            "total_matches": total_matches,
            "results": all_results
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the transcript and chunking.
        
        Returns:
            Info dictionary
        """
        return {
            "validation": self.validation,
            "is_chunked": self.is_chunked,
            "num_chunks": len(self.chunks),
            "chunks": [
                {
                    "index": c.index,
                    "chars": c.char_count,
                    "words": c.word_count,
                    "lines": f"{c.start_line}-{c.end_line}"
                }
                for c in self.chunks
            ] if self.is_chunked else []
        }
