from flask import Flask, jsonify, request
from collections import namedtuple
from sqlalchemy.orm.exc import NoResultFound
from src.infrastructure import init_extensions
from src import users, tweets
from src.config import configuration

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get("database", "url")
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


@app.route("/users/<login>/tweets", methods=["POST"])
def create_tweet(login):
    payload = request.get_json()
    tweet = tweets.create_tweet(login, payload.get("content"))
    return jsonify(tweet._asdict())


@app.route("/users/<login>/tweets", methods=["GET"])
def find_all_tweets(login):
    all_tweets = tweets.find_tweets(login)
    return jsonify(list(map(lambda t: t._asdict(), all_tweets)))


@app.errorhandler(NoResultFound)
def no_result_found_handler(error):
    return jsonify(message="not found", err=str(error)), 404
