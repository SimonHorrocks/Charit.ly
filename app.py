import logging
from functools import wraps

from flask import Flask, render_template, request
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

from helpers import setup_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charityForum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def requires_roles(*roles):
    def wrapper(f):  # create wrapper
        @wraps(f)
        def wrapped(*args, **kwargs):  # wrap function to check the user's role
            if current_user.role not in roles:  # if the role is not in the list of roles required
                # log unauthorised access attempt
                logging.warning('SECURITY - Unauthorised access attempt [%s, %s, %s, %s]',
                                current_user.id,
                                current_user.firstname,
                                current_user.role,
                                request.remote_addr)
                # Redirect the user to an unauthorised notice!
                return render_template('403.html') # add 403 page
            return f(*args, **kwargs)

        return wrapped

    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/logout')
@login_required
def logout():
    return render_template('logout.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/search')
def search():
    return render_template('search.html')


if __name__ == '__main__':
    setup_app(app, db)
    app.run()
