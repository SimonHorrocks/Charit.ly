import socket

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from users.forms import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://csc2033_team13:LashFain;own@localhost:420693306/csc1033_team13'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


# Blueprints were not working for me so I put the registration form here for now
# TODO: add blueprints for register and login forms
@app.route('/register')
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return login()

    return render_template('register.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


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
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app.run(host=my_host, port=free_port, debug=True)
