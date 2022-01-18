from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# form for creating a new charity
class NewCharityPage(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


# form for changing name
class NameForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()

