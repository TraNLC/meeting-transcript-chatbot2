# 🚀 Hướng dẫn sử dụng mô hình ZERO COST

## 📋 Tổng quan

Mô hình này cho phép bạn ghi âm và phân tích cuộc họp **HOÀN TOÀN MIỄN PHÍ** bằng cách kết hợp:

- **Google Colab** (GPU miễn phí) - WhisperX transcription
- **Gemini 1.5 Flash** (Free tier) - AI summary
- **Web Speech API** (Browser) - Live preview

---

## 🎯 Quy trình hoạt động

### Giai đoạn 1: TRONG CUỘC HỌP (The "Effect")
- ✅ **Web Speech API** hiển thị text real-time trên màn hình
- ✅ **MediaRecorder** ghi âm chất lượng cao (client-side)
- 🎨 Mục đích: Tạo hiệu ứng "high-tech", không cần chính xác 100%

### Giai đoạn 2: SAU CUỘC HỌP (The "Brain")
- ✅ Upload file ghi âm lên **Colab WhisperX** (GPU miễn phí)
- ✅ Nhận transcript chính xác + phân biệt người nói
- ✅ Gửi transcript sang **Gemini 1.5 Flash** (miễn phí)
- ✅ Nhận kết quả: Summary, Action Items, Key Decisions

---

## 🛠️ Setup (Chỉ 5 phút)

### Bước 1: Chuẩn bị Colab Notebook

1. Mở file `colab_whisperx_server.ipynb` trong Google Colab
2. Chọn **Runtime > Change runtime type > GPU (T4)**
3. Lấy **ngrok token** miễn phí tại: https://dashboard.ngrok.com/get-started/your-authtoken
4. Lấy **HuggingFace token** tại: https://huggingface.co/settings/tokens (cần cho diarization)
5. Sửa Cell 2:
   ```python
   NGROK_AUTH_TOKEN = "your_token_here"
   HF_TOKEN = "your_hf_token_here"
   ```
6. Chạy **Runtime > Run all**
7. Copy URL ngrok hiển thị (VD: `https://abcd-1234.ngrok-free.app`)

### Bước 2: Cấu hình Gemini API

1. Lấy API key miễn phí tại: https://aistudio.google.com/app/apikey
2. Thêm vào file `.env`:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   ```

---

## 🎬 Cách sử dụng

### A. Live Meeting (Ghi âm trực tiếp)

#### Trước khi họp (2 phút)

1. Mở Colab notebook → Run All
2. Copy URL ngrok
3. Vào trang Live Meeting: http://localhost:5000/recording/browser
4. Dán URL ngrok vào ô "Colab WhisperX URL"

### Trong cuộc họp

1. Nhập tiêu đề cuộc họp
2. Chọn ngôn ngữ
3. Bấm **"Bắt đầu họp"**
4. Cho phép truy cập microphone
5. **Chọn người nói hiện tại** từ dropdown (Speaker 1, 2, 3...)
6. Xem text hiển thị real-time với màu sắc riêng cho mỗi người
7. **Keyboard shortcuts**: Ctrl+1, Ctrl+2... để chuyển speaker nhanh

### Kết thúc cuộc họp

1. Bấm **"Dừng ghi âm"**
2. Đợi 2-5 phút xử lý:
   - File audio → Colab WhisperX (transcribe)
   - pyannote.audio → **Phân biệt người nói TỰ ĐỘNG** (85-95% accuracy)
   - Transcript → Gemini (summary + analysis)
3. Nhận kết quả:
   - 📝 Executive Summary
   - 🎯 Key Topics
   - ✅ Action Items
   - � Key Dcecisions
   - � Puarticipants (tự động phát hiện)
   - 💬 Full Transcript (với tên người nói TỰ ĐỘNG)

#### Sau khi họp

1. Tắt Colab: **Runtime > Disconnect and delete runtime**
2. Export kết quả (TXT, DOCX)
3. Xem lại trong History

---

### B. Upload (File có sẵn)

#### Trước khi upload (2 phút)

1. Mở Colab notebook → Run All (giống Live Meeting)
2. Copy URL ngrok

#### Upload và xử lý

1. Vào trang Upload: http://localhost:5000/upload
2. Kéo thả hoặc chọn file audio (MP3, WAV, MP4...)
3. Chọn ngôn ngữ và loại cuộc họp
4. **Dán URL Colab vào ô "Colab WhisperX URL"**
5. Bấm **"Upload và phân tích"**
6. Đợi 2-5 phút xử lý (tùy độ dài file)
7. Nhận kết quả tương tự Live Meeting

#### Sau khi upload

1. Tắt Colab nếu không dùng nữa
2. Export kết quả
3. Xem lại trong History

---

### 🆚 So sánh Live Meeting vs Upload

| Tính năng | Live Meeting | Upload |
|-----------|--------------|--------|
| **Input** | Ghi âm trực tiếp | File có sẵn |
| **Web Speech API** | ✅ (live preview) | ❌ |
| **MediaRecorder** | ✅ | ❌ |
| **WhisperX** | ✅ | ✅ |
| **Diarization** | Manual + Auto | Auto only |
| **Use case** | Họp đang diễn ra | Họp đã ghi sẵn |
| **Colab setup** | Cần | Cần (nếu dùng Zero Cost) |

---

## 💰 Chi phí

| Dịch vụ | Chi phí | Giới hạn |
|---------|---------|----------|
| Google Colab (GPU T4) | **$0** | ~12 giờ/ngày |
| Gemini 1.5 Flash | **$0** | 15 requests/phút |
| ngrok | **$0** | 1 tunnel đồng thời |
| Web Speech API | **$0** | Không giới hạn |

**Tổng chi phí: $0/tháng** 🎉

---

## �  Speaker Diarization (Phân biệt người nói)

### Giai đoạn 1: Trong họp (Manual)
- Chọn người nói từ dropdown
- Mỗi người có màu riêng (6 màu)
- Keyboard shortcuts: Ctrl+1-9
- **Độ chính xác: 100%** (do bạn chọn)

### Giai đoạn 2: Sau họp (Auto)
- WhisperX + pyannote.audio
- Tự động phân biệt giọng nói
- **Độ chính xác: 85-95%**
- Không cần làm gì thêm!

### Tips tăng độ chính xác Auto Diarization:
- ✅ Nói lần lượt, không chồng lấn
- ✅ Giọng nói khác biệt rõ ràng
- ✅ Audio chất lượng tốt
- ✅ 2-4 người (tốt nhất), >5 người (khó hơn)

---

## 🔧 Troubleshooting

### Lỗi: "Colab transcription failed"
- ✅ Kiểm tra URL ngrok có đúng không
- ✅ Kiểm tra Colab notebook còn chạy không
- ✅ Test endpoint: `curl https://your-url.ngrok-free.app/health`

