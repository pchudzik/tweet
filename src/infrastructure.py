from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()


@contextmanager
def session(commit=lambda s: s.commit()):
    try:
        s = db.session
        yield s
        commit(s)
    except:
        s.rollback()
        raise
    finally:
        s.close()


def init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
