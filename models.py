from sqlalchemy.orm import backref
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

from app import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    roleID = db.Column(db.String(100), nullable=False, default='user')
    pages = db.relationship('Page', backref='author', lazy=True)

    tags = db.relationship('Tag', secondary='interests', lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('{self.username})', '{self.email}' , '{self.role}')"

    def __init__(self, username, email, password, roleid):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.roleID = roleid


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    time_created = db.Column(db.DateTime)
    followers = db.Column(db.Integer, nullable=False, default=0)

    # relationships
    tags = db.relationship('Tag', secondary='tags', lazy='subquery', backref=db.backref('pages', lazy=True))
    posts = db.relationship('Post', backref='page', lazy=True)
    events = db.relationship('Post', backref='page', lazy=True)

    def __repr__(self):
        return f"Page('{self.name})', '{self.description}' , '{self.followers}')"

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.time_created = datetime.now()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(100), nullable=False)
    content = db.Column(db.VARCHAR(100))
    page = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Post('{self.title})', '{self.content}')"

    def __init__(self, title, content, page):
        self.title = title
        self.content = content
        self.post = page
        self.time_created = datetime.now()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    Page = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)


# Tags for pages to help with searching, user interests etc.
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), unique=True, nullable=False)


# Tree structure for comments
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.column(db.String(100), nullable=False)
    parent_id = db.Column(db.integer, db.ForeignKey('comment.id'))

    children = db.relationship('Comment', backref=backref('parent', remote_side=[id]))

# TODO: Add query to retrieve/add comments


# Junction table for tags and pages
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id), primary_key=True),
                db.Column('page_id', db.Integer, db.ForeignKey(Page.id), primary_key=True)
                )

# Junction table for tags and users
interests = db.Table('interests',
                     db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id), primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
                     )


def init_db():
    db.drop_all()
    db.create_all()
