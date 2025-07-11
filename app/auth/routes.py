from flask import Blueprint, render_template, session, redirect, url_for, flash
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.models import User
from app import db
from forms import LoginForm, SignUpForm

auth_bp = Blueprint("auth", __name__)

ph = PasswordHasher()

# Homepage route. Redirects to dashboard if user is logged in
@auth_bp.route('/')
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("index.html")

# Login route
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if not user:
            flash("No user found with this email.")
        else:
            try:
                ph.verify(user.password, password)
                session.permanent = True
                session["user_id"] = user.id
                return redirect(url_for("dashboard.dashboard"))
            except VerifyMismatchError:
                flash("Invalid credentials.")
    return render_template("login.html", form=form)

# Sign-up route
@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        password = ph.hash(form.password.data)

        existing = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()
        if existing:
            flash("Email already registered.")
        else:
            db.session.add(User(email=email, password=password))
            db.session.commit()
            user = db.session.execute(
                db.select(User).where(User.email == email)
            ).scalar_one()
            session.permanent = True
            session['user_id'] = user.id
            return redirect(url_for("dashboard.dashboard"))

    return render_template("signup.html", form=form)

# Logout route. Clears session and redirects to home
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.home"))