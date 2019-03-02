from unittest import mock
import pytest
from src import users
from src.FiledMatcher import FieldMatcher


@mock.patch("src.users.sql_session")
def test_create_user(sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock

    users.create_user("name", "password")

    session_mock.add.assert_called_with(FieldMatcher(
        name="name",
        password="password"))


@mock.patch("src.users.sql_session")
def test_find_user(sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock
    with mock.patch('src.db.find_user') as find_user:
        find_user.side_effect = [users.User(1, "name", "password")]

        found = users.find_user("user login")

        assert found.id == 1
        assert found.name == "name"
        assert found.password == "password"


@pytest.fixture()
def session_mock():
    return mock.Mock()
