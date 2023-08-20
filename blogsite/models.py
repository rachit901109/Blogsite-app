from datetime import datetime
from blogsite import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as sr


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


# Using flask_sqlalchemy which is a ORM-object relational mapper which allows us to use objects to access databases
# **flask_sqlalchemy** is a flask specific module
"""
This attribute defines a relationship between the User model and the Post model. 
It establishes a one-to-many relationship, as each user can have multiple posts. 
The backref parameter allows us to refer to the author of a post from the Post model using the attribute author.
In summary, the backref parameter in the db.relationship function creates a virtual attribute in the child model (Post model) 
that allows you to access the related parent model (User model) easily without defining an explicit column in the child model.
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)   

    def get_reset_token(self):
        s = sr(secret_key=app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id}, salt="email_confirmation")
    
    @staticmethod
    def verify_reset_token(token):
        s = sr(secret_key=app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,salt="email_confirmation",max_age=900)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Username:{self.username}\nEmail:{self.email}\nPfp:{self.img_file}"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}, {self.date_posted})"