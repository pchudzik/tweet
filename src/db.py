from sqlalchemy import Column, Integer, String, ForeignKey
import datetime
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

from src.infrastructure import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(64))

    def __init__(self, name, password, id_value=None):
        self.id = id_value
        self.name = name
        self.password = password

    def add_follower(self, user):
        self.followers.append(user)

    def __repr__(self):
        return f"{self.__class__.name}(id={self.id},name={self.name})"


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    user = relationship("User")
    post_time = Column("post_time", DateTime, nullable=False)

    def __init__(self, *, user, content, now=None):
        self.user = user
        self.content = content
        self.post_time = datetime.datetime.utcnow() if now is None else now

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id},user={self.user_id},content={self.content})"


class Follower(db.Model):
    __tablename__ = "followers"

    id = Column("id", Integer, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id])

    follower_id = Column("follower_id", Integer, ForeignKey("users.id"))
    follower = relationship("User", foreign_keys=[follower_id])

    def __init__(self, *, user, follower):
        self.user = user
        self.follower = follower


class Token(db.Model):
    __tablename__ = "jwt_revoked_tokens"

    id = db.Column("id", db.Integer, primary_key=True)
    jti = db.Column("jti", db.String(120))

    def __init__(self, jti):
        self.jti = jti


def is_token_revoked(session, jti):
    return bool(session.query(Token)
                .filter(Token.jti == jti)
                .first())


def login(session, login, password):
    return session.query(User) \
        .filter(User.name == login and User.password == password) \
        .one_or_none()


def find_user(session, login):
    return session.query(User).filter(User.name == login).one()


def find_tweets(session, login):
    return session \
        .query(Tweet) \
        .join(User, User.id == Tweet.user_id) \
        .filter(User.name == login) \
        .all()


def find_followers(session, login):
    followers_q = session \
        .query(Follower.follower_id) \
        .join(Follower.user) \
        .filter(User.name == login) \
        .subquery()

    return db.session.query(User).filter(User.id.in_(followers_q)).all()
