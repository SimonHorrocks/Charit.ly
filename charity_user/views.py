# IMPORTS

from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash

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
    return render_template('charity_user.html', pages=current_user.pages)


@charity_user_blueprint.route('/newcharity', methods=['GET', 'POST'])
@login_required
@requires_roles('charity')
def new_charity():
    form = NewCharityPage()
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.name.data).first()
        # if this returns a page, then the name already exists in database

        # if name already exists redirect user back to new charity page with error message so user can try again
        if page:
            flash('Charity with this name already exists')
            return render_template("new_charity.html", form=form)

        # create a new page with the form data
        new_charity = Page(name=form.name.data,
                           description=form.description.data,
                           user_id=current_user.id,
                           )

        # add the new page to the database
        db.session.add(new_charity)
        db.session.commit()
        return charity_profile()

    return render_template('new_charity.html', form=form)
