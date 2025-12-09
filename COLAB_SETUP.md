# 🚀 Hướng dẫn Setup Google Colab - Bắt đầu với Upload

## 📋 Bước 1: Chuẩn bị tokens

### 1.1. Lấy ngrok token (MIỄN PHÍ)
1. Truy cập: https://dashboard.ngrok.com/get-started/your-authtoken
2. Đăng ký/Đăng nhập (free account)
3. Copy token (dạng: `2abc...xyz`)
36Za1CVW7J1hu3aDLWCzYsUMvcC_4hrNbzBDoMit9mPsfTyiB

### 1.2. Lấy HuggingFace token (MIỄN PHÍ)
1. Truy cập: https://huggingface.co/settings/tokens
2. Đăng ký/Đăng nhập
3. Tạo token mới (Read access)
4. **QUAN TRỌNG**: Accept terms tại:
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0
5. Copy token (dạng: `hf_abc...xyz`)

---

## 🎯 Bước 2: Mở Colab Notebook

### Cách 1: Upload file
1. Truy cập: https://colab.research.google.com/
2. File > Upload notebook
3. Chọn `colab_whisperx_server.ipynb`

### Cách 2: Từ GitHub (nhanh hơn)
1. Truy cập: https://colab.research.google.com/
2. GitHub tab
3. Nhập: `TraNLC/meeting-transcript-chatbot2`
4. Chọn `colab_whisperx_server.ipynb`

---

## ⚙️ Bước 3: Cấu hình Colab

### 3.1. Chọn GPU (QUAN TRỌNG!)
1. Runtime > Change runtime type
2. Hardware accelerator: **GPU**
3. GPU type: **T4** (free)
4. Save

### 3.2. Điền tokens
1. Tìm **Cell 2** (Import và Setup)
2. Đợi 2-3 phút (cài đặt packages)

### 4.2. Lấy URL ngrok
Sau khi chạy xong, bạn sẽ thấy output:
```
============================================================
🚀 SERVER ĐANG CHẠY!
============================================================
📡 Public URL: https://1234-5678-90ab-cdef.ngrok-free.app

✅ Copy URL này và dán vào config của Meeting App

📝 Test endpoint:
   GET  https://1234-5678-90ab-cdef.ngrok-free.app/health
   POST https://1234-5678-90ab-cdef.ngrok-free.app/transcribe
============================================================
```

**Copy URL này**: `https://1234-5678-90ab-cdef.ngrok-free.app`

---

## 🧪 Bước 5: Test với Upload Tab

### 5.1. Mở Meeting App
```bash
cd meeting-transcript-chatbot2
python run.py
```

### 5.2. Truy cập Upload page
- URL: http://localhost:5000/upload

### 5.3. Upload file test
1. Kéo thả file audio (MP3, WAV, MP4...)
2. Chọn ngôn ngữ: **Tiếng Việt**
3. Chọn AI Model: **Gemini 2.5 Flash - Miễn phí 🆓**
4. **Dán URL Colab** vào ô "Colab WhisperX URL"
5. Bấm **"Upload và phân tích"**

### 5.4. Đợi kết quả
- Colab sẽ xử lý: 2-5 phút (tùy độ dài file)
- Bạn sẽ thấy:
  - ✅ Transcript với speaker labels
  - ✅ Summary
  - ✅ Key Topics
  - ✅ Action Items
  - ✅ Key Decisions

---

## 🎬 Demo với file mẫu

### File test nhỏ (30 giây)
Tạo file `test_audio.txt` với nội dung:
```
Chào mọi người, hôm nay chúng ta họp về dự án AI Meeting.
Tôi là John, CEO của công ty.
Tôi muốn nghe ý kiến của mọi người về tính năng mới.
```

Hoặc dùng file audio có sẵn trong `data/uploads/`

---

## 🔍 Kiểm tra Colab hoạt động

### Test 1: Health check
Mở browser, truy cập:
```
https://your-ngrok-url.ngrok-free.app/health
```

Kết quả mong đợi:
```json
{
  "status": "healthy",
  "device": "cuda",
  "model": "whisperx-large-v3"
}
```

