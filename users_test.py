import pytest
from unittest import mock
from operator import attrgetter
import users


def test_create_user(session_mock):
    with mock.patch('db.Session', return_value=session_mock):
        users.create_user("name", "password")

        session_mock.add.assert_called_with(FieldMatcher(
            name="name",
            password="password"))


@pytest.fixture()
def session_mock():
    return mock.Mock()


class FieldMatcher:
    def __init__(self, **fields):
        self.fields = dict((attrgetter(field), value) for field, value in fields.items())

    def __eq__(self, other):
        for attr, value in self.fields.items():
            assert value == attr(other)
        return True
