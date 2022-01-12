import datetime

import pytest
from flask_login import current_user

from app import db, app
from helpers import setup_app
from models import User, Tag, Event, Page

db.drop_all()

setup_app(app, db)
app.config["WTF_CSRF_ENABLED"] = False
app.config["TESTING"] = True


@pytest.fixture
def client():
    db.create_all()

    with app.test_client() as client:
        with app.app_context():
            yield client

    db.drop_all()


def create_test_user(role):
    test_user = User(email="test@email.com",
                     username="test",
                     password="Password1!",
                     roleID=role)
    db.session.add(test_user)
    db.session.commit()
    return test_user


def test_register(client):
    client.post("/register", data=dict(username="test", email="test@email.com", password="Password1!",
                                       confirm_password="Password1!"))
    assert User.query.filter_by(username="test").first() is not None


def test_login_and_logout(client):
    test_user = create_test_user("user")
    client.post("/login", data=dict(email="test@email.com", password="Password1!"))
    assert current_user == test_user
    client.get("/logout")
    assert current_user != test_user


def test_login_attempts(client):
    test_user = create_test_user("user")
    for _ in range(3):
        response = client.post("/login", data=dict(email="test@email.com", password="Password2!"))
    assert "Number of incorrect logins exceeded" in response.data.decode("utf-8")


def test_search(client):
    response = client.post("/search", data=dict(search="anything"))
    assert "No results." in response.data.decode("utf-8")
    test_charity = create_test_user("charity")
    response = client.post("/search", data=dict(search="test"))
    assert test_charity.username in response.data.decode("utf-8")
    test_tag = Tag(subject="foo")
    tagged_charity = User(email="tagged@email.com",
                          username="tagged",
                          password="Password1!",
                          roleID="charity")
    tagged_charity.tags.append(test_tag)
    db.session.add(test_tag)
    db.session.add(tagged_charity)
    db.session.commit()
    response = client.post("/search", data=dict(search="foo"))
    assert tagged_charity.username in response.data.decode("utf-8")


def test_nearby(client): # integrity error here for some reason
    test_user = create_test_user("charity")
    test_page = Page(name="test_page",
                     description="a test page for testing purposes",
                     user_id=test_user.id)
    test_event = Event(name="test_event",
                       description="a test event for testing purposes",
                       time=datetime.datetime.fromisoformat("2022-01-01 19:00"),
                       page=test_page.id,
                       lat=5,
                       lon=5)
    db.session.add(test_user)
    db.session.add(test_page)
    db.session.add(test_event)
    db.session.commit()
