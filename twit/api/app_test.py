from unittest import mock

import pytest
from sqlalchemy.orm.exc import NoResultFound

from twit.api.app import app


@mock.patch("twit.api.users.users.find_user")
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
