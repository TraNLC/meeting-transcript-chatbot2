"""Audio file management and storage."""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json


class AudioManager:
    """Manages audio recordings and metadata."""
    
    def __init__(self, recordings_dir: str = "data/recordings"):
        """Initialize audio manager.
        
        Args:
            recordings_dir: Directory to store recordings
        """
        self.recordings_dir = Path(recordings_dir)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        
        # Metadata file
        self.metadata_file = self.recordings_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"recordings": []}
    
    def _save_metadata(self):
        """Save metadata to file."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def save_recording(
        self,
        audio_file: str,
        duration: Optional[float] = None,
        title: Optional[str] = None,
        notes: Optional[str] = None
    ) -> str:
        """Save recording and metadata.
        
        Args:
            audio_file: Path to audio file
            duration: Recording duration in seconds
            title: Recording title
            notes: Additional notes
            
        Returns:
            Recording ID
        """
        # Generate recording ID
        recording_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Copy file to recordings directory
        source_path = Path(audio_file)
        dest_path = self.recordings_dir / f"{recording_id}.wav"
        
        if source_path.exists():
            import shutil
            shutil.copy2(source_path, dest_path)
        
        # Add metadata
        metadata_entry = {
            "id": recording_id,
            "filename": f"{recording_id}.wav",
            "filepath": str(dest_path),
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "title": title or f"Recording {recording_id}",
            "notes": notes or "",
            "processed": False,
            "transcript_id": None
        }
        
        self.metadata["recordings"].append(metadata_entry)
        self._save_metadata()
        
        return recording_id
    
    def get_recordings(self, processed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get list of recordings.
        
        Args:
            processed: Filter by processed status (None = all)
            
        Returns:
            List of recording metadata
        """
        recordings = self.metadata["recordings"]
        
        if processed is not None:
            recordings = [r for r in recordings if r.get("processed") == processed]
        
        # Sort by timestamp (newest first)
        recordings.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return recordings
    
    def get_recording(self, recording_id: str) -> Optional[Dict[str, Any]]:
        """Get specific recording metadata.
        
        Args:
            recording_id: Recording ID
            
        Returns:
            Recording metadata or None
        """
        for recording in self.metadata["recordings"]:
            if recording["id"] == recording_id:
                return recording
        return None
    
    def mark_processed(self, recording_id: str, transcript_id: Optional[str] = None):
        """Mark recording as processed.
        
        Args:
            recording_id: Recording ID
            transcript_id: Associated transcript ID
        """
        for recording in self.metadata["recordings"]:
            if recording["id"] == recording_id:
                recording["processed"] = True
                recording["transcript_id"] = transcript_id
                recording["processed_at"] = datetime.now().isoformat()
                break
        
        self._save_metadata()
    
    def delete_recording(self, recording_id: str) -> bool:
        """Delete recording and metadata.
        
        Args:
            recording_id: Recording ID
            
        Returns:
            True if successful
        """
        # Find and remove from metadata
        recording = None
        for i, r in enumerate(self.metadata["recordings"]):
            if r["id"] == recording_id:
                recording = self.metadata["recordings"].pop(i)
                break
        
        if not recording:
            return False
        
        # Delete file
        filepath = Path(recording["filepath"])
        if filepath.exists():
            filepath.unlink()
        
        self._save_metadata()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get recording statistics.
        
        Returns:
            Statistics dictionary
        """
        recordings = self.metadata["recordings"]
        
        total = len(recordings)
        processed = sum(1 for r in recordings if r.get("processed"))
        unprocessed = total - processed
        
        total_duration = sum(r.get("duration", 0) for r in recordings if r.get("duration"))
        
        return {
            "total_recordings": total,
            "processed": processed,
            "unprocessed": unprocessed,
            "total_duration_seconds": total_duration,
            "total_duration_minutes": total_duration / 60 if total_duration else 0
        }
    
    def format_duration(self, seconds: Optional[float]) -> str:
        """Format duration as HH:MM:SS.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted string
        """
        if seconds is None:
            return "00:00:00"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
