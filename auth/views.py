import logging
from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app import db
from auth.forms import RegisterForm, LoginForm
from models import User

auth_blueprint = Blueprint("auth", __name__, template_folder="templates")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    # if request method is POST and form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template("register.html", form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        roleID="user")

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # log user registration
        logging.warning("SECURITY - User registration [%s, %s]", form.email.data, request.remote_addr)

        # sends user to login page
        return redirect(url_for("auth.login"))
    # if request method is GET or form not valid re-render signup page
    return render_template("register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # create login form object
    form = LoginForm()

    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    # if request method is POST and form is valid
    if form.validate_on_submit():
        # increment the number of login attempts
        session['logins'] += 1
        # query for the user who matches the given email
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            elif session['logins'] == 1:
                flash('Please check your login details and try again. 2 login attempts remaining')
            # log the invalid login attempt
            logging.warning('SECURITY - Invalid Log in attempt [%s, %s]', form.email.data,
                            request.remote_addr)
        else:
            # reset login attempts
            session['logins'] = 0
            # log the user in with the flask login manager
            login_user(user, force=True)
            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
            # log successful login attempt
            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.email,
                            request.remote_addr)

            if user.roleID == 'admin':
                # if user is admin redirect to admin page
                return redirect(url_for('admin.admin'))
            else:
                # otherwise redirect to profile
                return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    # log user logout
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    # logout the user from the flask login manager
    logout_user()
    # redirect to the home page
    return redirect(url_for('index'))
