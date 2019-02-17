import pytest
from sqlalchemy.orm.exc import NoResultFound

from db import session_creator
from db import User, Tweet, Follower
from db import find_user, find_tweets, find_followers


@pytest.fixture()
def session():
    with session_creator(commit=lambda s:s.rollback()) as session:
        yield session


def test_create_user(session):
    johnd = create_entity(session, User("johnd", "secret321"))

    assert johnd.id is not None
    assert johnd.name == "johnd"
    assert johnd.password == "secret321"


def test_find_user(session):
    created = create_entity(session, User("johnd", "john"))

    found = find_user(session, "johnd")

    assert found is not None
    assert found.id == created.id
    assert found.name == "johnd"


def test_find_users_finds_nothing_when_not_existing(session):
    with pytest.raises(NoResultFound):
        find_user(session, "not existing login")


def test_user_add_tweet(session):
    user = create_entity(session, User("johnd", "john"))
    ala = create_entity(session, Tweet(user=user, content="ala ma kota"))
    kot = create_entity(session, Tweet(user=user, content="kot ma ale"))
    session.flush()

    assert set(find_tweets(session, user.name)) == {ala, kot}


def test_find_tweets(session):
    johnd = create_entity(session, User("johnd", "john"))
    smitha = create_entity(session, User("smitha", "adam"))

    john_tweet1 = create_entity(session, Tweet(user=johnd, content="ala ma kota"))
    john_tweet2 = create_entity(session, Tweet(user=johnd, content="kot ma ale"))
    create_entity(session, Tweet(user=smitha, content="content1"))
    create_entity(session, Tweet(user=smitha, content="content2"))

    session.flush()

    assert set(find_tweets(session, "johnd")) == {john_tweet1, john_tweet2}


def test_follow(session):
    john = create_entity(session, User("john", "secret"))
    adam = create_entity(session, User("adam", "secret"))
    mark = create_entity(session, User("mark", "secret"))

    create_entity(session, Follower(user=adam, follower=john))
    create_entity(session, Follower(user=adam, follower=mark))
    create_entity(session, Follower(user=john, follower=adam))

    assert len(find_followers(session, mark.name)) == 0
    assert set(find_followers(session, adam.name)) == {john, mark}
    assert set(find_followers(session, john.name)) == {adam}


def create_entity(session, entity):
    session.add(entity)
    session.flush()
    return entity
