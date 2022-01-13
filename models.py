import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User authentication information
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User activity information
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    # User information
    roleID = db.Column(db.String(100), nullable=False, default='user')
    pages = db.relationship('Page', backref='author', lazy=True)
    tags = db.relationship('Tag', secondary='interests', lazy='subquery', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, password, roleID):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.roleID = roleID
        self.registered_on = datetime.datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

    def __repr__(self):
        return f"User('{self.username})', '{self.email}' , '{self.roleID}')"


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    time_created = db.Column(db.DateTime)
    followers = db.Column(db.Integer, nullable=False, default=0)

    posts = db.relationship('Post', backref='parent_page', lazy=True)
    # relationships
    tags = db.relationship('Tag', secondary='tags', lazy='subquery', backref=db.backref('pages', lazy=True))
    events = db.relationship('Event', backref='event_page', lazy=True)

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.time_created = datetime.datetime.now()

    def __repr__(self):
        return f"Page('{self.name})', '{self.description}' , '{self.followers}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(100), nullable=False)
    content = db.Column(db.VARCHAR(100))
    page = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Post('{self.title})', '{self.content}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    page = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, name, description, time, page, lat, lon):
        self.name = name
        self.description = description
        self.time = time
        self.time_created = datetime.datetime.now()
        self.page = page
        self.lat = lat
        self.lon = lon


# Tags for pages to help with searching, user interests etc.
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(100), unique=True, nullable=False)


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
    admin = User(username='admin',
                 email='admin@email.com',
                 password='Admin1!',
                 roleID='admin')
    db.session.add(admin)
    db.session.commit()
