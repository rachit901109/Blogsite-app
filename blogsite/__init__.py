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

# create a db instance
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'

mail = Mail()


def create_app(config_class = config):
    app = Flask(__name__)

    # Configuration variable used to secure data in application and protect against CSRF (Cross-Site Request Forgery) attacks. 
    # we can use object to configure our app
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from blogsite.users.routes import users
    from blogsite.posts.routes import posts
    from blogsite.main.routes import main
    from blogsite.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app