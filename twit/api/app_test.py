from unittest import mock

from sqlalchemy.orm.exc import NoResultFound
from twit.api.conftest import token_header


@mock.patch("twit.api.users.users.find_user")
def test_NoResultFound_error_handler(find_user, client):
    find_user.side_effect = NoResultFound()

    response = client.get("/users/non_existing", headers=token_header("non_existing"))

    assert response.status_code == 404
    assert response.get_json() == {
        "message": "not found",
        "err": "()"
    }
