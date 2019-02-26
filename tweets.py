from collections import namedtuple
import db

Tweet = namedtuple("Tweet", "id user content")


def create_tweet(user_login, content):
    with db.session_creator() as session:
        user = db.find_user(session, user_login)
        tweet = db.Tweet(user=user, content=content)
        session.add(tweet)
        session.flush()
        return Tweet(tweet.id, user_login, content)
