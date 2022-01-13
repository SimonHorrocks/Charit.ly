# IMPORTS
import copy
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash
from app import db, requires_roles
from models import User

# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

user = User.query.first()


# VIEWS
# view admin homepage
@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')
