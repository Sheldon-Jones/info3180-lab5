# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only Images Allowed')
    ])
