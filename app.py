from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/search')
def search():
    return render_template('search.html')


if __name__ == '__main__':
    # setup login manager to handle user logins
    login_manager = LoginManager()
    # login view to redirect users to
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    # setup user loader (load user by id)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # TODO: test that this works since id field is UserID

    from auth.views import auth_blueprint
    from charity.views import charity_blueprint

    app.register_blueprint(charity_blueprint)
    app.register_blueprint(auth_blueprint)

    app.run()
