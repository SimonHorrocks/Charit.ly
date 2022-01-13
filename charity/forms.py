from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, IntegerField, DateTimeField, DateField

from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


class SearchForm(FlaskForm):
    search = StringField()
    submit = SubmitField()


class NewEventForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    time = DateField(format='%d%m%Y', validators=[DataRequired()])
    lat = DecimalField(validators=[DataRequired()])
    lon = DecimalField(validators=[DataRequired()])
    submit = SubmitField()