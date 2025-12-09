import backend.utils.ffmpeg_helper # Auto-setup ffmpeg path (MUST BE FIRST)
from app import create_app, socketio
import os
import logging

# Giảm log của werkzeug và socketio
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from app import create_app, socketio
import os
import logging

# Giảm log của werkzeug và socketio
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

app = create_app('development')

if __name__ == '__main__':
    # Force reload trigger v2 - Performance Fixes Applied 🚀
    try:
        # Pring with emoji might fail on some windows consoles, so wrap in try/except
        print("🤖 Akari.AI is starting...")
        print("   http://localhost:5000")
    except:
        print("Akari.AI is starting...")
        print("http://localhost:5000")
    print("-" * 40)
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True,
        log_output=False
    )
