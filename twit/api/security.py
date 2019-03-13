from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from flask import jsonify, request, Flask

from twit import users, tokens


def login_user():
    payload = request.get_json()
    login_state = users.login(payload.get("login"), payload.get("password"))
    if login_state:
        return jsonify(login_state._asdict())
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@jwt_refresh_token_required
def refresh_token():
    user = get_jwt_identity()
    return jsonify(tokens.refresh_token(user)._asdict())


@jwt_required
def logout():
    tokens.revoke(get_raw_jwt()['jti'])
    return '', 204


def init_security(app: Flask):
    app.add_url_rule("/login", None, view_func=login_user, methods=["POST"])
    app.add_url_rule("/login/refresh", view_func=refresh_token, methods=["POST"])
    app.add_url_rule("/logout", view_func=logout, methods=["POST"])
