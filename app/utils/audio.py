from google.cloud import texttospeech
import io
import re

# Generate speech audio from text using Google TTS
def generate_audio(text, voice="male"):
    client = texttospeech.TextToSpeechClient()

    # Choose voice profile
    if voice == "male":
        voice_name = "en-US-Chirp3-HD-Algenib"
    else:
        voice_name = "en-US-Chirp3-HD-Aoede"

    # Split text into chunks safe for TTS
    sentences = split_text_by_sentence(text)

    audio_content = b""
    for sentence in sentences:
        if not sentence.strip():
            continue
        
        input_text = texttospeech.SynthesisInput(text=sentence)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        audio_content += response.audio_content


    buffer = io.BytesIO(audio_content)
    buffer.seek(0)
    return buffer

# Split text into TTS-safe chunks, by sentence and byte length
def split_text_by_sentence(text, max_bytes=900):
    text = text[:5000]

    sentence_endings = re.compile(r'(?<=[.؟!?;])\s+')
    sentences = sentence_endings.split(text)

    safe_sentences = []
    for sentence in sentences:
        encoded = sentence.encode('utf-8')
        if len(encoded) <= max_bytes:
            safe_sentences.append(sentence.strip())
        else:
            # Further split overly long sentences into word chunks
            words = sentence.split()
            chunk = ""
            for word in words:
                if len((chunk + " " + word).encode('utf-8')) > max_bytes:
                    if chunk:
                        safe_sentences.append(chunk.strip())
                    chunk = word
                else:
                    chunk += " " + word
            if chunk:
                safe_sentences.append(chunk.strip())
    return safe_sentences
