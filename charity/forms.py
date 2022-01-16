from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TimeField, DateField, FloatField

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
    date = DateField(validators=[DataRequired()])
    time = TimeField()
    lat = FloatField(validators=[DataRequired()])
    lon = FloatField(validators=[DataRequired()])
    submit = SubmitField()


class TagForm(FlaskForm):
    subject = StringField(validators=[DataRequired()])
    submit = SubmitField()


class DescriptionForm(FlaskForm):
    description = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()

