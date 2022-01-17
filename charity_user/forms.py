from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewCharityPage(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


class NameForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()

