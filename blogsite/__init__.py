from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blogsite.config import config

"""
Flask-Login is a popular Flask extension that provides user session management and authentication functionalities. 
It simplifies the process of handling user logins, logouts, and user session management in a Flask application.
"""


app = Flask(__name__)

# Configuration variable used to secure data in application and protect against CSRF (Cross-Site Request Forgery) attacks. 
# we can use object to configure our app
app.config.from_object(config)

"""
specifies the URI (Uniform Resource Identifier) for the database. 
In this case, it's set to a SQLite database named site.db. SQLite is a lightweight, file-based database engine 
that is often used for development and testing purposes. In production, you may use a different database like PostgreSQL or MySQL.
"""

# create a db instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'danger'


mail = Mail(app)


from blogsite.users.routes import users
from blogsite.posts.routes import posts
from blogsite.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)