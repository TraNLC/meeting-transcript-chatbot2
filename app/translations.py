"""
Translation dictionaries for the application.
"""

translations = {
    "vi": {
        "title": "Akari AI - Trợ lý cuộc họp thông minh",
        "home_title": "Tập trung vào điều quan trọng.",
        "home_highlight": "AI sẽ ghi chép.",
        "home_subtitle": "Tự động chuyển đổi, phân tích và tóm tắt cuộc họp của bạn",
        "browser_record": "Ghi âm Browser",
        "browser_desc": "Ghi âm cuộc họp Online (Zoom, Meet, Teams) trên trình duyệt",
        "mic_record": "Ghi âm Mic",
        "mic_desc": "Ghi âm trực tiếp qua Microphone và xuất văn bản",
        "upload": "Upload & Phân tích",
        "upload_desc": "Upload Audio/Video/Text và nhận phân tích AI",
        "history": "Lịch sử",
        "history_desc": "Xem lại các cuộc họp và phân tích đã thực hiện",
        "home_btn": "Trang chủ"
    },
    "en": {
        "title": "Akari AI - Smart Meeting Assistant",
        "home_title": "Focus on what matters.",
        "home_highlight": "AI takes notes.",
        "home_subtitle": "Automatically transcribe, analyze, and summarize your meetings",
        "browser_record": "Browser Recording",
        "browser_desc": "Record Online meetings (Zoom, Meet, Teams) in browser",
        "mic_record": "Mic Recording",
        "mic_desc": "Record directly via Microphone and get transcript",
        "upload": "Upload & Analyze",
        "upload_desc": "Upload Audio/Video/Text and get AI analysis",
        "history": "History",
        "history_desc": "Review past meetings and analysis",
        "home_btn": "Home"
    }
}

def get_translations(lang="vi"):
    return translations.get(lang, translations["vi"])
