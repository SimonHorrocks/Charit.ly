from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    roleID = db.Column(db.String(100), nullable=False, default='user')
    pages = db.relationship('Page', backref='author', lazy=True)

    tags = db.relationship('Tag', secondary='interests', lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('{self.username})', '{self.email}' , '{self.roleID}')"


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_created = db.Column(db.DateTime)
    followers = db.Column(db.Integer, nullable=False, default=0)

    # relationships
    tags = db.relationship('Tag', secondary='tags', lazy='subquery', backref=db.backref('pages', lazy=True))
    posts = db.relationship('Post', backref='page', lazy=True)
    events = db.relationship('Post', backref='page', lazy=True)

    def __repr__(self):
        return f"Page('{self.name})', '{self.description}' , '{self.followers}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(100), nullable=False)
    content = db.Column(db.VARCHAR(100))
    page = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    time_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"Post('{self.title})', '{self.content}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    time_created = db.Column(db.DateTime)
    Page = db.Column(db.Integer, db.ForeignKey(Page.id), nullable=False)
    location = db.Column(db.String(100))


# Tags for pages to help with searching, user interests etc.
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
