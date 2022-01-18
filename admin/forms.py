from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from wtforms.validators import DataRequired, Email


# form for changing users' roles
class RolesForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    role = SelectField(u'Role', choices=['user', 'charity', 'admin'])
    submit = SubmitField()
