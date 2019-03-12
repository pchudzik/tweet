from collections import namedtuple
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from twit import db, infrastructure
from functools import wraps

Credentials = namedtuple("Credentials", "token, refresh_token")


def guarantee_identity(f):
    @wraps(f)
    def check(*args, **kwargs):
        login = kwargs["login"]
        user = get_jwt_identity()
        if user.get("name") != login:
            raise SecurityException()
        return f(*args, **kwargs)

    return check


def inject_identity(fn):
    @wraps(fn)
    def do_inject(*args, **kwargs):
        kwargs["user"] = UserIdentity(get_jwt_identity())
        return fn(*args, **kwargs)

    return do_inject


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
        "name": user.name
    }


class UserIdentity:
    def __init__(self, jwt_token):
        self.name = jwt_token.get("name")


class SecurityException(Exception):
    pass
