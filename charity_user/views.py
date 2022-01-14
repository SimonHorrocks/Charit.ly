# IMPORTS

from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash
from sqlalchemy import asc

from app import db, requires_roles
from models import Page

# CONFIG
from charity_user.forms import NewCharityPage

charity_user_blueprint = Blueprint('charity_user', __name__, template_folder='templates')


# VIEWS
# view charity profile
@charity_user_blueprint.route('/charity_profile', methods=['GET', 'POST'])
@login_required
@requires_roles('charity')
def charity_profile():
    charities = Page.query.filter_by(user_id=current_user.id).order_by(asc('name')).all()
    return render_template('charityuser.html', charities=charities)


@charity_user_blueprint.route('/newcharity', methods=['GET', 'POST'])
@login_required
@requires_roles('charity')
def newCharity():
    form = NewCharityPage()
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.name.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if page:
            flash('Charity with this name already exists')
            return render_template("newcharity.html", form=form)

        # create a new user with the form data
        new_charity = Page(name=form.name.data,
                           description=form.description.data,
                           user_id=current_user.id,
                           )

        # add the new user to the database
        db.session.add(new_charity)
        db.session.commit()
        return charity_profile()

    return render_template('newcharity.html', form=form)
