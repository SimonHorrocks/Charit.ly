from app import db
import datetime
from werkzeug.security import generate_password_hash


def init_db():
    db.drop_all()
    db.create_all()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User authentication information
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User information
    roleID = db.Column(db.String(100), nullable=False, default='user')
    pages = db.relationship('Page', backref='author', lazy=True)


    def __init__(self, username, email, password, roleID):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.roleID = roleID

    def __repr__(self):
        return f"User('{self.username})', '{self.email}' , '{self.roleID}')"


class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_created = db.Column(db.DateTime)
    followers = db.Column(db.Integer, nullable=False, default=0)

    posts = db.relationship('Post', backref='parent_page', lazy=True)

    def __repr__(self):
        return f"Page('{self.name})', '{self.description}' , '{self.followers}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(100), nullable=False)
    content = db.Column(db.VARCHAR(100))
    page = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Post('{self.title})', '{self.content}')"
