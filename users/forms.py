from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class RegisterForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField()