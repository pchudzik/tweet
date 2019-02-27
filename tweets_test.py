import pytest
from unittest import mock
from collections import namedtuple
from FiledMatcher import FieldMatcher
import tweets


def test_add_tweet(session_mock):
    user = object()
    with mock.patch("db.find_user", return_value=user):
        with mock.patch('db.Session', return_value=session_mock):
            tweets.create_tweet("john", "content")

            session_mock.add.assert_called_with(FieldMatcher(
                user=user,
                content="content"))
            session_mock.flush.assert_called()


def test_find_tweets(session_mock):
    TweetMock = namedtuple("TweetMock", "id content")
    tweet = [TweetMock(123, "any content")]

    with mock.patch("db.find_tweets", return_value=tweet) as find_tweets:
        with mock.patch('db.Session', return_value=session_mock):
            tweets.find_tweets("john")

            find_tweets.assert_called_with(session_mock, "john")


@pytest.fixture()
def session_mock():
    return mock.Mock()
