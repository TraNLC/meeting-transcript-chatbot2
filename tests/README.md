# Test Suite Documentation

## Tổng quan

Test suite này được thiết kế để kiểm tra toàn bộ chức năng upload và phân tích file của Meeting Transcript Chatbot, bao gồm:
- **Text files**: TXT, PDF, DOCX
- **Audio files**: MP3, WAV, WebM, M4A, OGG, FLAC
- **Video files**: MP4 (audio extraction)

## Cấu trúc thư mục

```
tests/
├── test_cases/              # YAML test case definitions
│   ├── upload_txt_tests.yaml
│   ├── upload_docx_tests.yaml
│   ├── upload_pdf_tests.yaml
│   ├── upload_wav_tests.yaml
│   ├── upload_mp3_tests.yaml
│   ├── upload_mp4_tests.yaml
│   └── upload_webm_tests.yaml
├── test_scripts/            # Generated Python test files
│   ├── test_txt_upload.py
│   ├── test_docx_upload.py
│   ├── test_pdf_upload.py
│   ├── test_wav_upload.py
│   ├── test_mp3_upload.py
│   ├── test_mp4_upload.py
│   └── test_webm_upload.py
├── test_generator.py        # Test generator script
├── test_summary.py          # Test statistics generator
└── README.md               # This file
```

## Các loại file được hỗ trợ

### Text Files (tối đa 100MB)
- **TXT**: Plain text files - Transcript văn bản thuần túy
- **DOCX**: Microsoft Word documents - Báo cáo cuộc họp định dạng Word
- **PDF**: PDF documents - Tài liệu PDF với text extraction

### Audio/Video Files (tối đa 100MB)
> **Lưu ý**: Với AI free (Groq, Hugging Face), giới hạn 100MB là hợp lý cho:
> - Audio chất lượng tốt: ~1-2 giờ (MP3 128kbps)
> - Audio chất lượng cao: ~30-45 phút (WAV 16kHz)
> - Video: ~10-15 phút (MP4 720p)

- **WAV**: Waveform Audio File Format - Chất lượng cao nhất, không nén
- **MP3**: MPEG Audio Layer 3 - Phổ biến nhất, nén tốt
- **MP4**: MPEG-4 Video - Trích xuất audio từ video
- **WebM**: Web Media format - Ghi âm từ trình duyệt

## Test Categories

### 1. Text File Tests
- **AI Analysis**: Summary quality, topic extraction, action items
- **Multi-language**: Vietnamese, English, Japanese
- **Content Understanding**: Technical content, short content, complex content
- **Edge Cases**: Minimal content, mixed languages, Unicode

### 2. PDF Tests
- **Parsing**: Simple PDF, multi-page PDF
- **Format Variations**: Images, tables, scanned PDF
- **Security**: Password-protected, corrupted files
- **Performance**: Large files, 100+ pages

### 3. DOCX Tests
- **Parsing**: Simple DOCX, multi-page DOCX
- **Format Variations**: Images, tables, formatting, headers/footers
- **Security**: Password-protected, corrupted files
- **Performance**: Large files, 100+ pages

### 4. Audio Tests (All formats)
- **STT + AI**: Transcription accuracy, AI analysis quality
- **Quality Variations**: Clear audio, noisy audio, low quality
- **Duration**: Short (< 30s), Medium (5-10 min), Long (> 30 min)
- **Language**: Vietnamese, English, mixed languages
- **Speaker Diarization**: Multiple speakers, interview format

### 5. Format-Specific Tests

#### WAV
- Sample rate (8kHz, 16kHz, 44.1kHz, 48kHz)
- Quality variations
- Speaker separation

#### MP3
- Bitrate variations (64kbps, 320kbps)
- Duration handling
- Compression quality

#### MP4
- Video quality (360p, 1080p)
- Codec variations (H.264, H.265)
- Audio extraction quality

#### WebM
- Browser recordings (Chrome, Firefox)
- Codec variations (Opus, Vorbis)
- Web recording quality

## Cách sử dụng

### 1. Generate test scripts từ YAML

```bash
cd tests
python test_generator.py
```

