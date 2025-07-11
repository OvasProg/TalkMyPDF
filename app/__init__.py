from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import timedelta

# Global DB object (imported by models)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Load environment variables
    load_dotenv()

    import logging
    logging.basicConfig(level=logging.INFO)

    # Create Flask app, aware of instance folders
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='static',
        template_folder='templates'
    )

    # Environment-based configuration
    env = os.getenv("FLASK_ENV", "production")
    app.config["ENV"] = env
    app.config["DEBUG"] = env == "development"  # Auto-enable debug in dev only

    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
    )

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.errors.handlers import errors_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(errors_bp)

    # # Create database tables if not exist
    # with app.app_context():
    #     from app import models
    #     db.create_all()

    return app