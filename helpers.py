from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def setup_app(app, db):
    # setup login manager to handle user logins
    login_manager = LoginManager()
    # login view to redirect users to
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    # setup user loader (load user by id)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # TODO: test that this works since id field is UserID

    from auth.views import auth_blueprint
    from charity.views import charity_blueprint
    from admin.views import admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(charity_blueprint)
    app.register_blueprint(admin_blueprint)
