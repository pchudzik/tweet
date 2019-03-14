from unittest import mock

import pytest

from twit.api.app import app
from twit.infrastructure import jwt
from twit.tokens import refresh_token
from twit.users import User


@jwt.token_in_blacklist_loader
def token_blacklist(*args):
    return False


@pytest.fixture(scope="module")
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


def token_header(user_login="any_user"):
    user = User(1, user_login, "any password")
    with app.test_request_context():
        token = refresh_token(user).token
    return {
        "Authorization": f"Bearer {token}"
    }
