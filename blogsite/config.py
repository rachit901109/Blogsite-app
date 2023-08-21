import os

class config():
    SECRET_KEY = 'random123key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('My_Mail_Add')
    MAIL_PASSWORD = os.environ.get('My_Mail_Pass')