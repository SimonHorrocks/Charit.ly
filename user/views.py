# IMPORTS

from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash

import app
from app import db, requires_roles
from models import Page


user_blueprint = Blueprint('user', __name__, template_folder='templates')


# PROFILE
@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@requires_roles('user')
def profile():
    return render_template('profile.html')

