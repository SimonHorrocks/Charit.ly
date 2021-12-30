import logging

from flask import Blueprint, redirect, url_for, render_template, flash, request

from app import db
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
                        roleid="user")

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
    pass


@auth_blueprint.route("/logout")
def logout():
    pass
