import pytest
from unittest import mock
import users
from FiledMatcher import FieldMatcher


def test_create_user(session_mock):
    with mock.patch('db.Session', return_value=session_mock):
        users.create_user("name", "password")

        session_mock.add.assert_called_with(FieldMatcher(
            name="name",
            password="password"))


def test_find_user():
    with mock.patch('db.find_user') as find_user:
        find_user.side_effect = [users.User(1, "name", "password")]

        found = users.find_user("user login")

        assert found.id == 1
        assert found.name == "name"
        assert found.password == "password"


@pytest.fixture()
def session_mock():
    return mock.Mock()
