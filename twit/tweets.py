from collections import namedtuple
from twit import db
from twit.infrastructure import session as sql_session

Tweet = namedtuple("Tweet", "id user content")


def create_tweet(user_login, content):
    with sql_session() as session:
        user = db.find_user(session, user_login)
        tweet = db.Tweet(user=user, content=content)
        session.add(tweet)
        session.flush()
        return Tweet(tweet.id, user_login, content)


def find_tweets(user_login):
    with sql_session() as session:
        return list(map(
            lambda t: Tweet(t.id, user_login, t.content),
            db.find_tweets(session, user_login)))
