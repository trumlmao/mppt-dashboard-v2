# app/routes.py
from flask import Blueprint, render_template, jsonify
from .data_manager import DataManager
import os

# Tạo một Blueprint tên là 'main'
main_bp = Blueprint('main', __name__)

# ---- Khởi tạo DataManager ----
# Đây là một cách để DataManager chỉ được khởi tạo một lần
# và có thể truy cập được bởi các route trong blueprint này
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
state_file_path = os.path.join(project_root, 'latest_state.json')
data_manager = DataManager(state_file=state_file_path)

# Các route bây giờ được đăng ký với blueprint, không phải app
@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/latest-data')
def get_latest_data():
    return jsonify(data_manager.get_latest_data())

@main_bp.route('/api/historical-data')
def get_historical_data():
    return jsonify(data_manager.query_historical_data(time_range='-10m'))