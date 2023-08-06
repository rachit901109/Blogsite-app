from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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

from blogsite import routes