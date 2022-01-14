import copy
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from geopy import distance
from sqlalchemy import desc

from app import db
from charity.forms import PostForm, SearchForm, NewEventForm
from models import Page
from models import Post, Tag, Event

charity_blueprint = Blueprint("charity", __name__, template_folder="templates")


@charity_blueprint.route('/<string:name>/blog',  methods=['GET', 'POST'])
def blog(name):
    form = NewEventForm()
    page = Page.query.filter_by(user_id=current_user.id).first()
    # if request method is POST and form is valid
    if form.validate_on_submit():
        # create a new user with the form data
        new_event = Event(name=form.name.data,
                          description=form.description.data,
                          date=form.date.data,
                          time=form.time.data,
                          page=page.id,
                          lat=form.lat.data,
                          lon=form.lon.data)
        # add the new user to the database
        db.session.add(new_event)
        db.session.commit()

    posts = Post.query.filter_by(page=page.id).order_by(desc('id')).all()
    return render_template('charity_profile.html', posts=posts, form=form)


@charity_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = PostForm()
    page = Page.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        time = datetime.now()
        new_post = Post(id=None, title=form.title.data, content=form.content.data, page=page.id,
                        time_created=time)

        db.session.add(new_post)
        db.session.commit()

        return blog(name=page.name)
    return render_template('create.html', form=form)


@charity_blueprint.route('/<string:name>/<int:id>/update', methods=('GET', 'POST'))
def update(name, id):
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


@charity_blueprint.route('/<string:name>/<int:id>/delete')
def delete(name, id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return blog(name)


@charity_blueprint.route('/<int:id>/view')
def view(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post.html', post=post)


# returns json list of all events within a certain distance of the coords
@charity_blueprint.route('/<string:coords>/<int:threshold>/nearby')
def nearby(coords, threshold):
    lon, lat = map(float, coords.split(":"))
    events = list(filter(lambda event: distance.distance((event.lat, event.lon), (lat, lon)).miles < threshold,
                         Event.query.all()))
    return {"events": list(
        map(lambda event: {"id": event.id, "name": event.name, "lat": event.lat, "lon": event.lon}, events))}


# Takes user search query, searches for a charity with a matching name, and charities with matching tags.
@charity_blueprint.route('/search', methods=["GET", "POST"])
def search():
    # Create search form
    form = SearchForm()
    # Initialise list of results
    results = []

    # If request method is POST or form is valid
    if form.validate_on_submit():
        # Removes whitespace at the beginning and end of search query
        search_text = form.search.data.strip()

        # Query database for charities with a matching username
        charity = Page.query.filter_by(name=search_text).first()
        # split search text into individual words

        words = search_text.split(" ")
        # Initialise list of tags
        search_tags = []
        for word in words:
            for tag in Tag.query.filter_by(subject=word).all():
                # If a word in the search query matches an existing tag, then add the tag to the list
                search_tags.append(tag)

        # Get list of charities with tags matching those in the list
        charities = []
        for tag in search_tags:
            for page in tag.pages:
                charities.append(page)

        # Create final list of results
        results = list(filter(lambda x: x is not None, [charity] + charities))

    return render_template('search.html', form=form, results=results)
