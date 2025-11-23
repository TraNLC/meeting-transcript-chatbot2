"""Transcript processing utilities for handling large transcripts."""

import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class TranscriptChunk:
    """Represents a chunk of transcript."""
    index: int
    content: str
    start_line: int
    end_line: int
    char_count: int
    word_count: int


class TranscriptProcessor:
    """Process and validate transcripts, split into manageable chunks."""
    
    # Limits
    MAX_CHARS = 50000  # ~50K characters per chunk (safe for most APIs)
    MAX_WORDS = 10000  # ~10K words per chunk
    MIN_CHUNK_SIZE = 1000  # Minimum chunk size to avoid too many small chunks
    
    # Rate limiting
    MAX_CHUNKS_PER_REQUEST = 10  # Maximum chunks to process in one request
    
    def __init__(self, transcript: str):
        """Initialize processor.
        
        Args:
            transcript: Meeting transcript text
        """
        self.transcript = transcript
        self.lines = transcript.split('\n')
        self.total_chars = len(transcript)
        self.total_words = len(transcript.split())
        self.total_lines = len(self.lines)
    
    def validate(self) -> Dict[str, Any]:
        """Validate transcript and return statistics.
        
        Returns:
            Dict with validation results and statistics
        """
        is_valid = True
        warnings = []
        errors = []
        
        # Check if empty
        if not self.transcript.strip():
            errors.append("Transcript is empty")
            is_valid = False
        
        # Check if too short
        if self.total_chars < 100:
            warnings.append("Transcript is very short (< 100 characters)")
        
        # Check if needs chunking
        needs_chunking = (
            self.total_chars > self.MAX_CHARS or 
            self.total_words > self.MAX_WORDS
        )
        
        if needs_chunking:
            estimated_chunks = self.estimate_chunks()
            if estimated_chunks > self.MAX_CHUNKS_PER_REQUEST:
                warnings.append(
                    f"Transcript is very large ({estimated_chunks} chunks). "
                    f"Consider splitting into smaller meetings."
                )
        
        return {
            "is_valid": is_valid,
            "needs_chunking": needs_chunking,
            "statistics": {
                "total_chars": self.total_chars,
                "total_words": self.total_words,
                "total_lines": self.total_lines,
                "estimated_chunks": self.estimate_chunks() if needs_chunking else 1
            },
            "warnings": warnings,
            "errors": errors
        }
    
    def estimate_chunks(self) -> int:
        """Estimate number of chunks needed.
        
        Returns:
            Estimated number of chunks
        """
        char_chunks = (self.total_chars + self.MAX_CHARS - 1) // self.MAX_CHARS
        word_chunks = (self.total_words + self.MAX_WORDS - 1) // self.MAX_WORDS
        return max(char_chunks, word_chunks)
    
    def split_into_chunks(self, strategy: str = "smart") -> List[TranscriptChunk]:
        """Split transcript into chunks.
        
        Args:
            strategy: Splitting strategy
                - "smart": Split at natural boundaries (paragraphs, speakers)
                - "simple": Split by character count
                - "balanced": Balance chunk sizes
        
        Returns:
            List of TranscriptChunk objects
        """
        if strategy == "smart":
            return self._split_smart()
        elif strategy == "balanced":
            return self._split_balanced()
        else:
            return self._split_simple()
    
    def _split_simple(self) -> List[TranscriptChunk]:
        """Simple split by character count.
        
        Returns:
            List of chunks
        """
        chunks = []
        chunk_size = self.MAX_CHARS
        
        for i in range(0, self.total_chars, chunk_size):
            chunk_text = self.transcript[i:i + chunk_size]
            chunks.append(TranscriptChunk(
                index=len(chunks),
                content=chunk_text,
                start_line=0,
                end_line=0,
                char_count=len(chunk_text),
                word_count=len(chunk_text.split())
            ))
        
        return chunks
    
    def _split_smart(self) -> List[TranscriptChunk]:
        """Smart split at natural boundaries (speakers, paragraphs).
        
        Returns:
            List of chunks
        """
        chunks = []
        current_chunk = []
        current_chars = 0
        current_words = 0
        start_line = 0
        
        for line_idx, line in enumerate(self.lines):
            line_chars = len(line)
            line_words = len(line.split())
            
            # Check if adding this line would exceed limits
            would_exceed = (
                current_chars + line_chars > self.MAX_CHARS or
                current_words + line_words > self.MAX_WORDS
            )
            
            # Check if this is a natural boundary (speaker change or empty line)
            is_boundary = (
                line.strip() == "" or 
                re.match(r'^[A-Z][a-z]+:', line) or
                re.match(r'^---', line)
            )
            
            if would_exceed and current_chunk and is_boundary:
                # Create chunk
                chunk_text = '\n'.join(current_chunk)
                chunks.append(TranscriptChunk(
                    index=len(chunks),
                    content=chunk_text,
                    start_line=start_line,
                    end_line=line_idx - 1,
                    char_count=current_chars,
                    word_count=current_words
                ))
                
                # Reset for next chunk
                current_chunk = [line]
                current_chars = line_chars
                current_words = line_words
                start_line = line_idx
            else:
                current_chunk.append(line)
                current_chars += line_chars + 1  # +1 for newline
                current_words += line_words
        
        # Add last chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append(TranscriptChunk(
                index=len(chunks),
                content=chunk_text,
                start_line=start_line,
                end_line=len(self.lines) - 1,
                char_count=current_chars,
                word_count=current_words
            ))
        
        return chunks
    
    def _split_balanced(self) -> List[TranscriptChunk]:
        """Split into balanced chunks of similar size.
        
        Returns:
            List of chunks
        """
        num_chunks = self.estimate_chunks()
        target_size = self.total_chars // num_chunks
        
        chunks = []
        current_chunk = []
        current_chars = 0
        start_line = 0
        
        for line_idx, line in enumerate(self.lines):
            line_chars = len(line)
            
            current_chunk.append(line)
            current_chars += line_chars + 1
            
            # Check if we've reached target size and at a boundary
            is_boundary = (
                line.strip() == "" or 
                re.match(r'^[A-Z][a-z]+:', line)
            )
            
            if current_chars >= target_size and is_boundary:
                chunk_text = '\n'.join(current_chunk)
                chunks.append(TranscriptChunk(
                    index=len(chunks),
                    content=chunk_text,
                    start_line=start_line,
                    end_line=line_idx,
                    char_count=current_chars,
                    word_count=len(chunk_text.split())
                ))
                
                current_chunk = []
                current_chars = 0
                start_line = line_idx + 1
        
        # Add last chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append(TranscriptChunk(
                index=len(chunks),
                content=chunk_text,
                start_line=start_line,
                end_line=len(self.lines) - 1,
                char_count=current_chars,
                word_count=len(chunk_text.split())
            ))
        
        return chunks
    
    def get_summary(self) -> str:
        """Get a summary of the transcript.
        
        Returns:
            Summary string
        """
        validation = self.validate()
        stats = validation['statistics']
        
        summary = f"""
Transcript Summary:
  • Total characters: {stats['total_chars']:,}
  • Total words: {stats['total_words']:,}
  • Total lines: {stats['total_lines']:,}
  • Needs chunking: {'Yes' if validation['needs_chunking'] else 'No'}
  • Estimated chunks: {stats['estimated_chunks']}
"""
        
        if validation['warnings']:
            summary += "\nWarnings:\n"
            for warning in validation['warnings']:
                summary += f"  ⚠️  {warning}\n"
        
        if validation['errors']:
            summary += "\nErrors:\n"
            for error in validation['errors']:
                summary += f"  ❌ {error}\n"
        
        return summary
