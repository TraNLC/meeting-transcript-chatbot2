from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import config

socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Register Blueprints
    from .blueprints.main import main_bp
    app.register_blueprint(main_bp)

    from .blueprints.api_recording import recording_bp
    app.register_blueprint(recording_bp, url_prefix='/api/recording')
    
    from .blueprints.api_upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    
    from .blueprints.api_chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    from .blueprints.api_search import search_bp
    app.register_blueprint(search_bp, url_prefix='/api/search')
    
    from .blueprints.api_export import export_bp
    app.register_blueprint(export_bp, url_prefix='/api/export')
    
    from .blueprints.api_rag import rag_bp
    app.register_blueprint(rag_bp, url_prefix='/api/rag')
    
    from .blueprints.api_history import history_bp
    app.register_blueprint(history_bp, url_prefix='/api/history')

    # Register Socket events
    from .services import socket_service
    socket_service.init_socket_events(socketio)

    # Global Context Processor for Localization
    from app.translations import get_translations
    from flask import request

    @app.context_processor
    def inject_translations():
        # Priority: 1. Query Param, 2. Cookie, 3. Default 'vi'
        lang = request.args.get('lang') or request.cookies.get('akari_lang') or 'vi'
        t = get_translations(lang)
        return dict(t=t, lang=lang)

    return app
