from collections import namedtuple
import db

User = namedtuple("User", "id, name, password")


def create_user(name, password):
    with db.session_creator() as session:
        user = db.User(name, password)
        session.add(user)
        session.flush()
        return User(user.id, user.name, user.password)
