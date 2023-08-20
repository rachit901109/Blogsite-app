import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

"""
Flask-Login is a popular Flask extension that provides user session management and authentication functionalities. 
It simplifies the process of handling user logins, logouts, and user session management in a Flask application.
"""


app = Flask(__name__)

# Configuration variable used to secure data in application and protect against CSRF (Cross-Site Request Forgery) attacks. It is essential to set a random and secret key for the application.
app.config['SECRET_KEY'] = 'random123key'

"""
specifies the URI (Uniform Resource Identifier) for the database. 
In this case, it's set to a SQLite database named site.db. SQLite is a lightweight, file-based database engine 
that is often used for development and testing purposes. In production, you may use a different database like PostgreSQL or MySQL.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# create a db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

# flask mail config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('My_Mail_Add')
app.config['MAIL_PASSWORD'] = os.environ.get('My_Mail_Pass')
mail = Mail(app)


from blogsite import routes