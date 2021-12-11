
from app import db


class User(db.Model):
    __tablename__ = 'User'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(30), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(100), nullable=False)
    RoleID = db.Column(db.String(100), nullable=False)
    EncryptionKey = db.Column(db.String(100), nullable=False)


class Page(db.Model):
    __tablename__ = 'Page'

    PageID = db.Column(db.Integer, primary_key=True)
    PageName = db.Column(db.VARCHAR(100), nullable=False)
    PageDescription = db.Column(db.TEXT)
    PageOwner = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    TimeCreated = db.Column(db.DateTime)
    Followers = db.Column(db.Integer, nullable=False, default=0)


class Post(db.Model):
    __tablename__ = 'Post'

    PostID = db.column(db.Integer, primary_key=True)
    PostTitle = db.Column(db.VARCHAR(100), nullable=False)
    PostContent = db.Column(db.VARCHAR(100))
    Page = db.column(db.Integer, db.ForeignKey('Page.PageID'))
    TimeCreated = db.Column(db.DateTime)


class Event(db.Model):
    __tablename__ = 'Event'

    EventID = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.VARCHAR(100))
    EventDescription = db.Column(db.VARCHAR(100))
    EventTime = db.Column(db.VARCHAR(100))
    TimeCreated = db.Column(db.VARCHAR(100))
    Page = db.column(db.Integer, db.ForeignKey('Page.PageID'))
    EventLocation = db.Column(db.VARCHAR(100))


class Interest(db.Model):
    __tablename__ = 'Interest'

    InterestID = db.column(db.Integer, primary_key=True)
    Interest = db.column(db.VARCHAR(100))


# Many to Many Relationships
Follows = db.table('Follows',
                   db.column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                   db.column('PageID', db.Integer, db.ForeignKey('Page.PageID'), primary_key=True)
                   )

Attending = db.table('Attending',
                     db.column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                     db.column('EventID', db.Integer, db.ForeignKey('Event.EventID'), primary_key=True)
                     )

UserInterest = db.table('UserInterest',
                        db.column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                        db.column('InterestID', db.Integer, db.ForeignKey('Interest.InterestID'), primary_key=True)
                        )
