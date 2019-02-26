from flask import Flask, jsonify, request
from collections import namedtuple
from sqlalchemy.orm.exc import NoResultFound

import users
import tweets

app = Flask(__name__)
app.debug = True

Message = namedtuple("Message", "from_, message")


@app.route("/users", methods=["POST"])
def add_user():
    payload = request.get_json()
    user = users.create_user(payload.get("name"), payload.get("password"))
    return jsonify(user._asdict())


@app.route("/users", methods=["GET"])
def list_users():
    login = request.args["name"]
    return jsonify(users.find_user(login)._asdict())


@app.route("/users/<login>/tweets", methods=["POST"])
def create_tweet(login):
    payload = request.get_json()
    tweet = tweets.create_tweet(login, payload.get("content"))
    return jsonify(tweet._asdict())


@app.errorhandler(NoResultFound)
def no_result_found_handler(error):
    return jsonify(message="not found", err=str(error)), 404


if __name__ == "__main__":
    app.run()
