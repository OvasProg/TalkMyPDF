from deep_translator import GoogleTranslator
import re

# Translate text between languages and clean the result
def translate_text(text, source_lang, target_lang):
    translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    cleaned_text = clean_translated_text(translated_text)
    return cleaned_text

# Clean up formatting issues in translated text
def clean_translated_text(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')  # Normalize line endings
    text = text.replace('\u00A0', ' ').replace('\u3000', ' ')  # Normalize special spaces
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with space
    text = re.sub(r'\n{2,}', '\n\n', text)  # Keep paragraph spacing
    text = re.sub(r'[ \t]+', ' ', text)  # Collapse multiple spaces/tabs
    text = re.sub(r' *\n *', '\n', text)  # Trim spaces around newlines
    return text.strip()
