from unittest import mock

from twit.api.conftest import token_header
from twit.tokens import Credentials



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
