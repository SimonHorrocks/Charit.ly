# IMPORTS
import copy
from flask_login import login_required
from flask import Blueprint, render_template
from sqlalchemy import asc

from admin.forms import RolesForm
from app import db, requires_roles
from models import User

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# VIEWS
# view admin homepage
@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    form = RolesForm()
    if form.validate_on_submit():
        User.query.filter_by(email=form.email.data).update({"roleID": form.role.data})
        db.session.commit()
    users = User.query.order_by(asc('username')).all()
    return render_template('admin.html', users=users, form=form)
