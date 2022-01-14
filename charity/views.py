import copy
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from geopy import distance
from sqlalchemy import desc

from app import db, requires_roles
from charity.forms import PostForm, SearchForm, NewEventForm, TagForm
from models import Page, tags
from models import Post, Tag, Event

charity_blueprint = Blueprint("charity", __name__, template_folder="templates")


# TODO: fix blueprint not working for update and delete pages
@charity_blueprint.route('/<int:id>/page', methods=['GET', 'POST'])
def page(id):
    form = NewEventForm()
    charity_page = Page.query.get(id)
    return render_template('charity_page.html', posts=charity_page.posts, form=form, page=charity_page,
                           add_tag_form=TagForm(), remove_tag_form=TagForm())


@charity_blueprint.route('/<int:page_id>/create', methods=('GET', 'POST'))
def create(page_id):
    form = PostForm()

    if form.validate_on_submit():
        time = datetime.now()
        new_post = Post(title=form.title.data, content=form.content.data, page=page_id,
                        time_created=time)

        db.session.add(new_post)
        db.session.commit()

        return page(page_id)
    return render_template('create.html', form=form)


@charity_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return render_template('500.html')

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()

        return page(post.page)

        # creates a copy of post object which is independent of database.
    post_copy = copy.deepcopy(post)

    # set update form with title and body of copied post object
    form.title.data = post_copy.title
    form.content.data = post_copy.content

    return render_template('update.html', form=form)


@charity_blueprint.route('/<int:id>/delete')
def delete(id):
    post = Post.query.filter_by(id=id).first()
    page_id = post.page
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return page(page_id)


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
            for tag_page in tag.pages:
                charities.append(tag_page)

        # Create final list of results
        results = list(filter(lambda x: x is not None, [charity] + charities))

    return render_template('search.html', form=form, results=results)


@charity_blueprint.route("/<int:page_id>/tag", methods=["POST"])
@requires_roles("charity")
def add_tag(page_id):
    form = TagForm()

    if form.validate_on_submit:
        tag = Tag.query.filter_by(subject=form.subject.data).first()
        if not tag:
            tag = Tag(subject=form.subject.data)
            db.session.add(tag)
            db.session.commit()
        current_page = Page.query.get(page_id)
        current_page.tags.append(tag)
        db.session.commit()

    return redirect(url_for("charity.page", id=page_id))


@charity_blueprint.route("/<int:page_id>/removetag", methods=["POST"])
@requires_roles("charity")
def remove_tag(page_id):
    form = TagForm()

    if form.validate_on_submit:
        tag = Tag.query.filter_by(subject=form.subject.data).first()
        current_page = Page.query.get(page_id)
        current_page.tags.remove(tag)
        db.session.commit()

    return redirect(url_for("charity.page", id=page_id))
