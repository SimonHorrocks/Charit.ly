import copy
from datetime import datetime

from flask import Blueprint, render_template
from sqlalchemy import desc
from app import db
from charity.forms import PostForm
from models import Post

charity_blueprint = Blueprint("charity", __name__, template_folder="templates")

# TODO: fix blueprint not working for update and delete pages
@charity_blueprint.route('/blog')
def blog():
    posts = Post.query.order_by(desc('id')).all()
    return render_template('charity_profile.html', posts=posts)


@charity_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = PostForm()

    if form.validate_on_submit():
        time = datetime.now()
        new_post = Post(id=None, title=form.title.data, content=form.content.data, page="placeholder", time_created=time)

        db.session.add(new_post)
        db.session.commit()

        return blog()
    return render_template('create.html', form=form)


@charity_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return render_template('500.html')

    form = PostForm()

    if form.validate_on_submit():
        Post.query.filter_by(id=id).update({"title": form.title.data})
        Post.query.filter_by(id=id).update({"content": form.content.data})

        db.session.commit()

        return blog()

        # creates a copy of post object which is independent of database.
    post_copy = copy.deepcopy(post)

    # set update form with title and body of copied post object
    form.title.data = post_copy.title
    form.content.data = post_copy.content

    return render_template('update.html', form=form)

@charity_blueprint.route('/<int:id>/delete')
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return blog()