from unittest import mock

from twit.api.conftest import token_header
from twit.users import User


@mock.patch("twit.api.users.users.create_user")
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


@mock.patch("twit.api.users.users.find_user")
def test_find_user(find_user, client):
    find_user.return_value = User(123, "name", "secret")

    response = client \
        .get("/users/name", headers=token_header("name")) \
        .get_json()

    assert response == {
        "id": 123,
        "name": "name",
        "password": "secret"
    }
