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
    
    try:
        from transformers import pipeline
        import torch
        import librosa
        
        yield "🔄 Đang khởi tạo HuggingFace Whisper..."
        
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
        
        # Load pipeline
        yield "📥 Đang tải Whisper model từ HuggingFace..."
        
        # Use openai/whisper-medium model (high accuracy)
        # Medium model: 769M params - best balance between accuracy and speed
        pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-medium",
            device=device,
            chunk_length_s=30,  # Process in 30s chunks for better accuracy
            return_timestamps=False
        )
        
        yield f"🎤 Đang transcribe audio (ngôn ngữ: {language})..."
        
        # Transcribe with progress
        import time
        start_time = time.time()
        
        # Show progress updates during transcription
        yield f"⏳ Đang xử lý... (0%)"
        
        result = pipe(
            audio_file,
            generate_kwargs={
                "language": language,
                "task": "transcribe"
            }
        )
        
        elapsed_time = time.time() - start_time
        
        # Calculate actual speed
        if duration_sec > 0:
            speed_factor = duration_sec / elapsed_time
            yield f"✅ Hoàn thành! Tốc độ: {speed_factor:.1f}x realtime ({elapsed_time:.1f}s cho {duration_min:.1f} phút audio)"
        
        transcript = result["text"].strip()
        
        # Get timestamp
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        yield f"""📝 **Transcript ({language}):** {now}

{transcript}

✅ Hoàn thành trong {elapsed_time:.1f} giây! Sử dụng HuggingFace Whisper (Medium model)
"""
            
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
