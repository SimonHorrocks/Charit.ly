from datetime import datetime
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
    comments = db.relationship('Comment', backref='commentor')

    def __init__(self, username, email, password, roleID):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.roleID = roleID
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None

    def __repr__(self):
        return f"User('{self.username})', '{self.email}' , '{self.roleID}')"


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    time_created = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='parent_page', lazy=True)
    # relationships
    tags = db.relationship('Tag', secondary='tags', lazy='subquery', backref=db.backref('pages', lazy=True))
    events = db.relationship('Event', backref='event_page', lazy=True)
    followers = db.relationship('User', secondary='following', lazy=True, backref='followed_pages')

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.time_created = datetime.now()

    def __repr__(self):
        return f"Page('{self.name})', '{self.description}' , '{len(self.followers)}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(100), nullable=False)
    content = db.Column(db.VARCHAR(100))
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Post('{self.title})', '{self.content}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    time_created = db.Column(db.DateTime)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, name, description, date, time, page, lat, lon):
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.time_created = datetime.now()
        self.page_id = page
        self.lat = lat
        self.lon = lon


# Tags for pages to help with searching, user interests etc.
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.Integer, db.ForeignKey(Post.id))
    original = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    replies = db.relationship('Comment')
    text = db.Column(db.String(100), nullable=False)

    @staticmethod
    def walk(comments, indent=0):
        for comment in comments:
            print(comment.text, indent)
            yield comment, indent
            if comment.replies:
                yield from Comment.walk(comment.replies, indent=indent+1)


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

following = db.Table('following',
                     db.Column('follower_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
                     db.Column('page_id', db.Integer, db.ForeignKey(Page.id), primary_key=True))


def init_db():
    db.drop_all()
    db.create_all()
    admin = User(username='admin',
                 email='admin@email.com',
                 password='Admin1!',
                 roleID='admin')
    db.session.add(admin)
    db.session.commit()
    user = User(username='user',
                 email='user@email.com',
                 password='Admin1!',
                 roleID='user')
    db.session.add(user)
    db.session.commit()
    user2 = User(username='user2',
                 email='user2@email.com',
                 password='Admin1!',
                 roleID='user')
    db.session.add(user2)
    db.session.commit()
    charity = User(username='charity',
                 email='charity@email.com',
                 password='Admin1!',
                 roleID='charity')
    db.session.add(charity)
    db.session.commit()
    charity2 = User(username='charity2',
                 email='charity2@email.com',
                 password='Admin1!',
                 roleID='charity')
    db.session.add(charity2)
    db.session.commit()