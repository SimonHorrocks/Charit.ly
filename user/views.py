# IMPORTS

from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash, redirect, url_for

import app
from app import db, requires_roles
from models import Page, User
from user.forms import NameForm

user_blueprint = Blueprint('user', __name__, template_folder='templates')


# PROFILE
@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@requires_roles('user')
def profile():
    return render_template('profile.html', change_name_form=NameForm())


@user_blueprint.route("/user_change_name", methods=["POST"])
@requires_roles("user")
def change_name():
    form = NameForm()
    if form.validate_on_submit:
        User.query.filter_by(id=current_user.id).update({"username": form.name.data})
        db.session.commit()

    return redirect(url_for("user.profile"))
