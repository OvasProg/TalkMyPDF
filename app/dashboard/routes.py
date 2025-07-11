from flask import Blueprint, render_template, request, redirect, session, flash, send_file, url_for
from app.utils.pdf import extract_pdf_text, create_pdf
from app.utils.summarize import generate_summary
from app.utils.translate import translate_text
from app.utils.audio import generate_audio
from app.utils.questions import generate_questions
from app.utils.limits import update_usage
from app.models import Usage
from app import db
from datetime import datetime, timezone

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Dashboard home route
@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    today = datetime.now(timezone.utc).date()
    usages = db.session.execute(
        db.select(Usage).where(Usage.user_id == user_id, Usage.date == today)
    ).scalars().all()

    usage_counts = {u.feature: u.count for u in usages}
    limits = {f: 3 - usage_counts.get(f, 0) for f in ['summary', 'audio', 'translate', 'questions']}

    return render_template("dashboard.html", limits=limits)

# Handle PDF summarization
@dashboard_bp.route('/summary', methods=["POST"])
def summary():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    update_usage(user_id, 'summary')

    text, error = extract_pdf_text()
    if error:
        return error

    summary_text = generate_summary(text)

    return render_template("summary.html", summary_text=summary_text)

# Download the generated summary as PDF
@dashboard_bp.route('/download_summary', methods=["POST"])
def download_summary():
    summary_text = request.form.get("summary_text")
    if not summary_text:
        flash("Something went wrong while generating the file. Please try again later.")
        return redirect(url_for("dashboard"))

    buffer = create_pdf(summary_text)

    return send_file(buffer, as_attachment=True, download_name="summary.pdf", mimetype='application/pdf')

# Handle text-to-speech request
@dashboard_bp.route('/audio', methods=["POST"])
def audio():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    update_usage(user_id, 'audio')

    text, error = extract_pdf_text()
    if error:
        return error

    return render_template("audio.html", text=text)

# Download generated audio file as mp3
@dashboard_bp.route('/download_audio', methods=["POST"])
def download_audio():
    text = request.form.get("audio_text")
    voice = request.form.get("voice")
    if not text:
        flash("Something went wrong while generating the file. Please try again later.")
        return redirect(url_for("dashboard"))

    mp3_file = generate_audio(text, voice)
    return send_file(
        mp3_file,
        as_attachment=True,
        download_name="audio.mp3",
        mimetype="audio/mpeg"
    )

# Handle translation request
@dashboard_bp.route('/translate', methods=["POST"])
def translate():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    update_usage(user_id, 'translate')

    text, error = extract_pdf_text()
    if error:
        return error

    return render_template("translate.html", text=text)

# Download translated text as PDF
@dashboard_bp.route('/download_translate', methods=["POST"])
def download_translate():
    text = request.form.get("text")
    source_lang = request.form.get("source_lang")
    target_lang = request.form.get("target_lang")
    if not text:
        flash("Something went wrong while generating the file. Please try again later.")
        return redirect(url_for("dashboard"))

    translated_text = translate_text(text, source_lang, target_lang)
    if not translated_text:
        flash("Something went wrong while translating the file. Please try again later.")
        return redirect(url_for("dashboard"))

    buffer = create_pdf(translated_text, target_lang)

    return send_file(buffer, as_attachment=True, download_name="translation.pdf", mimetype='application/pdf')

# Handle question generation request
@dashboard_bp.route('/questions', methods=["POST"])
def questions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    update_usage(user_id, 'questions')

    text, error = extract_pdf_text()
    if error:
        return error

    questions = generate_questions(text)

    return render_template("questions.html", questions=questions)

# Download generated questions as PDF
@dashboard_bp.route('/download_questions', methods=["POST"])
def download_questions():
    if not request.referrer or not request.referrer.startswith(request.host_url):
        flash("Direct access to this page is not allowed.")
        return redirect(url_for("dashboard"))
    questions = request.form.get("questions")
    if not questions:
        flash("Something went wrong while generating the file. Please try again later.")
        return redirect(url_for("dashboard"))

    buffer = create_pdf(questions)

    return send_file(buffer, as_attachment=True, download_name="questions.pdf", mimetype='application/pdf')
