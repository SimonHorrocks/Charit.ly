import copy
from datetime import datetime

from flask import Blueprint, render_template
from sqlalchemy import desc
from geopy import distance

from app import db
from charity.forms import PostForm, SearchForm
from models import Post, User, Tag, Event

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
        new_post = Post(id=None, title=form.title.data, content=form.content.data, page="placeholder",
                        time_created=time)

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


# returns json list of all events within a certain distance of the coords
@charity_blueprint.route('/<string:coords>/<int:threshold>/nearby')
def nearby(coords, threshold):
    lon, lat = filter(float, coords.split(":"))
    return list(filter(lambda event: distance.distance((event.lat, event.lon), (lat, lon)).miles < threshold, Event.query.all()))


@charity_blueprint.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        search_text = form.search.data.strip()
        charity = User.query.filter_by(username=search_text, roleID="charity").first()
        words = search_text.split(" ")
        search_tags = []
        for word in words:
            for tag in Tag.query.filter_by(subject=word).all():
                search_tags.append(tag)

        charities = [tag.users.filter_by(roleID="charity").first() for tag in search_tags]
        results = list(filter(lambda x: x is not None, [charity] + charities))

    return render_template('search.html', form=form, results=results)
