import pytest
from flask_testing import TestCase
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from src.config import configuration
from src.infrastructure import db, init_extensions

from src.db import User, Tweet, Follower
from src.db import find_user, find_tweets, find_followers


class DbTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get("database", "url")
        app.debug = True
        init_extensions(app)
        return app

    def test_create_user(self):
        johnd = create_entity(User("johnd", "secret321"))

        assert johnd.id is not None
        assert johnd.name == "johnd"
        assert johnd.password == "secret321"

    def test_find_user(self):
        created = create_entity(User("johnd", "john"))

        found = find_user("johnd")

        assert found is not None
        assert found.id == created.id
        assert found.name == "johnd"

    def test_find_users_finds_nothing_when_not_existing(self):
        with pytest.raises(NoResultFound):
            find_user("not existing login")

    def test_user_add_tweet(self):
        user = create_entity(User("johnd", "john"))
        ala = create_entity(Tweet(user=user, content="ala ma kota"))
        kot = create_entity(Tweet(user=user, content="kot ma ale"))
        db.session.flush()

        assert set(find_tweets(user.name)) == {ala, kot}

    def test_find_tweets(self):
        johnd = create_entity(User("johnd", "john"))
        smitha = create_entity(User("smitha", "adam"))

        john_tweet1 = create_entity(Tweet(user=johnd, content="ala ma kota"))
        john_tweet2 = create_entity(Tweet(user=johnd, content="kot ma ale"))
        create_entity(Tweet(user=smitha, content="content1"))
        create_entity(Tweet(user=smitha, content="content2"))

        db.session.flush()

        assert set(find_tweets("johnd")) == {john_tweet1, john_tweet2}

    def test_follow(self):
        john = create_entity(User("john", "secret"))
        adam = create_entity(User("adam", "secret"))
        mark = create_entity(User("mark", "secret"))

        create_entity(Follower(user=adam, follower=john))
        create_entity(Follower(user=adam, follower=mark))
        create_entity(Follower(user=john, follower=adam))

        assert len(find_followers(mark.name)) == 0
        assert set(find_followers(adam.name)) == {john, mark}
        assert set(find_followers(john.name)) == {adam}


def create_entity(entity):
    db.session.add(entity)
    db.session.flush()
    return entity
