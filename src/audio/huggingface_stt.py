"""HuggingFace Speech-to-Text using Whisper model.

Uses transformers pipeline for easy integration.
"""

from pathlib import Path
from datetime import datetime


def transcribe_audio_huggingface(audio_file, language="vi"):
    """Transcribe audio using HuggingFace Whisper model.
    
    Args:
        audio_file: Path to audio file
        language: Language code (vi, en, ja, ko, zh)
        
    Yields:
        str: Progress messages and final transcript
    """
    if audio_file is None or audio_file == "":
        yield "🎙️ Sẵn sàng ghi âm. Nhấn microphone icon để bắt đầu..."
        return
    
    # Debug: Log file path
    print(f"[DEBUG] Transcribing file: {audio_file}")
    print(f"[DEBUG] Language: {language}")
    
    try:
        from transformers import pipeline
        import torch
        import librosa
        import shutil
        import tempfile
        
        yield "🔄 Đang khởi tạo HuggingFace Whisper..."
        
        # Create a unique copy of audio file to avoid Gradio cache
        # This ensures each recording is processed fresh
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        unique_audio_path = Path(temp_dir) / f"whisper_input_{timestamp}.wav"
        
        # Copy audio file to unique path
        shutil.copy2(audio_file, unique_audio_path)
        audio_file = str(unique_audio_path)  # Use unique path for processing
        
        print(f"[DEBUG] Using unique file: {audio_file}")
        
        # Check file size and duration
        file_path = Path(audio_file)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        # Get audio duration
        try:
            audio_data, sr = librosa.load(audio_file, sr=None)
            duration_sec = len(audio_data) / sr
            duration_min = duration_sec / 60
            
            yield f"📊 File: {file_size_mb:.1f} MB, Thời lượng: {duration_min:.1f} phút"
            
            # Estimate processing time (rough estimate)
            # Medium model on CPU: ~1x realtime (1 min audio = 1 min processing)
            # On GPU: ~5-10x faster
            device = 0 if torch.cuda.is_available() else -1
            device_name = "GPU (CUDA)" if device == 0 else "CPU"
            
            if device == 0:
                est_time = duration_min / 5  # GPU is ~5x faster
                speed_info = "nhanh 5x"
            else:
                est_time = duration_min * 1.2  # CPU is ~1.2x realtime
                speed_info = "realtime"
            
            # Format time estimate
            if est_time < 1:
                time_str = f"{int(est_time * 60)} giây"
            else:
                time_str = f"{est_time:.1f} phút"
            
            yield f"⚙️  Thiết bị: {device_name} ({speed_info}) | Dự kiến: ~{time_str}"
            
            # Check if file too large with detailed warnings
            if duration_min > 120:
                yield f"🚨 Cảnh báo: File rất dài ({duration_min:.1f} phút = {duration_min/60:.1f} giờ). Khuyến nghị chia nhỏ file!"
            elif duration_min > 60:
                yield f"⚠️  Cảnh báo: File dài ({duration_min:.1f} phút). Có thể mất {time_str} để xử lý..."
            
            if file_size_mb > 200:
                yield f"🚨 Cảnh báo: File rất lớn ({file_size_mb:.1f} MB). Cần ít nhất 4GB RAM!"
            elif file_size_mb > 100:
                yield f"⚠️  Cảnh báo: File lớn ({file_size_mb:.1f} MB). Đảm bảo đủ RAM (khuyến nghị 2GB+)..."
                
        except Exception as e:
            yield f"⚠️  Không đọc được thông tin file: {e}"
        
        # Load pipeline (force reload to avoid cache)
        yield "📥 Đang tải Whisper model từ HuggingFace..."
        
        # Use openai/whisper-base model for faster processing
        # Base model: 74M params - faster and good enough for most cases
        # For long audio (>30s), we need return_timestamps=True
        import gc
        gc.collect()  # Clear memory before loading
        
        # Use small model for better accuracy (still fast enough)
        # base: 74M params, small: 244M params (3x larger, more accurate)
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small",  # Better accuracy than base
            device=device,
            return_timestamps=True,  # Required for long-form audio
            torch_dtype=torch.float32  # Ensure consistent dtype
        )
        
        yield f"🎤 Đang transcribe audio (ngôn ngữ: {language})..."
        
        # Transcribe with progress
        import time
        import hashlib
        start_time = time.time()
        
        # Calculate file hash to ensure unique processing
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()
            file_hash = hashlib.md5(audio_bytes).hexdigest()[:8]
            file_size_bytes = len(audio_bytes)
        
        yield f"🔍 Processing audio (ID: {file_hash}, Size: {file_size_bytes} bytes)..."
        
        # Check if this is a known cached file
        known_hashes = {
            "80d4ec5a": "Ghiền Mì Gõ Đẽ sample",  # Known sample file
        }
        
        if file_hash in known_hashes:
            yield f"⚠️  WARNING: Đây có thể là file mẫu cached: {known_hashes[file_hash]}"
            yield f"⚠️  Hãy thử: 1) Clear browser cache, 2) Refresh page, 3) Record lại"
        
        result = pipe(
            audio_file,
            generate_kwargs={
                "language": language,
                "task": "transcribe",
                "temperature": 0.0,  # More deterministic, reduce hallucination
                "no_repeat_ngram_size": 3  # Prevent repetition
            }
        )
        
        elapsed_time = time.time() - start_time
        
        # Extract text from result (handle both formats)
        if isinstance(result, dict):
            if "text" in result:
                transcript = result["text"].strip()
            elif "chunks" in result:
                # Combine chunks if timestamps are returned
                transcript = " ".join([chunk["text"] for chunk in result["chunks"]]).strip()
            else:
                transcript = str(result).strip()
        else:
            transcript = str(result).strip()
        
        # Detect potential hallucination (very short or repetitive text)
        if len(transcript) < 10:
            yield f"⚠️  Warning: Transcript quá ngắn ({len(transcript)} chars). Audio có thể không rõ hoặc quá ngắn."
        
        # Check for repetition (hallucination indicator)
        words = transcript.split()
        if len(words) > 5:
            unique_words = len(set(words))
            repetition_ratio = unique_words / len(words)
            if repetition_ratio < 0.3:  # Less than 30% unique words
                yield f"⚠️  Warning: Phát hiện lặp từ nhiều (có thể hallucination). Thử record lại với audio rõ hơn."
        
        # Get timestamp
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Calculate speed if duration available
        speed_info = ""
        try:
            if duration_sec > 0:
                speed_factor = duration_sec / elapsed_time
                speed_info = f" | Tốc độ: {speed_factor:.1f}x realtime"
        except:
            pass
        
        yield f"""📝 **Transcript ({language}):** {now}

{transcript}

✅ Hoàn thành trong {elapsed_time:.1f}s{speed_info}
"""
        
        # Cleanup unique temp file
        try:
            if unique_audio_path.exists():
                unique_audio_path.unlink()
                print(f"[DEBUG] Cleaned up temp file: {unique_audio_path}")
        except:
            pass
            
    except ImportError as e:
        yield f"""❌ Lỗi: Chưa cài đặt thư viện cần thiết

💡 **Cài đặt HuggingFace Transformers:**

```bash
pip install transformers torch torchaudio
```

**Với GPU support (khuyến nghị):**
```bash
pip install transformers torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Ưu điểm:**
- ✅ Miễn phí, không cần API key
- ✅ Chạy offline (local)
- ✅ Hỗ trợ 50+ ngôn ngữ
- ✅ Dễ cài đặt và sử dụng

**Lỗi chi tiết:** {str(e)}
"""
    except Exception as e:
        yield f"""❌ Lỗi khi transcribe: {str(e)}

💡 **Kiểm tra:**
- File audio có hợp lệ không?
- Đã cài đặt đầy đủ thư viện chưa?
- Có đủ RAM không? (cần ~2GB cho base model)

**Thử lại hoặc liên hệ support.**
"""


def transcribe_audio_simple(audio_file, language="vi"):
    """Simple non-generator version for testing.
    
    Args:
        audio_file: Path to audio file
        language: Language code
        
    Returns:
        str: Transcript text
    """
    if audio_file is None or audio_file == "":
        return "🎙️ Chưa có audio để transcribe"
    
    try:
        from transformers import pipeline
        import torch
        
        device = 0 if torch.cuda.is_available() else -1
        
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
            device=device
        )
        
        result = pipe(
            audio_file,
            generate_kwargs={
                "language": language,
                "task": "transcribe"
            }
        )
        
        transcript = result["text"].strip()
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        return f"""📝 **Transcript ({language}):** {now}

{transcript}
"""
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"
