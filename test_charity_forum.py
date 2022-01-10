import pytest
from flask import session
from flask_login import current_user

from app import db, app
from helpers import setup_app
from models import User

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

