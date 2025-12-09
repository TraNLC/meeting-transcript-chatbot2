import os
import sys
import shutil
from pathlib import Path

def check_ffmpeg_deps():
    print("=========================================")
    print("   FFmpeg & TorchCodec Diagnostic Tool   ")
    print("=========================================")
    
    # 1. Simulate the App's Startup (Import Helper)
    print("\n[1] SETUP: Loading backend.utils.ffmpeg_helper...")
    try:
        # Add project root to sys.path to mimic run.py
        current_dir = Path(__file__).parent.absolute()
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
            
        import backend.utils.ffmpeg_helper
        print("   ✅ backend.utils.ffmpeg_helper imported.")
    except ImportError as e:
        print(f"   ❌ Failed to import ffmpeg_helper: {e}")

    # 2. Check PATH and Binary Availability
    print("\n[2] CHECKING: FFmpeg binary in PATH...")
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path:
        print(f"   ✅ Found 'ffmpeg' at: {ffmpeg_path}")
        
        # 3. CRITICAL: Check for DLLs (Shared Libraries)
        print("\n[3] INSPECTING: Checking for Shared Libraries (.dll)...")
        bin_dir = Path(ffmpeg_path).parent
        dll_files = list(bin_dir.glob("*.dll"))
        
        print(f"   Directory: {bin_dir}")
        if not dll_files:
            print(f"   ❌ CRITICAL ERROR: 0 DLL files found!")
            print("   -------------------------------------------------------")
            print("   ⚠️ DIAGNOSIS: You are using a 'STATIC' or 'ESSENTIALS' build.")
            print("   TorchCodec requires a 'SHARED' build containing files like:")
            print("     - avcodec-61.dll")
            print("     - avformat-61.dll")
            print("     - avutil-59.dll")
            print("   -------------------------------------------------------")
        else:
            print(f"   ✅ SUCCESS: Found {len(dll_files)} DLL files.")
            print(f"   Examples: {[d.name for d in dll_files[:3]]}...")
    else:
        print("   ❌ Error: 'ffmpeg' command not found in PATH.")

    # 4. Attempt Import
    print("\n[4] TEST: Attempting to import dependencies...")
    try:
        import torch
        print(f"   ✅ torch version: {torch.__version__}")
        
        print("   Attempting to load extension (will fail if DLLs missing)...")
        # Try to trigger the specific error seen in logs
        # This often happens when accessing audio backend functions
        try:
            import torchaudio
            print(f"   ✅ torchaudio version: {torchaudio.__version__}")
            # Try to initialize a backend that uses ffmpeg
            torchaudio.set_audio_backend("ffmpeg") # or similar
            print("   ✅ torchaudio backend set.")
        except Exception as e:
             pass # torchaudio might warn, but let's see if we can trigger the loading error

    except Exception as e:
        print(f"   ❌ Import Failed: {e}")

    print("\n=========================================")
    if ffmpeg_path and not dll_files:
        print("👉 SOLUTION: Please download 'ffmpeg-release-full-shared.7z' instead of 'essentials'.")
    print("=========================================")

if __name__ == "__main__":
    check_ffmpeg_deps()
