import pytest
import tempfile
import os
from app import create_app

@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(str(db_path))
    yield app
    os.remove(str(db_path))

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_path(app):
    return app.config["DB_PATH"]

