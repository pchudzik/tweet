import pytest
from unittest import mock
from collections import namedtuple
from twit.FiledMatcher import FieldMatcher
from twit import tweets


@mock.patch("twit.tweets.sql_session")
def test_add_tweet(sql_session_mock, session_mock):
    user = object()
    sql_session_mock.return_value.__enter__.return_value = session_mock

    with mock.patch("twit.db.find_user", return_value=user):
        tweets.create_tweet("john", "content")

        session_mock.add.assert_called_with(FieldMatcher(
            user=user,
            content="content"))
        session_mock.flush.assert_called()


@mock.patch("twit.tweets.sql_session")
def test_find_tweets(sql_session_mock, session_mock):
    TweetMock = namedtuple("TweetMock", "id content")
    tweet = [TweetMock(123, "any content")]
    sql_session_mock.return_value.__enter__.return_value = session_mock

    with mock.patch("twit.db.find_tweets", return_value=tweet) as find_tweets:
        tweets.find_tweets("john")

        find_tweets.assert_called_with(session_mock, "john")


@pytest.fixture()
def session_mock():
    return mock.Mock()
