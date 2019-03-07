from unittest import mock

import pytest
from sqlalchemy.orm.exc import NoResultFound

from src.api import app
from src.users import User, Follower, Credentials
from src.tweets import Tweet


@mock.patch("src.users.create_user")
def test_create_user(create_user, client):
    create_user.return_value = User(123, "created", "secret")

    response = client \
        .post("/users", json={"name": "name", "password": "password"}) \
        .get_json()

    assert response == {
        "id": 123,
        "name": "created",
        "password": "secret"
    }

    create_user.assert_called_once_with("name", "password")


@mock.patch("src.users.find_user")
def test_find_user(find_user, client):
    find_user.return_value = User(123, "name", "secret")

    response = client \
        .get("/users/name") \
        .get_json()

    assert response == {
        "id": 123,
        "name": "name",
        "password": "secret"
    }


@mock.patch("src.tweets.create_tweet")
def test_create_tweet(create_tweet, client):
    login = "john"
    content = "content"
    create_tweet.return_value = Tweet(123, login, content)

    response = client \
        .post(f"/users/{login}/tweets", json={"content": content}) \
        .get_json()

    assert response == {
        "id": 123,
        "user": login,
        "content": content
    }


@mock.patch("src.tweets.find_tweets")
def test_find_tweet(find_tweets, client):
    login = "john"
    content = "content"
    find_tweets.return_value = [
        Tweet(123, login, content + "1"),
        Tweet(321, login, content + "2")]

    response = client \
        .get(f"/users/{login}/tweets") \
        .get_json()

    assert response == [{
        "id": 123,
        "user": login,
        "content": content + "1"
    }, {
        "id": 321,
        "user": login,
        "content": content + "2"
    }]


@mock.patch("src.api.users.follow")
def test_follow(follow, client):
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name}) \
        .get_json()

    assert response == {
        "id": 1,
        "user": 1,
        "follower": 2
    }


@mock.patch("src.api.users.login")
def test_login(login_mock, client):
    login_mock.return_value = Credentials("secret_token", "refresh_token")

    response = client \
        .post("/login", json={"login": "john", "password": "secret"}) \
        .get_json()

    login_mock.assert_called_with("john", "secret")
    assert response == {
        "token": "secret_token",
        "refresh_token": "refresh_token"
    }


@mock.patch("src.api.get_raw_jwt")
@mock.patch("src.api.tokens")
def test_logout(tokens_mock, get_raw_jwt_mock, client):
    get_raw_jwt_mock.return_value = {"jti": "some jti"}

    response = client.post("/logout")

    assert response.status_code == 204
    tokens_mock.revoke.assert_called_with("some jti")


@mock.patch("src.api.users.login")
def test_invalid_login(login_mock, client):
    login_mock.return_value = None

    response = client \
        .post("/login", json={"login": "john", "password": "secret"})

    assert response.status_code == 401
    assert response.get_json() == {
        "message": "Invalid credentials"
    }


@mock.patch("src.users.find_user")
def test_NoResultFound_error_handler(find_user, client):
    find_user.side_effect = NoResultFound()

    response = client.get("/users/non_existing")

    assert response.status_code == 404
    assert response.get_json() == {
        "message": "not found",
        "err": "()"
    }


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client
