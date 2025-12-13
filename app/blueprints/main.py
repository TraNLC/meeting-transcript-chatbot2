from flask import Blueprint, render_template, redirect, url_for, request
from app.translations import get_translations

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage with 4 action cards"""
    return render_template('home.html')

@main_bp.route('/browser_recording')
def browser_recording():
    """Browser recording page"""
    return render_template('browser_recording.html')

@main_bp.route('/mic_recording')
def mic_recording():
    """Microphone recording page"""
    return render_template('mic_recording.html')

# Redirects for legacy routes (to fix 404s if user uses old links)
@main_bp.route('/recording/browser')
def legacy_browser_recording():
    return redirect('/browser_recording')

@main_bp.route('/recording/mic')
def legacy_mic_recording():
    return redirect('/mic_recording')

@main_bp.route('/upload')
def upload_page():
    """Upload and analysis page"""
    return render_template('upload.html')

@main_bp.route('/history')
def history_page():
    """Meeting history page"""
    return render_template('history.html')

@main_bp.route('/record')
def record_page():
    """Record audio only (save to history, no analysis)"""
    return render_template('record.html')

@main_bp.route('/analyze-audio')
def analyze_audio_page():
    """Upload and analyze audio file"""
    return render_template('analyze_audio.html')

@main_bp.route('/analyze-text')
def analyze_text_page():
    """Upload and analyze text/docx/PDF file"""
    return render_template('analyze_text.html')

@main_bp.route('/meeting/<meeting_id>')
def meeting_detail(meeting_id):
    """Meeting detail page"""
    return render_template('meeting_detail.html', meeting_id=meeting_id)

@main_bp.route('/analysis')
def analysis_page():
    """Analysis results page (2-column layout)"""
    return render_template('analysis.html')

@main_bp.route('/recordbrowseranalysis')
def record_browser_analysis():
    """Browser recording analysis page"""
    return render_template('analysis.html')

@main_bp.route('/recordmicanalysis')
def record_mic_analysis():
    """Mic recording analysis page"""
    return render_template('analysis.html')

@main_bp.route('/test-transcript')
def test_transcript():
    """Test page for transcript tab"""
    return render_template('test_transcript.html')
