import io
import pytest
from app.utils import pdf
from flask import Flask, request, redirect, url_for
from PyPDF2 import PdfReader

# Create a minimal Flask app for test context
@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test"

    @app.route("/dashboard")
    def dashboard():
        return "Dashboard"

    return app

# Utility: create a small in-memory PDF using PyMuPDF
def create_test_pdf_bytes(text="Hello, PDF!"):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Test extracting text from a valid uploaded PDF
def test_extract_pdf_text_success(app, client):
    data = {
        "pdf_file": (create_test_pdf_bytes(), "test.pdf")
    }

    with app.test_request_context(method="POST", data=data, content_type='multipart/form-data'):
        text, error = pdf.extract_pdf_text()
        assert error is None
        assert "Hello" in text

# Test behavior when no file is uploaded
def test_extract_pdf_text_missing_file(app):
    with app.test_request_context(method="POST", data={}):
        text, error = pdf.extract_pdf_text()
        assert text is None
        assert error.status_code == 302

# Test extraction from an empty PDF
def test_extract_pdf_text_empty_pdf(app):
    empty_pdf = io.BytesIO(b"%PDF-1.4\n%%EOF")
    with app.test_request_context(method="POST", data={"pdf_file": empty_pdf}):
        text, error = pdf.extract_pdf_text()
        assert text is None
        assert error.status_code == 302

# Test PDF generation from English text
def test_create_pdf_with_english_text():
    buffer = pdf.create_pdf("Hello, this is a test PDF.", lang="en")
    assert isinstance(buffer, io.BytesIO)
    buffer.seek(0)
    reader = PdfReader(buffer)
    content = "".join(p.extract_text() or "" for p in reader.pages)
    assert "Hello" in content

# Test PDF creation with auto language detection (mocked as French)
def test_create_pdf_with_auto_language_detection(monkeypatch):
    monkeypatch.setattr("app.utils.pdf.detect", lambda x: "fr")
    buffer = pdf.create_pdf("Bonjour le monde.")
    buffer.seek(0)
    reader = PdfReader(buffer)
    content = "".join(p.extract_text() or "" for p in reader.pages)
    assert "Bonjour" in content

# Test PDF generation with Arabic text and font
def test_create_pdf_with_arabic_text():
    buffer = pdf.create_pdf("مرحبا بالعالم", lang="ar")
    assert isinstance(buffer, io.BytesIO)