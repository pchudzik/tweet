from unittest import mock

import pytest
from sqlalchemy.orm.exc import NoResultFound

from api import app
from users import User


@mock.patch("users.create_user")
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


@mock.patch("users.find_user")
def test_find_user(find_user, client):
    find_user.return_value = User(123, "name", "secret")

    response = client \
        .get("/users?name=name") \
        .get_json()

    assert response == {
        "id": 123,
        "name": "name",
        "password": "secret"
    }


@mock.patch("users.find_user")
def test_NoResultFound_error_handler(find_user, client):
    find_user.side_effect = NoResultFound()

    response = client.get("/users?name=non_existing")

    print(response)
    assert response.status_code == 404
    assert response.get_json() == {
        "message": "not found",
        "err": "()"
    }


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client
