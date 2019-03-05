import pytest
from flask_testing import TestCase
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from src.config import configuration
from src.infrastructure import init_extensions, session as sql_session

from src.db import User, Tweet, Follower
from src.db import find_user, find_tweets, find_followers, login


class DbTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get("database", "url")
        app.debug = True
        init_extensions(app)
        return app

    def test_create_user(self):
        with session_for_test() as session:
            johnd = create_entity(session, User("johnd", "secret321"))

            assert johnd.id is not None
            assert johnd.name == "johnd"
            assert johnd.password == "secret321"

    def test_find_user(self):
        with session_for_test() as session:
            created = create_entity(session, User("johnd", "john"))

            found = find_user(session, "johnd")

            assert found is not None
            assert found.id == created.id
            assert found.name == "johnd"

    def test_find_users_finds_nothing_when_not_existing(self):
        with pytest.raises(NoResultFound), session_for_test() as session:
            find_user(session, "not existing login")

    def test_user_add_tweet(self):
        with session_for_test() as session:
            user = create_entity(session, User("johnd", "john"))
            ala = create_entity(session, Tweet(user=user, content="ala ma kota"))
            kot = create_entity(session, Tweet(user=user, content="kot ma ale"))
            session.flush()

            assert set(find_tweets(session, user.name)) == {ala, kot}

    def test_find_tweets(self):
        with session_for_test() as session:
            johnd = create_entity(session, User("johnd", "john"))
            smitha = create_entity(session, User("smitha", "adam"))

            john_tweet1 = create_entity(session, Tweet(user=johnd, content="ala ma kota"))
            john_tweet2 = create_entity(session, Tweet(user=johnd, content="kot ma ale"))
            create_entity(session, Tweet(user=smitha, content="content1"))
            create_entity(session, Tweet(user=smitha, content="content2"))

            session.flush()

            assert set(find_tweets(session, "johnd")) == {john_tweet1, john_tweet2}

    def test_follow(self):
        with session_for_test() as session:
            john = create_entity(session, User("john", "secret"))
            adam = create_entity(session, User("adam", "secret"))
            mark = create_entity(session, User("mark", "secret"))

            create_entity(session, Follower(user=adam, follower=john))
            create_entity(session, Follower(user=adam, follower=mark))
            create_entity(session, Follower(user=john, follower=adam))

            assert len(find_followers(session, mark.name)) == 0
            assert set(find_followers(session, adam.name)) == {john, mark}
            assert set(find_followers(session, john.name)) == {adam}

    def test_login_user(self):
        with session_for_test() as session:
            john = create_entity(session, User("john", "secret"))
            session.flush()

            assert login(session, "john", "secret").id == john.id

    def test_login_invalid_user(self):
        with session_for_test() as session:
            assert login(session, "any_login", "invalid_password") is None


def session_for_test():
    return sql_session(lambda s: s.rollback())


def create_entity(session, entity):
    session.add(entity)
    session.flush()
    return entity
