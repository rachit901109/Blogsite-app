from datetime import datetime
from flask import current_app
from blogsite import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as sr
from sqlalchemy.ext.associationproxy import association_proxy  

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

saved_table = db.Table('saved_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"tag: {self.name}"

class post_ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False) 

    user = db.relationship('User', back_populates='rated_posts_association')
    post = db.relationship('Post', back_populates='rated_by_association')

    def __repr__(self):
        return f"rating_id: {self.id}, User: {self.user_id}, post_rated: {self.post_id}, value: {self.value}"   

# New Models for the database 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)   

    saved = db.relationship('Post', secondary="saved_table", backref='saved_by', lazy=True)

    rated_posts_association = db.relationship('post_ratings', back_populates='user')
    rated_posts = association_proxy("rated_posts_association", "post")

    @property
    def num_posts(self):
        return len(self.posts)
    
    def get_reset_token(self):
        s = sr(secret_key=current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id}, salt="email_confirmation")
    
    @staticmethod
    def verify_reset_token(token):
        s = sr(secret_key=current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,salt="email_confirmation",max_age=900)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"name: {self.username}, mail: {self.email}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    tags = db.relationship('Tag', secondary=post_tags, backref='posts', lazy=True)

    rated_by_association = db.relationship('post_ratings', back_populates='post')
    rated_by = association_proxy("rated_by_association", "user")

    @property
    def update_rating(self):
        return sum(item.value for item in self.rated_by_association)/len(self.rated_by_association)

    def __repr__(self):
        if len(self.tags)>0:
            return f"id: {self.id}, title: {self.title}, rating: {self.rating}, tags: {self.tags}"
        return f"id: {self.id}, title: {self.title}, rating: {self.rating}"
    