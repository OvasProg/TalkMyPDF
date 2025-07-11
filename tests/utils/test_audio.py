import io
import pytest
from app.utils.audio import split_text_by_sentence, generate_audio

# ---- UNIT TESTS FOR TEXT SPLITTING ----

# Basic sentence splitting test
def test_split_text_simple():
    text = "Hello world. How are you? This is a test!"
    sentences = split_text_by_sentence(text)
    assert len(sentences) == 3
    assert sentences[0].startswith("Hello")
    assert all(len(s.encode()) <= 900 for s in sentences)

# Ensure overly long sentence is chunked safely
def test_split_text_overflow():
    long_sentence = "word " * 5000
    sentences = split_text_by_sentence(long_sentence)
    assert all(len(s.encode()) <= 900 for s in sentences)

# Test handling of text exactly near 900-byte threshold
def test_split_text_exact_limit():
    # Make a string close to 900 bytes
    chunk = "a" * 895
    text = f"{chunk}. More text here."
    result = split_text_by_sentence(text)
    assert any("More text" in r for r in result)

# ---- UNIT TESTS FOR generate_audio() ----

from unittest.mock import patch, MagicMock

# Test male voice synthesis with mocked TTS client
@patch("app.utils.audio.texttospeech.TextToSpeechClient")
def test_generate_audio_male(mock_tts_client):
    # Mock response object with dummy audio content
    mock_response = MagicMock()
    mock_response.audio_content = b"FAKEAUDIO"
    mock_tts_client.return_value.synthesize_speech.return_value = mock_response

    buffer = generate_audio("Hello. How are you?", voice="male")
    assert isinstance(buffer, io.BytesIO)
    assert buffer.getvalue() == b"FAKEAUDIOFAKEAUDIO"  # two sentences

# Test female voice synthesis with mocked TTS client
@patch("app.utils.audio.texttospeech.TextToSpeechClient")
def test_generate_audio_female(mock_tts_client):
    mock_response = MagicMock()
    mock_response.audio_content = b"BINAUDIO"
    mock_tts_client.return_value.synthesize_speech.return_value = mock_response

    buffer = generate_audio("Bonjour le monde!", voice="female")
    assert buffer.getvalue() == b"BINAUDIO"