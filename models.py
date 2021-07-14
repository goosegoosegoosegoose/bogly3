"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

now = datetime.datetime.now()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)

    last_name = db.Column(db.String(50),
                           nullable=True,
                           unique=False)

    image_url = db.Column(db.Text(),
                          nullable=False,
                          unique=False,
                          default="https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-256x256.jpg")

    post = db.relationship('Post')

# can't get default to work with users made with new user form on frontend

class Post(db.Model):
    """Post""" 

    __tablename__="posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    content = db.Column(db.Text(), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, unique=False, default=f'{now}')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    
    user = db.relationship('User')
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    unique_tags = db.relationship('PostTag', backref='posts')

class Tag(db.Model):
    """Tag"""

    __tablename__="tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    unique_tags = db.relationship('PostTag', backref='tags')

class PostTag(db.Model):
    """Links post and tag"""

    __tablename__="post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

