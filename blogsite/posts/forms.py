from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Post_form(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    content = TextAreaField(label='Content', validators=[DataRequired()])
    submit = SubmitField(label='Create Post')