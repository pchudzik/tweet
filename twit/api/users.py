from flask import jsonify, request, Flask
from flask_jwt_extended import jwt_required
from twit import users
from twit import tokens


def add_user():
    payload = request.get_json()
    user = users.create_user(payload.get("name"), payload.get("password"))
    return jsonify(user._asdict())


@tokens.guarantee_identity
@jwt_required
def list_user(login):
    return jsonify(users.find_user(login)._asdict())


def init_users_endpoints(app: Flask):
    app.add_url_rule("/users", view_func=add_user, methods=["POST"])
    app.add_url_rule("/users/<login>", view_func=list_user, methods=["GET"])
