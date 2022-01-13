import logging
from functools import wraps

from flask import Flask, render_template, request
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

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
                                current_user.firstname,
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
    return render_template('index.html')


# EXPLORE PAGE VIEW
@app.route('/explore')
def explore():
    return render_template('explore.html')


# EVENT MAP PAGE VIEW
@app.route('/map')
def map():
    return render_template('map.html')


# PROFILE
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


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
    setup_app(app, db)
    app.run()
