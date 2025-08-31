# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# Chúng ta không cần validator 'Email' cho form này nữa
from wtforms.validators import DataRequired ,EqualTo,Email
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
class LoginForm(FlaskForm):
    """Định nghĩa cấu trúc cho Form Đăng nhập."""
    # THAY ĐỔI: Sử dụng 'username' thay vì 'email'
    username = StringField('Username', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    # THAY ĐỔI NHỎ: Dùng 'Sign In' cho thân thiện hơn
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # VALIDATION NẰM Ở ĐÂY:
    # Flask-WTF tự động gọi các hàm có tên validate_<field_name>
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
