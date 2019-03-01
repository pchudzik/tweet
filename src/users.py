from collections import namedtuple
from src import db
from src.infrastructure import db as sql

User = namedtuple("User", "id, name, password")


def create_user(name, password):
    user = db.User(name, password)
    sql.session.add(user)
    sql.session.flush()
    return User(user.id, user.name, user.password)


def find_user(login):
    user = db.find_user(login)
    return User(user.id, user.name, user.password)
