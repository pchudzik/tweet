from unittest import mock

import pytest

from twit.api.app import app
from twit.users import User, Follower


@mock.patch("twit.api.users.users.follow")
def test_follow(follow, jwt_mock, client):
    stub_user(jwt_mock, "john")
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


@mock.patch("twit.api.users.users.follow")
def test_raises_security_exception_when_following_invalid_user(follow, jwt_mock, client):
    stub_user(jwt_mock, "mark")
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name})

    assert response.status_code == 403


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture()
def jwt_mock():
    with mock.patch("twit.api.security.tokens.get_jwt_identity") as jwt_identity:
        yield jwt_identity


def stub_user(identity, user):
    identity.return_value = {
        "name": user
    }
