import pytest
from unittest import mock
from FiledMatcher import FieldMatcher
import tweets


def test_add_tweet(session_mock):
    user = object()
    with mock.patch("db.find_user", return_value=user) as find_user:
        with mock.patch('db.Session', return_value=session_mock):
            tweets.create_tweet("john", "content")

            session_mock.add.assert_called_with(FieldMatcher(
                user=user,
                content="content"))
            session_mock.flush.assert_called()


@pytest.fixture()
def session_mock():
    return mock.Mock()
