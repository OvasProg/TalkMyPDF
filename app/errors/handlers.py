from flask import Blueprint, flash, redirect, url_for, session

errors_bp = Blueprint("errors", __name__)

# Handle 404 Not Found errors
@errors_bp.app_errorhandler(404)
def handle_404(e):
    flash("Couldn’t find the page you were looking for. It may have been deleted, or the URL is incorrect.")
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.home"))

# Handle 405 Method Not Allowed errors
@errors_bp.app_errorhandler(405)
def handle_405(e):
    flash("That action is not allowed. Please use the appropriate buttons or links.")
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.home"))

# Handle 413 Payload Too Large errors
@errors_bp.app_errorhandler(413)
def handle_413(e):
    flash("Uploaded file is too big. Try to split it into smaller parts")
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.home"))

# Handle 500 Internal Server Error
@errors_bp.app_errorhandler(500)
def handle_500(e):
    flash("Something went wrong on our end. Please try again later.")
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.home"))