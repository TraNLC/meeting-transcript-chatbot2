from app import create_app, socketio
import os

app = create_app('development')

if __name__ == '__main__':
    print("=" * 80)
    print("Meeting Analyzer Pro - Mapped to Modular Structure")
    print("=" * 80)
    print("Starting server...")
    print("URL: http://localhost:5000")
    print("WebSocket: Enabled")
    print("=" * 80)
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )
