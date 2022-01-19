# IMPORTS
import logging

from flask_login import login_required, current_user
from flask import Blueprint, render_template, request
from sqlalchemy import asc

from admin.forms import RolesForm
from app import db, requires_roles
from models import User

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# VIEWS
# view admin homepage
@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    form = RolesForm()
    if form.validate_on_submit():
        # updates the role of a user with inputted email
        User.query.filter_by(email=form.email.data).update({"roleID": form.role.data})
        db.session.commit()
        # adds information about role change to the log
        logging.warning('SECURITY - Privilege Modification [%s, %s, %s, %s]', current_user.email, form.email.data, form.role.data, request.remote_addr)
    with open("charity_forum.log", "r") as f:  # open log file for reading
        content = f.read().splitlines()[-10:]  # read the last ten lines
        content.reverse()  # reverse them into order
    users = User.query.order_by(asc('username')).all()
    return render_template('admin.html', users=users, form=form, logs=content)
