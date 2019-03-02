from collections import namedtuple
from src import db
from src.infrastructure import session as sql_session

User = namedtuple("User", "id, name, password")


def create_user(name, password):
    with sql_session() as session:
        user = db.User(name, password)
        session.add(user)
        session.flush()
        return User(user.id, user.name, user.password)


def find_user(login):
    with sql_session() as session:
        user = db.find_user(session, login)
        return User(user.id, user.name, user.password)
