from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    username = StringField(validators=[Required(), Length(min=5, max=20, message='Username must be between '
                                                                                 '5 and 20 characters in length. ')])
    password = PasswordField(validators=[Required(), Length(min=8, max=15, message='Password must be between 8 and '
                                                                                   '15 characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password',
                                                                     message='Passwords must be equal.')])
    submit = SubmitField()