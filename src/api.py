from flask import Flask, jsonify, request
from collections import namedtuple
from sqlalchemy.orm.exc import NoResultFound
from src.infrastructure import init_extensions
from src import users, tweets
from src.config import configuration
from src import tokens
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get("database", "url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = configuration.get("database", "tack_modifications")
app.config['JWT_SECRET_KEY'] = configuration.get("jwt", "secret")
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
init_extensions(app)
Message = namedtuple("Message", "from_, message")


@app.route("/users", methods=["POST"])
def add_user():
    payload = request.get_json()
    user = users.create_user(payload.get("name"), payload.get("password"))
    return jsonify(user._asdict())


@app.route("/users/<login>", methods=["GET"])
def list_users(login):
    return jsonify(users.find_user(login)._asdict())


@app.route("/login", methods=["POST"])
def login_user():
    payload = request.get_json()
    login_state = users.login(payload.get("login"), payload.get("password"))
    if login_state:
        return jsonify(login_state._asdict())
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@jwt_refresh_token_required
@app.route("/login/refresh", methods=["POST"])
def refresh_token():
    user = get_jwt_identity()
    return jsonify(tokens.refresh_token(user)._asdict())


@jwt_required
@app.route("/logout", methods=["POST"])
def logout():
    tokens.revoke(get_raw_jwt()['jti'])
    return '', 204


@app.route("/users/<login>/tweets", methods=["POST"])
def create_tweet(login):
    payload = request.get_json()
    tweet = tweets.create_tweet(login, payload.get("content"))
    return jsonify(tweet._asdict())


@app.route("/users/<login>/tweets", methods=["GET"])
def find_all_tweets(login):
    all_tweets = tweets.find_tweets(login)
    return jsonify(list(map(lambda t: t._asdict(), all_tweets)))


@app.route("/users/<login>/followers", methods=["PATCH"])
def add_follower(login):
    payload = request.get_json()
    follower = payload.get("follower")
    user = payload.get("user")
    return jsonify(users.follow(follower, user)._asdict())


@app.errorhandler(NoResultFound)
def no_result_found_handler(error):
    return jsonify(message="not found", err=str(error)), 404


@app.errorhandler(Exception)
def any_error_handler(error):
    return jsonify(message="not found", err=str(error)), 500
