from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, EqualTo, Length, DataRequired, NoneOf, Regexp, ValidationError

special_characters = "*?!'^+%&/()=}][{$#@<>"
uppercase_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase_characters = "abcdefghijklmnopqrstuvwxyz"
digits = "0123456789"


def check_password_special(form, field):
    data = field.data  # capture field data in variable
    for c in special_characters:  # iterate through and return if at least one special character in data
        if c in data:
            return
    raise ValidationError(
        f"Password must contain at least one special character ({special_characters}).")  # if none found show error message


def check_password_upper(form, field):
    data = field.data  # capture field data in variable
    for c in uppercase_characters:  # iterate through and return if at least one upper case letter in data
        if c in data:
            return
    raise ValidationError("Password must contain at least one uppercase character.")  # if none found show error message


def check_password_lower(form, field):
    data = field.data  # capture field data in variable
    for c in lowercase_characters:  # iterate through and return if at least one lower case letter in data
        if c in data:
            return
    raise ValidationError("Password must contain at least one lowercase character.")  # if none found show error message


def check_password_digit(form, field):
    data = field.data  # capture field data in variable
    for c in digits:  # iterate through and return if at least one digit in data
        if c in data:
            return
    raise ValidationError("Password must contain at least one digit.")  # if none found show error message


class RegisterForm(FlaskForm):
    # Set up fields
    email = StringField(validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired(),
                                        NoneOf(special_characters, "Username must not contain any special "
                                                                   "characters (%(values)s).")])

    password = PasswordField(validators=[DataRequired(),
                                         Length(6, 12, "Password must be between 6 and 12 characters long."),
                                         check_password_special,
                                         check_password_upper,
                                         check_password_lower,
                                         check_password_digit])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo("password", "Passwords do not match.")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    # Set up fields
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()