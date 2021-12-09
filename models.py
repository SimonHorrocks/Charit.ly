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
    PageOwner = db.Column(db.Integer, nullable=False)
    TimeCreated = db.Column(db.DateTime)
    Followers = db.Column(db.Integer, nullable=False, default=0)

class Post(db.Model):
    __tablename__ = 'Post'

    PostID = db.column(db.Integer, primary_key=True)
    PostTitle = db.Column(db.VARCHAR(100), nullable=False)
    PostContent = db.Column(db.VARCHAR(100))
    Page = db.column(db.Integer, nullable=False)
    TimeCreated = db.Column(db.DateTime)

class Event(db.Model):
    __tablename__ = 'Event'

    EventID = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.VARCHAR(100))
    EventDescription = db.Column(db.VARCHAR(100))
    EventTime = db.Column(db.VARCHAR(100))
    TimeCreated = db.Column(db.VARCHAR(100))
    Page = db.column(db.Intger)
    EventLocation = db.Column(db.VARCHAR(100))

class Follows(db.Model):
    __tablename__ = 'Follows'

    UserID = db.column(db.Integer)
    PageID = db.column(db.Integer)

class Attending(db.Model):
    __tablename__ = 'Attending'

    UserID = db.column(db.Integer)
    EventID = db.column(db.Integer)



