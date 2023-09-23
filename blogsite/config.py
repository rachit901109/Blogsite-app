import os

class config():
    SECRET_KEY = 'random123key'
    """
    specifies the URI (Uniform Resource Identifier) for the database. 
    In this case, it's set to a SQLite database named site.db. SQLite is a lightweight, file-based database engine 
    that is often used for development and testing purposes. In production, you may use a different database like PostgreSQL or MySQL.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_model.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('My_Mail_Add')
    MAIL_PASSWORD = os.environ.get('My_Mail_Pass')