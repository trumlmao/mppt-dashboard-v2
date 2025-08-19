# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Khởi tạo extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application Factory"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_folder = os.path.join(project_root, 'app/templates')
    app = Flask(__name__, template_folder=template_folder)

    # Cấu hình app
    app.config['SECRET_KEY'] = 'a_very_secret_key_change_this_later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mppt_user:mppt_password@localhost:5432/mppt_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Gắn extensions vào app
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models

        # ---- THÊM HÀM USER_LOADER VÀO ĐÂY ----
        @login_manager.user_loader
        def load_user(user_id):
            # Flask-Login sẽ truyền vào user_id dưới dạng chuỗi (string)
            # Chúng ta cần chuyển nó thành số nguyên (integer) để truy vấn database
            return models.User.query.get(int(user_id))
        # ----------------------------------------

        # Import và đăng ký Blueprint
        from .routes import main_bp
        app.register_blueprint(main_bp)

        # Tạo database
        db.create_all()

    return app