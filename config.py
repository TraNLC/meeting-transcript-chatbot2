import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'meeting-analyzer-secret-key'
    BASE_DIR = Path(__file__).parent
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    RECORDING_FOLDER = BASE_DIR / 'data' / 'recordings'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB

    @staticmethod
    def init_app(app):
        # Create directories
        Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        Config.RECORDING_FOLDER.mkdir(parents=True, exist_ok=True)
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
