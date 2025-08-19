# app/web_app.py
from flask import Flask, render_template, jsonify
from data_manager import DataManager
import os

# ---- Cấu hình Đường dẫn ----
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_folder = os.path.join(project_root, 'app/templates')

# ---- Khởi tạo Ứng dụng ----
app = Flask(__name__, template_folder=template_folder)

# Tạo đối tượng DataManager, trỏ đến đúng vị trí file state
state_file_path = os.path.join(project_root, 'latest_state.json')
# SỬA LỖI: Xóa bỏ tham số log_dir không còn tồn tại
data_manager = DataManager(state_file=state_file_path)

# ---- Các Route (đường dẫn web) ----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/latest-data')
def get_latest_data():
    return jsonify(data_manager.get_latest_data())

# ---- Chạy ứng dụng ----
if __name__ == '__main__':
    print(f"Khởi động Web App. Mở trình duyệt và truy cập http://12.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)