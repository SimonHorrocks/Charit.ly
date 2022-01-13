from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField, DateTimeField

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
    time = DateTimeField(format='%d%m%Y %H-%M-%s', validators=[DataRequired()])
    lat = IntegerField(validators=[DataRequired()])
    lon = IntegerField(validators=[DataRequired()])
    submit = SubmitField()