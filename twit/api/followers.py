from flask import jsonify, request, Flask

from twit import tokens
from twit import users


@tokens.inject_identity
def add_follower(login, user):
    payload = request.get_json()
    follower = payload.get("follower")
    user = payload.get("user") if user.name == login and login == payload.get("user") else ""

    if not user:
        raise tokens.SecurityException()

    return jsonify(users.follow(follower, user)._asdict())


def init_followers_endpoints(app: Flask):
    app.add_url_rule("/users/<login>/followers", view_func=add_follower, methods=["PATCH"])
