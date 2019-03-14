from unittest import mock

from twit.api.conftest import token_header
from twit.users import User, Follower


@mock.patch("twit.api.users.users.follow")
def test_follow(follow, client):
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name},
               headers=token_header("john")) \
        .get_json()

    assert response == {
        "id": 1,
        "user": 1,
        "follower": 2
    }


@mock.patch("twit.api.users.users.follow")
def test_raises_security_exception_when_following_invalid_user(follow, client):
    john_user = User(1, "john", "secret1")
    adam_user = User(2, "adam", "secret2")
    follow.return_value = Follower(1, john_user.id, adam_user.id)

    response = client \
        .patch(f"/users/{john_user.name}/followers",
               json={"user": john_user.name, "follower": adam_user.name},
               headers=token_header("some_other_user"))

    assert response.status_code == 403
