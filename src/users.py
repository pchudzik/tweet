from collections import namedtuple
from src import db
from src.infrastructure import session as sql_session
from src import tokens

User = namedtuple("User", "id, name, password")
User.from_ = lambda db_user: User(db_user.id, db_user.name, db_user.password)
Follower = namedtuple("Follower", "id, user, follower")
Credentials = namedtuple("Credentials", "token, refresh_token")


def create_user(name, password):
    with sql_session() as session:
        user = db.User(name, password)
        session.add(user)
        session.flush()
        return User.from_(user)


def follow(follower, user):
    with sql_session() as session:
        follower_db = db.find_user(session, follower)
        user_db = db.find_user(session, user)
        follower = db.Follower(user=user_db, follower=follower_db)
        session.add(follower)
        session.flush()
        return Follower(
            follower.id,
            follower.user.id,
            follower.follower.id)


def find_user(login):
    with sql_session() as session:
        user = db.find_user(session, login)
        return User(user.id, user.name, user.password)


def login(login, password):
    with sql_session() as session:
        user = db.login(session, login, password)

        if user:
            return tokens.refresh_token(user)
