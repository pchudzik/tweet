from unittest import mock
from src import users
from src.FiledMatcher import FieldMatcher


def test_create_user():
    with mock.patch('src.infrastructure.db.session') as session_mock:
        users.create_user("name", "password")

        session_mock.add.assert_called_with(FieldMatcher(
            name="name",
            password="password"))


def test_find_user():
    with mock.patch('src.db.find_user') as find_user:
        find_user.side_effect = [users.User(1, "name", "password")]

        found = users.find_user("user login")

        assert found.id == 1
        assert found.name == "name"
        assert found.password == "password"
