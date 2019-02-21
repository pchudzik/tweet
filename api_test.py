from unittest import mock

import pytest

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


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client
