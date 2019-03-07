from collections import namedtuple
from flask_jwt_extended import create_access_token, create_refresh_token
from src import db, infrastructure

Credentials = namedtuple("Credentials", "token, refresh_token")


def refresh_token(user):
    return Credentials(
        _generate_token(user),
        _generate_refresh_token(user))


def revoke(jti):
    with infrastructure.session() as session:
        session.add(db.Token(jti))


def _generate_token(user):
    return create_access_token(_create_identity(user))


def _generate_refresh_token(user):
    return create_refresh_token(_create_identity(user))


def _create_identity(user):
    return {
        "user": {
            "name": user.name
        }
    }
