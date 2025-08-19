# app/models.py
from flask_login import UserMixin
from . import db # <-- THAY ĐỔI QUAN TRỌNG: Import từ __init__.py

class User(UserMixin, db.Model):
    # ... (phần còn lại của class giữ nguyên) ...
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    devices = db.relationship('Device', backref='owner', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'

class Device(db.Model):
    # ... (phần còn lại của class giữ nguyên) ...
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(80), unique=True, nullable=False)
    device_name = db.Column(db.String(120), nullable=False, default='My MPPT Device')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return f'<Device {self.device_id}>'