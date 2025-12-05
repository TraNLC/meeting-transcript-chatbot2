"""Backup and restore utilities for data management.

Provides automatic backup, restore, and cleanup functionality.
"""

import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import zipfile
from .logger import get_logger

logger = get_logger(__name__)


class BackupManager:
    """Manage backups for application data."""
    
    def __init__(self, backup_dir: str = "backups"):
        """Initialize backup manager.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        logger.info(f"BackupManager initialized: {self.backup_dir}")
    
    def create_backup(self, name: str = None, include_recordings: bool = False) -> Path:
        """Create backup of all data.
        
        Args:
            name: Backup name (auto-generated if None)
            include_recordings: Whether to include audio recordings
            
        Returns:
            Path to backup file
        """
        if name is None:
            name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_file = self.backup_dir / f"{name}.zip"
        
        logger.info(f"Creating backup: {backup_file}")
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup history
                history_dir = Path("data/history")
                if history_dir.exists():
                    for file in history_dir.glob("*.json"):
                        zipf.write(file, f"history/{file.name}")
                    logger.debug(f"Backed up {len(list(history_dir.glob('*.json')))} history files")
                
                # Backup checklists
                checklist_dir = Path("data/checklists")
                if checklist_dir.exists():
                    for file in checklist_dir.glob("*.json"):
                        zipf.write(file, f"checklists/{file.name}")
                    logger.debug(f"Backed up {len(list(checklist_dir.glob('*.json')))} checklist files")
                
                # Backup ChromaDB
                chroma_dir = Path("data/chroma_db")
                if chroma_dir.exists():
                    for file in chroma_dir.rglob("*"):
                        if file.is_file():
                            rel_path = file.relative_to("data")
                            zipf.write(file, str(rel_path))
                    logger.debug("Backed up ChromaDB")
                
                # Backup recordings metadata
                recordings_meta = Path("data/recordings/metadata.json")
                if recordings_meta.exists():
                    zipf.write(recordings_meta, "recordings/metadata.json")
                    logger.debug("Backed up recordings metadata")
                
                # Optionally backup audio files
                if include_recordings:
                    recordings_dir = Path("data/recordings")
                    if recordings_dir.exists():
                        for file in recordings_dir.glob("*.wav"):
                            zipf.write(file, f"recordings/{file.name}")
                        logger.debug(f"Backed up {len(list(recordings_dir.glob('*.wav')))} audio files")
                
                # Add backup metadata
                metadata = {
                    "created_at": datetime.now().isoformat(),
                    "include_recordings": include_recordings,
                    "version": "1.0"
                }
                zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
            
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            logger.info(f"Backup created successfully: {backup_file} ({size_mb:.2f} MB)")
            return backup_file
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}", exc_info=True)
            if backup_file.exists():
                backup_file.unlink()
            raise
    
    def restore_backup(self, backup_file: Path, overwrite: bool = False) -> bool:
        """Restore from backup file.
        
        Args:
            backup_file: Path to backup file
            overwrite: Whether to overwrite existing data
            
        Returns:
            True if successful
        """
        if not backup_file.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return False
        
        logger.info(f"Restoring backup: {backup_file}")
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                # Read metadata
                metadata_str = zipf.read("backup_metadata.json").decode()
                metadata = json.loads(metadata_str)
                logger.info(f"Backup created at: {metadata['created_at']}")
                
                # Extract all files
                extract_dir = Path("data")
                
                if not overwrite:
                    # Create restore directory with timestamp
                    restore_dir = Path(f"data_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    zipf.extractall(restore_dir)
                    logger.info(f"Backup extracted to: {restore_dir}")
                else:
                    zipf.extractall(extract_dir)
                    logger.info(f"Backup restored to: {extract_dir}")
            
            logger.info("Backup restored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}", exc_info=True)
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups.
        
        Returns:
            List of backup info dictionaries
        """
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    metadata_str = zipf.read("backup_metadata.json").decode()
                    metadata = json.loads(metadata_str)
                    
                    size_mb = backup_file.stat().st_size / (1024 * 1024)
                    
                    backups.append({
                        "name": backup_file.stem,
                        "file": str(backup_file),
                        "created_at": metadata.get("created_at"),
                        "size_mb": round(size_mb, 2),
                        "include_recordings": metadata.get("include_recordings", False)
                    })
            except Exception as e:
                logger.warning(f"Failed to read backup metadata: {backup_file} - {e}")
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        return backups
    
    def delete_backup(self, backup_name: str) -> bool:
        """Delete a backup file.
        
        Args:
            backup_name: Name of backup to delete
            
        Returns:
            True if successful
        """
        backup_file = self.backup_dir / f"{backup_name}.zip"
        
        if not backup_file.exists():
            logger.warning(f"Backup not found: {backup_name}")
            return False
        
        try:
            backup_file.unlink()
            logger.info(f"Deleted backup: {backup_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}", exc_info=True)
            return False
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 10):
        """Clean up old backups.
        
        Args:
            keep_days: Keep backups newer than this many days
            keep_count: Keep at least this many recent backups
        """
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            logger.info(f"Only {len(backups)} backups, no cleanup needed")
            return
        
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        deleted_count = 0
        
        # Keep the most recent backups
        for backup in backups[keep_count:]:
            created_at = datetime.fromisoformat(backup["created_at"])
            
            if created_at < cutoff_date:
                if self.delete_backup(backup["name"]):
                    deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old backups")


