from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TimeField, DateField, FloatField, HiddenField

from wtforms.validators import DataRequired


# form for adding new posts
class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


# form for searching charities/tags
class SearchForm(FlaskForm):
    search = StringField()
    submit = SubmitField()


# form for adding new events
class NewEventForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    date = DateField(validators=[DataRequired()])
    time = TimeField()
    lat = FloatField(validators=[DataRequired()])
    lon = FloatField(validators=[DataRequired()])
    submit = SubmitField()


# form for adding/removing tags
class TagForm(FlaskForm):
    subject = StringField(validators=[DataRequired()])
    submit = SubmitField()


# form for changing description
class DescriptionForm(FlaskForm):
    description = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()


# form for changing name
class NameForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()


# form for adding comments
class CommentForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    reply_to = HiddenField()
    submit = SubmitField()


# form for following charities
class FollowForm(FlaskForm):
    submit = SubmitField()