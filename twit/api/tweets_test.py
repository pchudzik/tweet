from unittest import mock

import pytest

from twit.api.app import app
from twit.tweets import Tweet


@mock.patch("twit.api.tweets.tweets.create_tweet")
def test_create_tweet(create_tweet, client, jwt_mock):
    stub_user(jwt_mock, "john")
    login = "john"
    content = "content"
    create_tweet.return_value = Tweet(123, login, content)

    response = client \
        .post(f"/users/{login}/tweets", json={"content": content}) \
        .get_json()

    assert response == {
        "id": 123,
        "user": login,
        "content": content
    }


@mock.patch("twit.api.tweets.tweets.create_tweet")
def test_raises_execption_when_creating_tweet_as_other_user(create_tweet, client, jwt_mock):
    stub_user(jwt_mock, "adam")

    response = client \
        .post("/users/other/tweets", json={"content": "any_content"})

    assert response.status_code == 403


@mock.patch("twit.api.tweets.tweets.find_tweets")
def test_find_tweet(find_tweets, client):
    login = "john"
    content = "content"
    find_tweets.return_value = [
        Tweet(123, login, content + "1"),
        Tweet(321, login, content + "2")]

    response = client \
        .get(f"/users/{login}/tweets") \
        .get_json()

    assert response == [{
        "id": 123,
        "user": login,
        "content": content + "1"
    }, {
        "id": 321,
        "user": login,
        "content": content + "2"
    }]


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture()
def jwt_mock():
    with mock.patch("twit.api.security.tokens.get_jwt_identity") as jwt_identity:
        yield jwt_identity


def stub_user(identity, user):
    identity.return_value = {
        "name": user
    }
