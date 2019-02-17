from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from contextlib import contextmanager

from config import configuration

engine = create_engine(configuration.get("database", "url"), echo=True)

Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_creator(commit=lambda s: s.commit()):
    session = Session()
    try:
        yield session
        commit(session)
    except:
        session.rollback()
        raise
    finally:
        session.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(64))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def add_follower(self, user):
        self.followers.append(user)

    def __repr__(self):
        return f"{self.__class__.name}(id={self.id},name={self.name})"


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    user = relationship("User")

    def __init__(self, *, user, content):
        self.user = user
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id},user={self.user_id},content={self.content})"


class Follower(Base):
    __tablename__ = "followers"

    id = Column("id", Integer, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id])

    follower_id = Column("follower_id", Integer, ForeignKey("users.id"))
    follower = relationship("User", foreign_keys=[follower_id])

    def __init__(self, *, user, follower):
        self.user = user
        self.follower = follower


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

    return session.query(User).filter(User.id.in_(followers_q)).all()
