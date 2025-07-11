import pytest
from app.utils.translate import clean_translated_text, translate_text
from unittest.mock import patch

# ---- UNIT TESTS FOR CLEANER ----

# Test newline normalization and paragraph handling
def test_clean_translated_text_newlines():
    raw = "Line one.\r\nLine two.\rLine three.\n\n\nLine four."
    cleaned = clean_translated_text(raw)
    assert "Line one. Line two. Line three." in cleaned
    assert "\n\nLine four." in cleaned

# Test special space characters and whitespace cleanup
def test_clean_translated_text_spaces():
    raw = "This\u00A0is\u3000a test.\nThis   line\t\tshould be cleaned."
    cleaned = clean_translated_text(raw)
    assert "This is a test." in cleaned
    assert "line should" in cleaned
    assert "\t" not in cleaned

# Test leading/trailing whitespace trimming
def test_clean_translated_text_strip():
    raw = "\n   Hello world!   \n"
    cleaned = clean_translated_text(raw)
    assert cleaned == "Hello world!"

# ---- UNIT TEST FOR TRANSLATE ----

# Test full translation pipeline with mocked GoogleTranslator
@patch("app.utils.translate.GoogleTranslator.translate")
def test_translate_text_with_mock(mock_translate):
    mock_translate.return_value = "Bonjour  le   monde. \n \nC'est    génial!"

    result = translate_text("Hello world", "en", "fr")

    assert "Bonjour le monde." in result
    assert "  " not in result  # spaces cleaned