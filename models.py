from app import db


def init_db():
    db.drop_all()
    db.create_all()


class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(30), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(100), nullable=False)
    RoleID = db.Column(db.String(100), nullable=False)
    EncryptionKey = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password, roleid, encryptionkey):
        self.Username = username
        self.Email = email
        self.Password = password
        self.RoleID = roleid
        self.EncryptionKey = encryptionkey


class Page(db.Model):
    __tablename__ = 'Page'

    PageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PageName = db.Column(db.VARCHAR(100), nullable=False)
    PageDescription = db.Column(db.TEXT)
    PageOwner = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    TimeCreated = db.Column(db.DateTime)
    Followers = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, pagename, pagedescription, pageowner, timecreated, followers):
        self.PageName = pagename
        self.PageDescription = pagedescription
        self.PageOwner = pageowner
        self.TimeCreated = timecreated
        self.Followers = followers


class Post(db.Model):
    __tablename__ = 'Post'

    PostID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PostTitle = db.Column(db.VARCHAR(100), nullable=False)
    PostContent = db.Column(db.VARCHAR(100))
    Page = db.Column(db.Integer, db.ForeignKey('Page.PageID'))
    TimeCreated = db.Column(db.DateTime)

    def __init__(self, posttitle, postcontent, page, timecreated):
        self.PostTitle = posttitle
        self.PostContent = postcontent
        self.Page = page
        self.TimeCreated = timecreated


class Event(db.Model):
    __tablename__ = 'Event'

    EventID = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.VARCHAR(100))
    EventDescription = db.Column(db.VARCHAR(100))
    EventTime = db.Column(db.VARCHAR(100))
    TimeCreated = db.Column(db.VARCHAR(100))
    Page = db.Column(db.Integer, db.ForeignKey('Page.PageID'))
    EventLocation = db.Column(db.VARCHAR(100))

    def __init__(self, eventname, eventdescription, eventtime, timecreated, page, eventlocation):
        self.EventName = eventname
        self.EventDescription = eventdescription
        self.EventTime = eventtime
        self.TimeCreated = timecreated
        self.Page = page
        self.EventLocation = eventlocation


class Interest(db.Model):
    __tablename__ = 'Interest'

    InterestID = db.Column(db.Integer, primary_key=True)
    Interest = db.Column(db.VARCHAR(100))

    def __init__(self, interest):
        self.Interest = interest


# Many to Many Relationships
Follows = db.table('Follows',
                   db.Column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                   db.Column('PageID', db.Integer, db.ForeignKey('Page.PageID'), primary_key=True)
                   )

Attending = db.table('Attending',
                     db.Column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                     db.Column('EventID', db.Integer, db.ForeignKey('Event.EventID'), primary_key=True)
                     )

UserInterest = db.table('UserInterest',
                        db.Column('UserID', db.Integer, db.ForeignKey('User.UserID'), primary_key=True),
                        db.Column('InterestID', db.Integer, db.ForeignKey('Interest.InterestID'), primary_key=True)
                        )
