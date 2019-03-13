from flask import jsonify, request, Flask

from twit import tokens
from twit import tweets


@tokens.guarantee_identity
def create_tweet(login):
    payload = request.get_json()
    tweet = tweets.create_tweet(login, payload.get("content"))
    return jsonify(tweet._asdict())


def find_all_tweets(login):
    all_tweets = tweets.find_tweets(login)
    return jsonify(list(map(lambda t: t._asdict(), all_tweets)))


def init_tweets_endpoints(app: Flask):
    app.add_url_rule("/users/<login>/tweets", view_func=create_tweet, methods=["POST"])
    app.add_url_rule("/users/<login>/tweets", view_func=find_all_tweets, methods=["GET"])
