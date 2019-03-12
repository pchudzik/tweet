from unittest import mock
import pytest
import twit.db as db
from twit import users
from twit.tokens import Credentials
from twit.FiledMatcher import FieldMatcher


@mock.patch("twit.users.sql_session")
def test_create_user(sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock

    users.create_user("name", "password")

    session_mock.add.assert_called_with(FieldMatcher(
        name="name",
        password="password"))


@mock.patch("twit.users.sql_session")
def test_find_user(sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock
    with mock.patch('twit.db.find_user') as find_user:
        find_user.side_effect = [db.User("name", "password", id_value=1)]

        found = users.find_user("user login")

        assert found.id == 1
        assert found.name == "name"
        assert found.password == "password"


@mock.patch("twit.users.sql_session")
def test_follow(sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock

    john_user = db.User("john", "secret", id_value=1)
    adam_user = db.User("adam", "secret", id_value=2)

    with mock.patch('twit.users.db.find_user') as find_user:
        find_user.side_effect = mock_find_user_to_find((john_user, adam_user))

        follower = users.follow("adam", "john")

        assert follower.user == john_user.id
        assert follower.follower == adam_user.id
        session_mock.add.assert_called_with(FieldMatcher(
            user=john_user,
            follower=adam_user
        ))


@mock.patch("twit.users.sql_session")
@mock.patch("twit.users.tokens")
def test_login_user(token_mock, sql_session_mock, session_mock):
    sql_session_mock.return_value.__enter__.return_value = session_mock
    with mock.patch("twit.users.db.login") as login_user:
        user = db.User("john", "secret", id_value=1)
        login_user.return_value = user
        token_mock.refresh_token.return_value = Credentials(
            "secret_token",
            "refresh_token")

        credentials = users.login("login", "password")

        assert credentials.token == "secret_token"
        assert credentials.refresh_token == "refresh_token"
        token_mock.refresh_token.assert_called_with(user)


@pytest.fixture()
def session_mock():
    return mock.Mock()


def mock_find_user_to_find(users):
    db_stub = dict((u.name, u) for u in users)

    def user_finder(_, user_name):
        if user_name in db_stub:
            return db_stub[user_name]

    return user_finder
