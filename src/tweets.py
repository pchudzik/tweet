from collections import namedtuple
from src import db
from src.infrastructure import db as sql

Tweet = namedtuple("Tweet", "id user content")


def create_tweet(user_login, content):
    user = db.find_user(user_login)
    tweet = db.Tweet(user=user, content=content)
    sql.session.add(tweet)
    sql.session.flush()
    return Tweet(tweet.id, user_login, content)


def find_tweets(user_login):
    return list(map(
        lambda t: Tweet(t.id, user_login, t.content),
        db.find_tweets(user_login)))
