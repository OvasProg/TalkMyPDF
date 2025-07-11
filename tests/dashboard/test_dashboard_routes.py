import io
import pytest
from unittest.mock import patch
from app.models import User
from argon2 import PasswordHasher

# Fixture that logs in a user for dashboard testing
@pytest.fixture
def logged_in_client(app, client):
    ph = PasswordHasher()
    user = User(email="test@example.com", password=ph.hash("secure123"))
    with app.app_context():
        from app import db
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as sess:
        sess["user_id"] = user_id

    return client

# Utility: create a basic in-memory PDF for testing uploads
def create_test_pdf_bytes(text="Hello PDF"):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Ensure dashboard redirects if user is not logged in
def test_dashboard_requires_login(client):
    response = client.get("/dashboard/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location

# Ensure dashboard renders for logged-in users
def test_dashboard_access(logged_in_client):
    response = logged_in_client.get("/dashboard/")
    assert response.status_code == 200
    assert b"Your PDF Assistant" in response.data

# Mock translation and test PDF download route
@patch("app.utils.translate.translate_text")
def test_download_translate(mock_translate, logged_in_client):
    mock_translate.return_value = "Translated text"

    response = logged_in_client.post("/dashboard/download_translate", data={
        "text": "Translate me",
        "source_lang": "en",
        "target_lang": "es"
    })
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"