### Lỗi: "Speech recognition error"
- ✅ Chỉ hỗ trợ Chrome/Edge (không hỗ trợ Firefox)
- ✅ Kiểm tra microphone đã được cho phép chưa
- ✅ Lỗi này không ảnh hưởng đến ghi âm chính

### Lỗi: "Gemini API quota exceeded"
- ✅ Đợi 1 phút rồi thử lại
- ✅ Kiểm tra API key còn hạn không

### Colab bị disconnect
- ✅ Colab free có giới hạn ~12 giờ/ngày
- ✅ Chạy lại notebook và lấy URL mới
- ✅ Nếu cần dùng lâu, nâng cấp Colab Pro ($10/tháng)

---

## 🎓 Tips & Tricks

### Tăng độ chính xác
- ✅ Ghi âm trong môi trường yên tĩnh
- ✅ Dùng microphone tốt
- ✅ Nói rõ ràng, không quá nhanh

### Tiết kiệm thời gian Colab
- ✅ Chỉ mở Colab khi cần họp
- ✅ Tắt ngay sau khi xử lý xong
- ✅ Không để Colab chạy suốt ngày

### Xử lý file lớn
- ✅ Colab free xử lý được file ~2 giờ
- ✅ File > 2 giờ: chia nhỏ hoặc dùng Colab Pro

---

## 🆚 So sánh với các giải pháp khác

| Tính năng | Zero Cost Model | Otter.ai | Fireflies.ai |
|-----------|----------------|----------|--------------|
| Chi phí | **$0** | $8.33/tháng | $10/tháng |
| Thời lượng | Không giới hạn | 300 phút/tháng | 800 phút/tháng |
| Speaker Diarization | ✅ | ✅ | ✅ |
| AI Summary | ✅ (Gemini) | ✅ | ✅ |
| Privacy | ✅ (Tự host) | ❌ (Cloud) | ❌ (Cloud) |
| Offline | ❌ | ❌ | ❌ |

---

## 📚 Tài liệu tham khảo

- WhisperX: https://github.com/m-bain/whisperX
- Gemini API: https://ai.google.dev/gemini-api/docs
- ngrok: https://ngrok.com/docs
- Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

---

## 🤝 Đóng góp

Nếu bạn có ý tưởng cải thiện, hãy tạo issue hoặc pull request!

---

**Made with ❤️ by Akari AI Team**
