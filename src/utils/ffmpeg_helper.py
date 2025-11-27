"""FFmpeg Helper - Auto-detect and configure ffmpeg path."""

import os
import sys
from pathlib import Path


def setup_ffmpeg_path():
    """
    Automatically setup ffmpeg PATH.
    Checks multiple locations and adds to PATH if found.
    """
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    
    # Possible ffmpeg locations
    possible_paths = [
        # Local project folder
        project_root / "ffmpeg-8.0.1-essentials_build" / "bin",
        project_root / "ffmpeg" / "bin",
        
        # Common Windows locations
        Path("C:/ffmpeg/bin"),
        Path("C:/Program Files/ffmpeg/bin"),
        
        # Check if already in PATH
        None  # Will check system PATH
    ]
    
    # Check each location
    for path in possible_paths:
        if path is None:
            # Check if ffmpeg already in PATH
            import shutil
            if shutil.which("ffmpeg"):
                print("✅ ffmpeg found in system PATH")
                return True
            continue
        
        if path.exists():
            ffmpeg_exe = path / "ffmpeg.exe"
            if ffmpeg_exe.exists():
                # Add to PATH for current process
                path_str = str(path.absolute())
                if path_str not in os.environ["PATH"]:
                    os.environ["PATH"] = f"{path_str};{os.environ['PATH']}"
                    print(f"✅ ffmpeg configured: {path_str}")
                return True
    
    print("⚠️  ffmpeg not found - recording features may not work")
    print("💡 Run: python -m pip install ffmpeg-python")
    print("   Or download from: https://ffmpeg.org/download.html")
    return False


def get_ffmpeg_path():
    """Get ffmpeg executable path."""
    import shutil
    
    # Try to find ffmpeg
    ffmpeg = shutil.which("ffmpeg")
    
    if ffmpeg:
        return ffmpeg
    
    # Try local project folder
    project_root = Path(__file__).parent.parent.parent
    local_ffmpeg = project_root / "ffmpeg-8.0.1-essentials_build" / "bin" / "ffmpeg.exe"
    
    if local_ffmpeg.exists():
        return str(local_ffmpeg)
    
    return None


def check_ffmpeg():
    """Check if ffmpeg is available and working."""
    import subprocess
    
    ffmpeg_path = get_ffmpeg_path()
    
    if not ffmpeg_path:
        return False, "ffmpeg not found"
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, version_line
        else:
            return False, "ffmpeg not working"
            
    except Exception as e:
        return False, str(e)


# Auto-setup when module is imported
if __name__ != "__main__":
    setup_ffmpeg_path()
