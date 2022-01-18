import logging
from functools import wraps

from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from helpers import setup_app

# CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charityForum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy(app)


# RBAC FUNCTION
def requires_roles(*roles):
    def wrapper(f):  # create wrapper
        @wraps(f)
        def wrapped(*args, **kwargs):  # wrap function to check the user's role
            if current_user.roleID not in roles:  # if the role is not in the list of roles required
                # log unauthorised access attempt
                logging.warning('SECURITY - Unauthorised access attempt [%s, %s, %s, %s]',
                                current_user.id,
                                current_user.username,
                                current_user.roleID,
                                request.remote_addr)
                # Redirect the user to an unauthorised notice!
                return render_template('403.html')  # add 403 page
            return f(*args, **kwargs)

        return wrapped

    return wrapper


# HOME PAGE VIEW
@app.route('/')
def index():
    posts = []
    if current_user.is_authenticated:
        for page in current_user.followed_pages:
            posts = posts + page.posts
        posts.sort(key=lambda p: p.time_created)
    return render_template('index.html', posts=posts)


# EXPLORE PAGE VIEW
@app.route('/explore')
def explore():
    from models import Page, Post, Event
    charities = Page.query.order_by(desc("id")).all()
    posts = Post.query.order_by(desc("id")).all()
    events = Event.query.order_by(desc("id")).all()
    return render_template('explore.html', posts=posts, charities=charities, events=events)


# EVENT MAP PAGE VIEW
@app.route('/map')
def map():
    return render_template('map.html')


# ERROR PAGE VIEWS
@app.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # LOGGING, don't include in setup so tests don't save logs
    # filter for logging security issues
    class SecurityFilter(logging.Filter):
        def filter(self, record):
            return "SECURITY" in record.getMessage()


    # filter for logging everything else
    class ConsoleFilter(logging.Filter):
        def filter(self, record):
            return "SECURITY" not in record.getMessage()


    # create file handler to log security messages to file
    fh = logging.FileHandler('charity_forum.log', mode='w')
    fh.setLevel(logging.WARNING)
    fh.addFilter(SecurityFilter())
    fh_formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
    fh.setFormatter(fh_formatter)

    # create stream handler to log non security messages to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.addFilter(ConsoleFilter())
    ch_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(ch_formatter)

    # add handlers to root logger
    logger = logging.getLogger()
    logger.addHandler(fh)
    logger.addHandler(ch)
    # stop handler messages being sent to root logger
    logger.propagate = False

    setup_app(app, db)
    app.run()