### Test 2: Upload qua curl
```bash
curl -X POST https://your-ngrok-url.ngrok-free.app/transcribe \
  -F "file=@test_audio.mp3"
```

---

## ⚠️ Lưu ý quan trọng

### 1. Colab timeout
- Free tier: ~12 giờ/ngày
- Nếu không dùng 90 phút → disconnect
- **Giải pháp**: Chỉ mở khi cần, tắt ngay sau khi xong

### 2. ngrok URL thay đổi
- Mỗi lần chạy lại Colab → URL mới
- **Giải pháp**: Copy URL mới và dán lại vào Upload page

### 3. GPU không khả dụng
- Nếu thấy "GPU not available"
- **Giải pháp**: Runtime > Change runtime type > GPU

### 4. HuggingFace token lỗi
- Nếu thấy "401 Unauthorized"
- **Giải pháp**: Accept terms tại pyannote links (xem Bước 1.2)

---

## 🎯 Workflow hoàn chỉnh

```
1. Mở Colab → Run All → Copy URL
2. Mở Meeting App → Upload page
3. Dán URL Colab
4. Upload file audio
5. Đợi 2-5 phút
6. Nhận kết quả
7. Tắt Colab (nếu không dùng nữa)
```

---

## 🆘 Troubleshooting

### Lỗi: "Colab transcription failed"
**Nguyên nhân**: URL sai hoặc Colab đã tắt
**Giải pháp**:
1. Kiểm tra Colab còn chạy không
2. Test health endpoint
3. Copy lại URL mới

### Lỗi: "No module named 'whisperx'"
**Nguyên nhân**: Cell 1 chưa chạy xong
**Giải pháp**: Đợi Cell 1 cài đặt xong (2-3 phút)

### Lỗi: "CUDA out of memory"
**Nguyên nhân**: File quá lớn (>2 giờ)
**Giải pháp**: 
1. Chia nhỏ file
2. Hoặc dùng Colab Pro ($10/tháng)

### Lỗi: "Speaker diarization failed"
**Nguyên nhân**: Chưa accept terms HuggingFace
**Giải pháp**: Accept terms tại pyannote links

### Lỗi: "RuntimeError: operator torchvision::nms does not exist"
**Nguyên nhân**: Xung đột phiên bản Torch giữa WhisperX và Colab.
**Giải pháp**: Thay thế **Cell 2 (Install Dependencies)** bằng code sau:

```python
# Cell 2: Install Dependencies (Fixed)
!pip install whisperx flask pyngrok python-dotenv requests -q
!pip install faster-whisper -q

# Fix Torch Version Mismatch
!pip uninstall torch torchvision torchaudio -y
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
print("✅ Cài đặt hoàn tất!")
```

---

## 💰 Chi phí

| Dịch vụ | Chi phí | Giới hạn |
|---------|---------|----------|
| Google Colab (GPU T4) | **$0** | ~12 giờ/ngày |
| ngrok | **$0** | 1 tunnel |
| HuggingFace | **$0** | Không giới hạn |
| Gemini 1.5 Flash | **$0** | 15 requests/phút |

**Tổng: $0/tháng** 🎉

---

## 📚 Video hướng dẫn

1. **Setup Colab**: https://www.youtube.com/watch?v=inN8seMm7UI
2. **ngrok tutorial**: https://www.youtube.com/watch?v=8FJz3LkVGmI
3. **WhisperX demo**: https://www.youtube.com/watch?v=ABFqbY_rmEk

---

## 🎓 Tips

1. **Bookmark URL Colab**: Để mở nhanh lần sau
2. **Save tokens**: Lưu tokens vào file riêng (không commit lên Git!)
3. **Test với file nhỏ trước**: Đảm bảo mọi thứ hoạt động
4. **Monitor Colab**: Xem logs để debug nếu có lỗi

---

**Chúc bạn thành công! 🚀**

Nếu gặp vấn đề, xem file `ZERO_COST_GUIDE.md` hoặc mở issue trên GitHub.
