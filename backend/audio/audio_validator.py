"""Audio quality validation before processing."""

import librosa
import numpy as np
from pathlib import Path
from typing import Tuple


def validate_audio_quality(audio_path: str) -> Tuple[bool, str]:
    """
    Validate audio file quality before transcription.
    
    Checks:
    - Sample rate (>=8kHz)
    - Duration (1s - 2h)
    - Amplitude (not too quiet)
    - Clipping (not distorted)
    - File size (<500MB)
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        (is_valid, message): True if valid, else False with error message
    """
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        duration = len(y) / sr
        
        # 1. Check sample rate
        if sr < 8000:
            return False, f"❌ Sample rate quá thấp ({sr}Hz). Cần ít nhất 8kHz để transcribe chính xác."
        
        # 2. Check duration
        if duration < 1:
            return False, "❌ Audio quá ngắn (<1 giây). Không đủ nội dung để transcribe."
        
        if duration > 7200:  # 2 hours
            duration_min = duration / 60
            return False, f"❌ Audio quá dài ({duration_min:.1f} phút). Vui lòng chia nhỏ file (<2 giờ)."
        
        # 3. Check if audio is too quiet
        max_amplitude = np.max(np.abs(y))
        if max_amplitude < 0.01:
            return False, "❌ Audio quá nhỏ/yếu (max amplitude < 0.01). Tăng volume khi record hoặc dùng audio editor."
        
        # 4. Check for clipping (distortion)
        clipping_samples = np.sum(np.abs(y) > 0.99)
        clipping_rate = clipping_samples / len(y)
        if clipping_rate > 0.01:  # >1% clipped
            return False, f"❌ Audio bị clipping/distortion ({clipping_rate*100:.1f}% samples). Giảm volume khi record."
        
        # 5. Check file size
        file_size_mb = Path(audio_path).stat().st_size / (1024 * 1024)
        if file_size_mb > 500:
            return False, f"❌ File quá lớn ({file_size_mb:.0f}MB). Giới hạn 500MB. Compress hoặc chia nhỏ file."
        
        # All checks passed
        return True, f"✅ Audio quality OK ({duration:.1f}s, {sr}Hz, {file_size_mb:.1f}MB)"
        
    except Exception as e:
        return False, f"❌ Lỗi khi đọc file audio: {str(e)}"


def get_audio_info(audio_path: str) -> dict:
    """
    Get detailed audio information.
    
    Returns:
        dict with duration, sample_rate, channels, file_size_mb
    """
    try:
        y, sr = librosa.load(audio_path, sr=None, mono=False)
        
        # Handle stereo vs mono
        if len(y.shape) > 1:
            channels = y.shape[0]
            duration = y.shape[1] / sr
        else:
            channels = 1
            duration = len(y) / sr
        
        file_size_mb = Path(audio_path).stat().st_size / (1024 * 1024)
        
        return {
            "duration_seconds": duration,
            "duration_formatted": f"{int(duration // 60):02d}:{int(duration % 60):02d}",
            "sample_rate": sr,
            "channels": channels,
            "file_size_mb": round(file_size_mb, 2)
        }
    except Exception as e:
        return {"error": str(e)}
