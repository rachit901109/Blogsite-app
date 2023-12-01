from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class Post_form(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    content = TextAreaField(label='Content', validators=[DataRequired()])
    submit = SubmitField(label='Create Post')


class Rate_post_form(FlaskForm):
    rating = SelectField(label='Rating', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
    submit = SubmitField(label='Rate Post')