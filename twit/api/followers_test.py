from unittest import mock

from twit.api.conftest import stub_user
from twit.users import User, Follower


@mock.patch("twit.api.users.users.follow")
def test_follow(follow, jwt_mock, client):
    stub_user(jwt_mock, "john")
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name}) \
        .get_json()

    assert response == {
        "id": 1,
        "user": 1,
        "follower": 2
    }


@mock.patch("twit.api.users.users.follow")
def test_raises_security_exception_when_following_invalid_user(follow, jwt_mock, client):
    stub_user(jwt_mock, "mark")
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name})

    assert response.status_code == 403
