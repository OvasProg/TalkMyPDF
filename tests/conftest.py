import pytest
from app import create_app, db
from app.models import User
from argon2 import PasswordHasher

# Creates and configures a new app instance for each test
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "MAX_CONTENT_LENGTH": 5 * 1024 * 1024,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Returns a test client for simulating HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Adds a sample user to the test database
@pytest.fixture
def new_user(app):
    ph = PasswordHasher()
    user = User(email="test@example.com", password=ph.hash("secure123"))
    db.session.add(user)
    db.session.commit()
    return user