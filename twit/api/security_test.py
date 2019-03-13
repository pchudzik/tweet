from unittest import mock

import pytest

from twit.api.app import app
from twit.infrastructure import jwt
from twit.tokens import refresh_token, Credentials
from twit.users import User


@jwt.token_in_blacklist_loader
def token_blacklist(*args):
    return False


@mock.patch("twit.api.security.get_raw_jwt")
@mock.patch("twit.api.security.tokens")
def test_logout(tokens_mock, get_raw_jwt_mock, client):
    get_raw_jwt_mock.return_value = {"jti": "some jti"}

    response = client.post("/logout", headers=token_header())

    assert response.status_code == 204
    tokens_mock.revoke.assert_called_with("some jti")


@mock.patch("twit.api.users.users.login")
def test_invalid_login(login_mock, client):
    login_mock.return_value = None

    response = client \
        .post("/login", json={"login": "john", "password": "secret"})

    assert response.status_code == 401
    assert response.get_json() == {
        "message": "Invalid credentials"
    }


@mock.patch("twit.api.users.users.login")
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


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def token_header(user_login="any_user"):
    user = User(1, user_login, "any password")
    with app.test_request_context():
        token = refresh_token(user).token
    return {
        "Authorization": f"Bearer {token}"
    }
