from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class RegisterForm(FlaskForm):
    email = StringField()
    username = StringField()
    password = PasswordField()
    confirm_password = PasswordField()
    submit = SubmitField()