class DataCleanup:
    """Clean up old data to save space."""
    
    @staticmethod
    def cleanup_old_recordings(days: int = 90) -> int:
        """Delete recordings older than specified days.
        
        Args:
            days: Delete recordings older than this
            
        Returns:
            Number of recordings deleted
        """
        recordings_dir = Path("data/recordings")
        if not recordings_dir.exists():
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for audio_file in recordings_dir.glob("*.wav"):
            # Check file modification time
            mtime = datetime.fromtimestamp(audio_file.stat().st_mtime)
            
            if mtime < cutoff_date:
                try:
                    audio_file.unlink()
                    deleted_count += 1
                    logger.debug(f"Deleted old recording: {audio_file.name}")
                except Exception as e:
                    logger.error(f"Failed to delete {audio_file}: {e}")
        
        logger.info(f"Cleaned up {deleted_count} old recordings (>{days} days)")
        return deleted_count
    
    @staticmethod
    def cleanup_old_history(days: int = 180) -> int:
        """Delete analysis history older than specified days.
        
        Args:
            days: Delete history older than this
            
        Returns:
            Number of history files deleted
        """
        history_dir = Path("data/history")
        if not history_dir.exists():
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for history_file in history_dir.glob("*.json"):
            try:
                # Read timestamp from file
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    timestamp_str = data.get("timestamp", "")
                    
                    if timestamp_str:
                        # Parse timestamp (format: YYYY-MM-DD HH:MM:SS)
                        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                        
                        if timestamp < cutoff_date:
                            history_file.unlink()
                            deleted_count += 1
                            logger.debug(f"Deleted old history: {history_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {history_file}: {e}")
        
        logger.info(f"Cleaned up {deleted_count} old history files (>{days} days)")
        return deleted_count
    
    @staticmethod
    def get_storage_stats() -> Dict:
        """Get storage statistics.
        
        Returns:
            Dictionary with storage stats
        """
        stats = {
            "recordings": {"count": 0, "size_mb": 0},
            "history": {"count": 0, "size_mb": 0},
            "chroma_db": {"size_mb": 0},
            "backups": {"count": 0, "size_mb": 0},
            "total_mb": 0
        }
        
        # Recordings
        recordings_dir = Path("data/recordings")
        if recordings_dir.exists():
            files = list(recordings_dir.glob("*.wav"))
            stats["recordings"]["count"] = len(files)
            stats["recordings"]["size_mb"] = sum(f.stat().st_size for f in files) / (1024 * 1024)
        
        # History
        history_dir = Path("data/history")
        if history_dir.exists():
            files = list(history_dir.glob("*.json"))
            stats["history"]["count"] = len(files)
            stats["history"]["size_mb"] = sum(f.stat().st_size for f in files) / (1024 * 1024)
        
        # ChromaDB
        chroma_dir = Path("data/chroma_db")
        if chroma_dir.exists():
            size = sum(f.stat().st_size for f in chroma_dir.rglob("*") if f.is_file())
            stats["chroma_db"]["size_mb"] = size / (1024 * 1024)
        
        # Backups
        backup_dir = Path("backups")
        if backup_dir.exists():
            files = list(backup_dir.glob("*.zip"))
            stats["backups"]["count"] = len(files)
            stats["backups"]["size_mb"] = sum(f.stat().st_size for f in files) / (1024 * 1024)
        
        # Total
        stats["total_mb"] = (
            stats["recordings"]["size_mb"] +
            stats["history"]["size_mb"] +
            stats["chroma_db"]["size_mb"] +
            stats["backups"]["size_mb"]
        )
        
        return stats


# Global backup manager
_backup_manager = None


def get_backup_manager() -> BackupManager:
    """Get global backup manager instance."""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager()
    return _backup_manager
