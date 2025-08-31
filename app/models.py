
# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
class User(UserMixin, db.Model):
    # ... (phần còn lại của class giữ nguyên) ...
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    devices = db.relationship('Device', backref='owner', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Device(db.Model):
    # ... (phần còn lại của class giữ nguyên) ...
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(80), unique=True, nullable=False)
    device_name = db.Column(db.String(120), nullable=False, default='My MPPT Device')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return f'<Device {self.device_id}>'