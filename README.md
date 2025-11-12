# 📝 TalkMyPDF

TalkMyPDF is an AI-powered Flask web application that allows users to upload PDF documents, then interact with them using a variety of smart tools:
- 🔍 Summarize long documents
- ❓ Generate 5 AI-curated questions
- 🌍 Translate text into multiple languages
- 🗣️ Convert text to speech (MP3 download)
- 📥 Export results as PDF or audio

It’s built with modularity, security, and scalability in mind — powered by Cohere AI, Google Cloud TTS, and PostgreSQL.

## 🚀 Features

### 📂 Upload & Process PDFs

Upload a PDF and perform multiple operations directly from the dashboard.

### 🧠 AI-Powered Summarization

Get a concise summary of any PDF using Cohere’s command-a-03-2025 model.

### ❓ Question Generation

Generate 5 educational questions based on your document content.

### 🌍 Language Translation

Translate text to and from the most popular languages using deep-translator.

### 🔊 Text-to-Speech (TTS)

Convert PDF text to natural-sounding audio via Google Cloud Text-to-Speech.
- Select male or female voices
- Download the result as an MP3 file

### 🧾 Export as PDF

All outputs (summary, questions, translations) can be downloaded in PDF format using proper language support fonts.

### 🧠 Smart Daily Limits

Each logged-in user can use every functionality up to 3 times per day.
- Limits reset automatically every new UTC day
- Usage is stored securely in PostgreSQL

### 🔐 Secure Authorization
- Uses Argon2 hashing for storing passwords
- Requires strong passwords (uppercase, lowercase, digits, special symbols)
- Keeps user logged in via 7-day secure cookies

## 🧱 Project Structure

Your application is modular and well-organized:
```
TalkMyPDF_v2/
├── app/
│   ├── auth/          # Login & signup logic
│   ├── dashboard/     # Core features: summary, audio, questions, translation
│   ├── errors/        # Custom error handlers
│   ├── static/        # CSS, fonts, images
│   ├── templates/     # HTML pages
│   ├── utils/         # PDF parsing, audio, summarization, limits, translation
│   ├── models.py      # SQLAlchemy models
│   └── __init__.py    # App factory with config and blueprints
├── migrations/        # Alembic migrations for PostgreSQL
├── tests/             # Unit & integration test suites
├── run.py             # App runner
├── forms.py           # Login & signup forms
├── requirements.txt   # Dependencies
├── .env.example       # Environment variable template
├── README.md          # This file
```
This clean structure enables fast debugging and allows independent updates to features like summarization, translation, etc.

## 🧪 Testing
- Test coverage using pytest
- Includes unit tests for each module
- Includes integration tests for user auth and dashboard functionality

## 🧑‍💻 Local Setup

1. Clone the repository
```git
git clone https://github.com/yourusername/TalkMyPDF_v2.git
cd TalkMyPDF_v2
```
2. Create a virtual environment
```git
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```git
pip install -r requirements.txt
```
4. Set environment variables
```git
cp .env.example .env
# then update .env with your keys
```
5. Run database migrations
```git
flask db upgrade
```
6. Start the app
```git
python run.py
```

## 💬 Future Improvements
- User usage dashboard with visual stats
- Email-based password recovery
- Batch processing for PDFs
- Multi-language audio support
