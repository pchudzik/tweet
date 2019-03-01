import pytest
from unittest import mock
from collections import namedtuple
from src.FiledMatcher import FieldMatcher
from src import tweets


def test_add_tweet():
    user = object()
    with mock.patch("src.db.find_user", return_value=user):
        with mock.patch('src.infrastructure.db.session') as session_mock:
            tweets.create_tweet("john", "content")

            session_mock.add.assert_called_with(FieldMatcher(
                user=user,
                content="content"))
            session_mock.flush.assert_called()


def test_find_tweets():
    TweetMock = namedtuple("TweetMock", "id content")
    tweet = [TweetMock(123, "any content")]

    with mock.patch("src.db.find_tweets", return_value=tweet) as find_tweets:
        with mock.patch('src.infrastructure.db.session'):
            tweets.find_tweets("john")

            find_tweets.assert_called_with("john")

