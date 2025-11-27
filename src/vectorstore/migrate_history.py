"""Migration script to convert existing history to ChromaDB."""

import os
import json
from datetime import datetime
from chroma_manager import ChromaManager


def migrate_existing_history():
    """Migrate existing meeting history to ChromaDB."""
    
    history_dir = "data/history"
    if not os.path.exists(history_dir):
        print("No history directory found. Nothing to migrate.")
        return
    
    # Initialize ChromaDB manager
    chroma = ChromaManager()
    
    # Get existing meetings count
    existing_stats = chroma.get_statistics()
    print(f"Current ChromaDB stats: {existing_stats}")
    
    # Scan history directory
    migrated = 0
    skipped = 0
    errors = 0
    
    for filename in os.listdir(history_dir):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(history_dir, filename)
        meeting_id = filename.replace('.json', '')
        
        try:
            # Check if already migrated
            if chroma.get_meeting(meeting_id):
                print(f"Skipping {meeting_id} - already in ChromaDB")
                skipped += 1
                continue
            
            # Load history file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            transcript = data.get('transcript', '')
            if not transcript:
                print(f"Skipping {meeting_id} - no transcript")
                skipped += 1
                continue
            
            # Extract analysis
            analysis = data.get('analysis', {})
            meeting_type = data.get('meeting_type', 'meeting')
            language = data.get('language', 'en')
            
            # Store in ChromaDB
            success = chroma.store_meeting(
                meeting_id=meeting_id,
                transcript=transcript,
                analysis=analysis,
                meeting_type=meeting_type,
                language=language
            )
            
            if success:
                print(f"✓ Migrated {meeting_id}")
                migrated += 1
            else:
                print(f"✗ Failed to migrate {meeting_id}")
                errors += 1
                
        except Exception as e:
            print(f"✗ Error migrating {meeting_id}: {e}")
            errors += 1
    
    # Print summary
    print("\n" + "="*50)
    print("MIGRATION SUMMARY")
    print("="*50)
    print(f"Migrated: {migrated}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Total processed: {migrated + skipped + errors}")
    
    # Show new stats
    new_stats = chroma.get_statistics()
    print(f"\nNew ChromaDB stats: {new_stats}")


if __name__ == "__main__":
    print("Starting migration of existing history to ChromaDB...")
    print("="*50)
    migrate_existing_history()
