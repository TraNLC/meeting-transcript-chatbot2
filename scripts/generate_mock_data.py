import json
import os
import shutil
from pathlib import Path
import datetime
import subprocess

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RECORDINGS_DIR = DATA_DIR / "recordings"
UPLOADS_DIR = DATA_DIR / "uploads"
METADATA_FILE = RECORDINGS_DIR / "metadata.json"

# Audio Gen (using ffmpeg if available, else simple file copy/write)
# Try to find ffmpeg
FFMPEG_PATH = "ffmpeg"
POSSIBLE_PATHS = [
    BASE_DIR / "ffmpeg-8.0.1-essentials_build" / "bin" / "ffmpeg.exe",
    Path("ffmpeg")
]
for p in POSSIBLE_PATHS:
    if os.path.exists(str(p)) or shutil.which(str(p)):
        FFMPEG_PATH = str(p)
        break

def generate_silence(filename, duration=5):
    """Generate silent audio using ffmpeg"""
    try:
        cmd = [FFMPEG_PATH, "-y", "-f", "lavfi", "-i", f"anullsrc=r=16000:cl=mono", "-t", str(duration), str(filename)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Generated audio: {filename}")
    except Exception as e:
        print(f"Failed to generate audio {filename} with ffmpeg: {e}")
        # Fallback: create dummy file
        with open(filename, 'wb') as f:
            f.write(b'\x00' * 1024 * 100) # 100KB junk

def create_mock_data():
    print("🚀 Generating Mock Data...")
    
    # Create Dirs
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Metadata
    metadata = {
        "recordings": [
            {
                "id": "rec_001",
                "title": "Project Kickoff",
                "timestamp": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
                "duration": "00:05:00",
                "filename": "rec_001.webm",
                "category": "recording",
                "transcript": "[Guest-1] Hello everyone.\n[Guest-2] Hi there!"
            },
            {
                "id": "rec_abnormal_empty",
                "title": "Empty Recording",
                "timestamp": datetime.datetime.now().isoformat(),
                "duration": "00:00:00",
                "filename": "empty.webm",
                "category": "recording",
                "transcript": ""
            }
        ]
    }
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print("✅ Created metadata.json")

    # 2. Audio Files
    generate_silence(RECORDINGS_DIR / "rec_001.webm", duration=5)
    
    # Abnormal: Empty file
    (RECORDINGS_DIR / "empty.webm").touch()
    
    # Abnormal: Huge file (dummy)
    with open(RECORDINGS_DIR / "huge_file.webm", 'wb') as f:
        f.seek(1024 * 1024 * 50) # 50MB sparse
        f.write(b'0')
    
    # Abnormal: Corrupt header
    with open(RECORDINGS_DIR / "corrupt.webm", 'wb') as f:
        f.write(b'RIFF....')

    print("✅ Created mock audio files (Standard, Empty, Huge, Corrupt)")
    
    # 3. Uploads
    with open(UPLOADS_DIR / "sample_upload.txt", 'w', encoding='utf-8') as f:
        f.write("Sample meeting transcript text file.")
        
    print("✅ Done!")

if __name__ == '__main__':
    create_mock_data()
