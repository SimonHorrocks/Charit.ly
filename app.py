from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://csc2033_team13:LashFain;own@localhost:42069:3306/csc1033_team13'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

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

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
