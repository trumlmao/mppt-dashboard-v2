# app/routes.py
from flask import render_template, jsonify, Blueprint, redirect, flash, url_for# Thêm Blueprint vào import
from .forms import LoginForm , RegistrationForm
from .data_manager import DataManager
import os
from flask_login import logout_user,current_user,login_user
from .models import db,User
# ---- TẠO BLUEPRINT Ở ĐÂY ----
main_bp = Blueprint('main', __name__)

# ---- Khởi tạo DataManager ----
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
state_file_path = os.path.join(project_root, 'latest_state.json')
data_manager = DataManager(state_file=state_file_path)

# ---- Route Chính ----
@main_bp.route('/')
def index():
    return render_template('index.html')

# ---- Route Xác thực ----
@main_bp.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(form.password.data):

            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}!')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)
@main_bp.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data ,email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)



    
@main_bp.route('/logout')
def logout():
    """Xử lý việc đăng xuất người dùng."""
    logout_user() # Hàm này của Flask-Login sẽ xóa session của người dùng
    flash('You have been logged out.')
    return redirect(url_for('main.login')) # Chuyển hướng về trang đăng nhập
# ---- API Endpoints ----
@main_bp.route('/api/latest-data')
def get_latest_data():
    return jsonify(data_manager.get_latest_data())

@main_bp.route('/api/historical-data')
def get_historical_data():
    return jsonify(data_manager.query_historical_data(time_range='-10m'))