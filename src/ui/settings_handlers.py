"""Handler functions for Settings tab."""

from pathlib import Path
from typing import Tuple, List
import pandas as pd

from src.utils.backup import get_backup_manager, DataCleanup
from src.utils.cache import get_all_cache_stats, clear_all_caches, get_cache
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_backup_handler(name: str, include_recordings: bool) -> str:
    """Create backup.
    
    Args:
        name: Backup name
        include_recordings: Include audio files
        
    Returns:
        Status message
    """
    try:
        manager = get_backup_manager()
        backup_file = manager.create_backup(
            name=name if name.strip() else None,
            include_recordings=include_recordings
        )
        
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        return f"✅ Backup created successfully!\n\nFile: {backup_file.name}\nSize: {size_mb:.2f} MB"
        
    except Exception as e:
        logger.error(f"Failed to create backup: {e}", exc_info=True)
        return f"❌ Error creating backup: {str(e)}"


def list_backups_handler() -> Tuple[pd.DataFrame, List[str]]:
    """List all backups.
    
    Returns:
        Tuple of (dataframe, dropdown choices)
    """
    try:
        manager = get_backup_manager()
        backups = manager.list_backups()
        
        if not backups:
            df = pd.DataFrame(columns=["Tên", "Ngày tạo", "Kích thước (MB)", "Có ghi âm"])
            return df, []
        
        # Create dataframe
        df = pd.DataFrame([
            {
                "Tên": b["name"],
                "Ngày tạo": b["created_at"][:19],
                "Kích thước (MB)": b["size_mb"],
                "Có ghi âm": "✅" if b["include_recordings"] else "❌"
            }
            for b in backups
        ])
        
        # Create dropdown choices
        choices = [b["name"] for b in backups]
        
        return df, choices
        
    except Exception as e:
        logger.error(f"Failed to list backups: {e}", exc_info=True)
        df = pd.DataFrame(columns=["Tên", "Ngày tạo", "Kích thước (MB)", "Có ghi âm"])
        return df, []


def restore_backup_handler(backup_name: str) -> str:
    """Restore from backup.
    
    Args:
        backup_name: Name of backup to restore
        
    Returns:
        Status message
    """
    if not backup_name:
        return "⚠️ Please select a backup to restore"
    
    try:
        manager = get_backup_manager()
        backup_file = Path("backups") / f"{backup_name}.zip"
        
        success = manager.restore_backup(backup_file, overwrite=False)
        
        if success:
            return f"✅ Backup restored successfully!\n\nData extracted to: data_restore_*\nReview before overwriting current data."
        else:
            return "❌ Failed to restore backup"
            
    except Exception as e:
        logger.error(f"Failed to restore backup: {e}", exc_info=True)
        return f"❌ Error restoring backup: {str(e)}"


def delete_backup_handler(backup_name: str) -> Tuple[str, pd.DataFrame, List[str]]:
    """Delete backup.
    
    Args:
        backup_name: Name of backup to delete
        
    Returns:
        Tuple of (status, updated dataframe, updated choices)
    """
    if not backup_name:
        df, choices = list_backups_handler()
        return "⚠️ Please select a backup to delete", df, choices
    
    try:
        manager = get_backup_manager()
        success = manager.delete_backup(backup_name)
        
        # Refresh list
        df, choices = list_backups_handler()
        
        if success:
            return f"✅ Deleted backup: {backup_name}", df, choices
        else:
            return f"❌ Failed to delete backup: {backup_name}", df, choices
            
    except Exception as e:
        logger.error(f"Failed to delete backup: {e}", exc_info=True)
        df, choices = list_backups_handler()
        return f"❌ Error: {str(e)}", df, choices


def get_storage_stats_handler() -> str:
    """Get storage statistics.
    
    Returns:
        Formatted storage stats
    """
    try:
        stats = DataCleanup.get_storage_stats()
        
        output = []
        output.append("## 📊 Thống Kê Dung Lượng\n")
        output.append(f"**Tổng:** {stats['total_mb']:.2f} MB\n")
        output.append("---\n")
        output.append(f"**🎙️ Ghi âm:** {stats['recordings']['count']} files ({stats['recordings']['size_mb']:.2f} MB)")
        output.append(f"**📊 Lịch sử:** {stats['history']['count']} files ({stats['history']['size_mb']:.2f} MB)")
        output.append(f"**🔍 ChromaDB:** {stats['chroma_db']['size_mb']:.2f} MB")
        output.append(f"**💾 Backups:** {stats['backups']['count']} files ({stats['backups']['size_mb']:.2f} MB)")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Failed to get storage stats: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def cleanup_recordings_handler(days: int) -> str:
    """Clean up old recordings.
    
    Args:
        days: Delete recordings older than this
        
    Returns:
        Status message
    """
    try:
        count = DataCleanup.cleanup_old_recordings(days)
        return f"✅ Deleted {count} recordings older than {days} days"
        
    except Exception as e:
        logger.error(f"Failed to cleanup recordings: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def cleanup_history_handler(days: int) -> str:
    """Clean up old history.
    
    Args:
        days: Delete history older than this
        
    Returns:
        Status message
    """
    try:
        count = DataCleanup.cleanup_old_history(days)
        return f"✅ Deleted {count} history files older than {days} days"
        
    except Exception as e:
        logger.error(f"Failed to cleanup history: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def get_cache_stats_handler() -> str:
    """Get cache statistics.
    
    Returns:
        Formatted cache stats
    """
    try:
        stats = get_all_cache_stats()
        
        if not stats:
            return "## ⚡ Cache Statistics\n\nNo caches active"
        
        output = []
        output.append("## ⚡ Cache Statistics\n")
        
        for name, cache_stats in stats.items():
            output.append(f"### {name}")
            output.append(f"- Size: {cache_stats['size']}/{cache_stats['max_size']}")
            output.append(f"- Usage: {cache_stats['usage_percent']:.1f}%")
            output.append(f"- TTL: {cache_stats['ttl']}s\n")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def clear_llm_cache_handler() -> str:
    """Clear LLM cache.
    
    Returns:
        Status message
    """
    try:
        cache = get_cache('llm_responses')
        cache.clear()
        return "✅ LLM cache cleared"
        
    except Exception as e:
        logger.error(f"Failed to clear LLM cache: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def clear_all_cache_handler() -> str:
    """Clear all caches.
    
    Returns:
        Status message
    """
    try:
        clear_all_caches()
        return "✅ All caches cleared"
        
    except Exception as e:
        logger.error(f"Failed to clear caches: {e}", exc_info=True)
        return f"❌ Error: {str(e)}"


def get_logs_handler(lines: int = 100) -> str:
    """Get recent logs.
    
    Args:
        lines: Number of lines to show
        
    Returns:
        Log content
    """
    try:
        from datetime import datetime
        log_file = Path("logs") / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        if not log_file.exists():
            return "No logs found for today"
        
        # Read last N lines
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]
            return "".join(recent_lines)
            
    except Exception as e:
        logger.error(f"Failed to read logs: {e}", exc_info=True)
        return f"❌ Error reading logs: {str(e)}"