Script này sẽ đọc tất cả các file YAML trong `test_cases/` và tạo ra các file Python test tương ứng trong `test_scripts/`.

### 2. Chạy tất cả tests

```bash
# Chạy tất cả tests
pytest tests/test_scripts/ -v

# Chạy test cho một loại file cụ thể
pytest tests/test_scripts/test_mp3_upload.py -v
pytest tests/test_scripts/test_pdf_upload.py -v

# Chạy test với category cụ thể
pytest tests/test_scripts/ -v -k "mp3_stt_ai"
pytest tests/test_scripts/ -v -k "pdf_parsing"
```

### 3. Chạy test với filter

```bash
# Chỉ chạy critical tests
pytest tests/test_scripts/ -v -m critical

# Chỉ chạy high priority tests
pytest tests/test_scripts/ -v -m high

# Chạy tests cho một category
pytest tests/test_scripts/ -v -k "stt_ai"
```

## YAML Test Case Format

```yaml
test_suite:
  name: "Test Suite Name"
  endpoint: "http://localhost:5000/api/upload/process"
  file_type: "audio" # or "text"
  description: "Test description"

test_cases:
  - id: TEST001
    name: "Test case name"
    priority: "critical" # critical, high, medium, low
    category: "test_category"
    input:
      file: "mocks/test_file.mp3"
      file_type: "audio"
      meeting_type: "meeting"
      transcribe_lang: "vi"
      output_lang: "vi"
    expected:
      status_code: 200
      ai_validations:
        - "len(result['transcript']) > 100"
        - "len(result['summary']) > 50"
      max_response_time: 120
```

## Mock Files

Các file mock cần được chuẩn bị trong thư mục `mocks/`:

### Text Files
- `meeting_sample.txt`
- `interview_sample.txt`
- `brainstorm_sample.txt`
- `meeting_report.pdf`
- `meeting_report.docx`

### Audio Files
- `clear_meeting.{wav,mp3,webm}`
- `english_meeting.{wav,mp3,webm}`
- `noisy_meeting.wav`
- `short_meeting.{wav,mp3,webm}`
- `medium_meeting.{wav,mp3,webm}`
- `long_meeting.{wav,mp3,webm}`

### Video Files
- `clear_meeting.mp4`
- `english_meeting.mp4`

## Test Statistics

| File Type | Test Cases | Focus Areas |
|-----------|-----------|-------------|
| TXT | 14 | AI analysis, multi-language, content understanding |
| DOCX | 12 | Parsing, format handling, security |
| PDF | 11 | Parsing, format handling, security |
| WAV | 8 | Sample rate, quality, speaker separation |
| MP3 | 8 | Bitrate, duration, compression |
| MP4 | 9 | Video quality, audio extraction |
| WebM | 8 | Browser recordings, codecs |
| **Total** | **70** | **Comprehensive coverage** |

## CI/CD Integration

Để tích hợp vào CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      - name: Generate tests
        run: python tests/test_generator.py
      - name: Run tests
        run: pytest tests/test_scripts/ -v --tb=short
```

## Lưu ý

1. **Server phải chạy**: Đảm bảo Flask server đang chạy tại `http://localhost:5000`
2. **Mock files**: Chuẩn bị đầy đủ mock files trong thư mục `mocks/`
3. **API keys**: Đảm bảo có API keys cho Groq/OpenAI trong `.env`
4. **Timeout**: Một số tests có thể mất nhiều thời gian (STT, AI analysis)
5. **File size limits**: 
   - Text files (TXT, DOCX, PDF): 100MB
   - Audio files (WAV, MP3, MP4, WebM): Khuyến nghị 100MB cho free tier AI

## Troubleshooting

### Test fails với "Mock file not found"
- Kiểm tra xem file mock có tồn tại trong `mocks/`
- Đảm bảo đường dẫn file đúng trong YAML

### Test fails với "Connection refused"
- Đảm bảo Flask server đang chạy
- Kiểm tra port 5000 có bị chiếm không

### Test fails với "API quota exceeded"
- Đợi vài phút và thử lại
- Kiểm tra API keys trong `.env`

### Test timeout
- Tăng timeout trong YAML: `max_response_time: 300`
- Kiểm tra file size không quá lớn
