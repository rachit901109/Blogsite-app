from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
# from blogsite.models import User
# from flask import current_app


class Recommendation_engine_form(FlaskForm):
    username = SelectField(label='Username')
    engine = SelectField(label='Engine', choices=[('content-based','Content Based'),('ibcf','Collaborative Filtering')])
    submit = SubmitField(label='Recommendation Engine')