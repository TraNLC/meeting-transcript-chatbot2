import pytest
import sys
from pathlib import Path

# Add root to python path
sys.path.append(str(Path(__file__).parent.parent))

from app import create_app, socketio

@pytest.fixture
def app():
    app = create_app('development')
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test",
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def socket_client(app):
    return socketio.test_client(app)
