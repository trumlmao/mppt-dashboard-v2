# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_folder = os.path.join(project_root, 'app/templates')
    app = Flask(__name__, template_folder=template_folder)

    app.config['SECRET_KEY'] = 'a_very_secret_key_change_this_later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mppt_user:mppt_password@localhost:5432/mppt_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' # Giữ nguyên dòng này

    with app.app_context():
        from . import models

        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))

        # SỬA LỖI: Import blueprint từ routes.py
        from .routes import main_bp
        app.register_blueprint(main_bp)

        db.create_all()

    return app