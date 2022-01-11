from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from helpers import setup_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charityForum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    setup_app(app, db)
    app.run()
