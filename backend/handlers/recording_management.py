"""Handlers for recording history in Tab 1."""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


def get_recordings_grouped_by_date(filter_type: str = "Tất cả", search_query: str = "") -> str:
    """Get recordings grouped by date for sidebar display.
    
    Args:
        filter_type: "Tất cả", "Hôm nay", "Tuần này", "Tháng này"
        search_query: Search text
        
    Returns:
        HTML string with grouped recordings
    """
    try:
        metadata_file = Path("data/recordings/metadata.json")
        
        if not metadata_file.exists():
            return """
            <div style="padding: 20px; text-align: center; color: #666;">
                <p>📭 Chưa có bản ghi âm nào</p>
                <p style="font-size: 12px;">Bắt đầu ghi âm để xem lịch sử</p>
            </div>
            """
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recordings = data.get('recordings', [])
        
        if not recordings:
            return """
            <div style="padding: 20px; text-align: center; color: #666;">
                <p>📭 Chưa có bản ghi âm nào</p>
            </div>
            """
        
        # Filter by date
        now = datetime.now()
        filtered = []
        
        for rec in recordings:
            rec_date = datetime.fromisoformat(rec['timestamp'])
            
            # Apply date filter
            if filter_type == "Hôm nay":
                if rec_date.date() != now.date():
                    continue
            elif filter_type == "Tuần này":
                week_ago = now - timedelta(days=7)
                if rec_date < week_ago:
                    continue
            elif filter_type == "Tháng này":
                if rec_date.month != now.month or rec_date.year != now.year:
                    continue
            
            # Apply search filter
            if search_query:
                title = rec.get('title', '').lower()
                if search_query.lower() not in title:
                    continue
            
            filtered.append(rec)
        
        if not filtered:
            return """
            <div style="padding: 20px; text-align: center; color: #666;">
                <p>🔍 Không tìm thấy kết quả</p>
            </div>
            """
        
        # Group by date
        grouped = {}
        for rec in filtered:
            rec_date = datetime.fromisoformat(rec['timestamp'])
            date_key = rec_date.date()
            
            if date_key not in grouped:
                grouped[date_key] = []
            
            grouped[date_key].append(rec)
        
        # Sort by date (newest first)
        sorted_dates = sorted(grouped.keys(), reverse=True)
        
        # Build HTML
        html_parts = ['<div style="max-height: 500px; overflow-y: auto; padding: 5px;">']
        
        for date_key in sorted_dates:
            # Date label
            if date_key == now.date():
                date_label = "Hôm nay"
            elif date_key == (now - timedelta(days=1)).date():
                date_label = "Hôm qua"
            else:
                date_label = date_key.strftime("%d/%m/%Y")
            
            html_parts.append(f'<div style="margin-bottom: 15px;">')
            html_parts.append(f'<div style="font-size: 11px; color: #666; margin-bottom: 5px; font-weight: 600;">{date_label}</div>')
            
            # Recordings for this date
            for rec in grouped[date_key]:
                rec_id = rec.get('id', '')
                title = rec.get('title', 'Untitled')
                duration = rec.get('duration', 0)
                
                # Format duration
                if duration > 0:
                    mins = int(duration // 60)
                    secs = int(duration % 60)
                    duration_str = f"{mins}:{secs:02d}"
                else:
                    duration_str = "?"
                
                # Recording item
                html_parts.append(f'''
                <div class="recording-item" data-id="{rec_id}" 
                     style="padding: 8px; background: #f3f4f6; border-radius: 5px; margin-bottom: 5px; 
                            cursor: pointer; font-size: 13px; transition: all 0.2s;"
                     onmouseover="this.style.background='#e5e7eb'"
                     onmouseout="this.style.background='#f3f4f6'"
                     onclick="selectRecording('{rec_id}')">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span>📝 {title}</span>
                        <span style="font-size: 11px; color: #666;">{duration_str}</span>
                    </div>
                </div>
                ''')
            
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        
        # Add JavaScript for selection
        html_parts.append('''
        <script>
        function selectRecording(id) {
            console.log('Selected recording:', id);
            // Trigger Gradio event to load recording
            // This will be handled by event handlers
        }
        </script>
        ''')
        
        return ''.join(html_parts)
        
    except Exception as e:
        return f"""
        <div style="padding: 20px; text-align: center; color: #dc2626;">
            <p>❌ Lỗi: {str(e)}</p>
        </div>
        """


def load_selected_recording(recording_id: str) -> Tuple[str, str, str]:
    """Load a selected recording from history.
    
    Args:
        recording_id: Recording ID
        
    Returns:
        Tuple of (audio_path, transcript, info_markdown)
    """
    try:
        metadata_file = Path("data/recordings/metadata.json")
        
        if not metadata_file.exists():
            return None, "", "❌ Không tìm thấy metadata"
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recordings = data.get('recordings', [])
        
        # Find recording
        recording = None
        for rec in recordings:
            if rec.get('id') == recording_id:
                recording = rec
                break
        
        if not recording:
            return None, "", "❌ Không tìm thấy bản ghi âm"
        
        # Get info
        title = recording.get('title', 'Untitled')
        timestamp = recording.get('timestamp', '')
        duration = recording.get('duration', 0)
        language = recording.get('language', 'vi')
        audio_path = recording.get('audio_file', '')
        transcript = recording.get('transcript', '')
        
        # Format info
        rec_date = datetime.fromisoformat(timestamp)
        date_str = rec_date.strftime("%d/%m/%Y %H:%M")
        
        mins = int(duration // 60)
        secs = int(duration % 60)
        duration_str = f"{mins}:{secs:02d}"
        
        info_md = f"""### 📝 {title}

**Ngày:** {date_str}  
**Thời lượng:** {duration_str}  
**Ngôn ngữ:** {language.upper()}
"""
        
        return audio_path, transcript, info_md
        
    except Exception as e:
        return None, "", f"❌ Lỗi: {str(e)}"


def delete_selected_recording(recording_id: str) -> Tuple[str, str]:
    """Delete a recording from history.
    
    Args:
        recording_id: Recording ID
        
    Returns:
        Tuple of (status_message, updated_html)
    """
    try:
        metadata_file = Path("data/recordings/metadata.json")
        
        if not metadata_file.exists():
            return "❌ Không tìm thấy metadata", ""
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recordings = data.get('recordings', [])
        
        # Find and remove recording
        recording = None
        for i, rec in enumerate(recordings):
            if rec.get('id') == recording_id:
                recording = recordings.pop(i)
                break
        
        if not recording:
            return "❌ Không tìm thấy bản ghi âm", ""
        
        # Delete audio file
        audio_path = Path(recording.get('audio_file', ''))
        if audio_path.exists():
            audio_path.unlink()
        
        # Save updated metadata
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Refresh list
        updated_html = get_recordings_grouped_by_date()
        
        return f"✅ Đã xóa: {recording.get('title', 'Untitled')}", updated_html
        
    except Exception as e:
        return f"❌ Lỗi: {str(e)}", ""
