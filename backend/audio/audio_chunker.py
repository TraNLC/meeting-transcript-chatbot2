"""Audio-specific chunking with timestamps and speakers."""

from typing import List, Dict, Any


def chunk_audio_transcript(
    segments: List[Dict],
    time_window: int = 60,
    max_tokens: int = 512
) -> List[Dict[str, Any]]:
    """
    Chunk audio transcript by time windows and speakers.
    
    Optimized for RAG retrieval with:
    - Time-based boundaries (default 60s)
    - Token limits (default 512)
    - Speaker awareness
    - Overlapping for context
    
    Args:
        segments: WhisperX output segments from Colab
            [{"start": 0.5, "end": 3.2, "text": "...", "speaker": "SPEAKER_00"}, ...]
        time_window: Maximum duration per chunk (seconds)
        max_tokens: Maximum tokens per chunk
    
    Returns:
        List of chunks with metadata:
        [{
            "chunk_id": "chunk_0.0",
            "text": "[00:00] **User 1**: Hello\n[00:05] **User 2**: Hi",
            "start_time": 0.0,
            "end_time": 58.5,
            "duration": 58.5,
            "speakers": ["SPEAKER_00", "SPEAKER_01"],
            "metadata": {...}
        }, ...]
    """
    chunks = []
    current_chunk = {
        "segments": [],
        "speakers": set(),
        "start_time": None,
        "end_time": None,
        "text": ""
    }
    
    for seg in segments:
        start = seg.get('start', 0)
        end = seg.get('end', 0)
        text = seg.get('text', '').strip()
        speaker = seg.get('speaker', 'Unknown')
        
        if not text:
            continue
        
        # Initialize first chunk
        if current_chunk["start_time"] is None:
            current_chunk["start_time"] = start
        
        # Calculate current metrics
        duration = end - current_chunk["start_time"]
        token_count = len(current_chunk["text"].split()) + len(text.split())
        
        # Determine if we should split
        should_split = (
            duration > time_window or
            token_count > max_tokens
        )
        
        if should_split and current_chunk["segments"]:
            # Finalize and save current chunk
            chunks.append(_finalize_chunk(current_chunk))
            
            # Start new chunk with overlap (last 2 segments)
            overlap_segments = current_chunk["segments"][-2:]
            current_chunk = {
                "segments": overlap_segments,
                "speakers": {s.get('speaker') for s in overlap_segments},
                "start_time": overlap_segments[0]['start'] if overlap_segments else start,
                "end_time": None,
                "text": ' '.join([s['text'] for s in overlap_segments])
            }
        
        # Add current segment to chunk
        current_chunk["segments"].append(seg)
        current_chunk["speakers"].add(speaker)
        current_chunk["end_time"] = end
        current_chunk["text"] += f" {text}"
    
    # Add final chunk
    if current_chunk["segments"]:
        chunks.append(_finalize_chunk(current_chunk))
    
    return chunks


def _finalize_chunk(chunk_data: Dict) -> Dict[str, Any]:
    """
    Format chunk with speaker labels and timestamps.
    
    Maps SPEAKER_00 → User 1, SPEAKER_01 → User 2, etc.
    Formats text as: "[MM:SS] **User X**: text"
    """
    # Map speakers to User 1, User 2, User 3...
    speaker_map = {}
    for i, speaker in enumerate(sorted(chunk_data["speakers"]), 1):
        speaker_map[speaker] = f"User {i}"
    
    # Format text with timestamps and speakers
    formatted_lines = []
    for seg in chunk_data["segments"]:
        # Format timestamp
        m = int(seg['start'] // 60)
        s = int(seg['start'] % 60)
        time_str = f"{m:02d}:{s:02d}"
        
        # Get speaker label
        speaker_label = speaker_map.get(seg.get('speaker'), 'Unknown')
        
        # Format line
        formatted_lines.append(
            f"[{time_str}] **{speaker_label}**: {seg['text']}"
        )
    
    return {
        "chunk_id": f"chunk_{chunk_data['start_time']:.1f}",
        "text": '\n'.join(formatted_lines),
        "start_time": chunk_data["start_time"],
        "end_time": chunk_data["end_time"],
        "duration": chunk_data["end_time"] - chunk_data["start_time"],
        "speakers": list(chunk_data["speakers"]),
        "metadata": {
            "time_range": f"{_format_time(chunk_data['start_time'])} - {_format_time(chunk_data['end_time'])}",
            "speaker_count": len(chunk_data["speakers"]),
            "segment_count": len(chunk_data["segments"])
        }
    }


def _format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def merge_chunks_for_display(chunks: List[Dict[str, Any]]) -> str:
    """
    Merge all chunks into single formatted transcript for display.
    
    Returns:
        Full transcript with timestamps and speakers
    """
    return '\n\n'.join([chunk['text'] for chunk in chunks])
