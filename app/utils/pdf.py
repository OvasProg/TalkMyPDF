import fitz
from flask import request, flash, redirect, url_for
from langdetect import detect
import io
from fpdf import FPDF

# Extract text from uploaded PDF file
def extract_pdf_text():
    file = request.files.get("pdf_file")
    if not file:
        flash("Looks like the PDF is missing. Try uploading it again")
        return None, redirect(url_for("dashboard"))

    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()

    if not text:
        flash("Could not extract text from PDF.")
        return None, redirect(url_for("dashboard"))

    return text, None

# Create a downloadable PDF file from text, with language-aware font support
def create_pdf(text, lang="detect"):
    if lang == "detect":
        lang = detect(text)
        print(lang)
    font_args = "NotoSans", "", "app/static/fonts/NotoSans-Regular.ttf", True
    if lang in ["en", "es", "fr", "de", "pt", "it", "ru", "uk"]:
        font_args = "NotoSans", "", "app/static/fonts/NotoSans-Regular.ttf", True
    elif lang == "hi":
        font_args = "NotoSansDevanagari", "", "app/static/fonts/NotoSansDevanagari-Regular.ttf", True
    elif lang in ["zh-CN", "zh-cn", "zh-tw", "zh-TW"]:
        font_args = "NotoSansCJK", "", "app/static/fonts/NotoSansSC-Regular.ttf", True
    elif lang == "ar":
        font_args = "NotoSansArabic", "", "app/static/fonts/NotoSansArabic-Regular.ttf", True

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(*font_args)
    pdf.set_font(font_args[0], "", 12)
    pdf.write(10, text)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)
    return buffer