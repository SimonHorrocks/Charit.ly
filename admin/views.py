# IMPORTS
import copy
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash
from sqlalchemy import asc

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
    users = User.query.order_by(asc('username')).all()
    return render_template('admin.html', users=users)
