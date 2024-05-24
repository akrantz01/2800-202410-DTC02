from typing import Generator

import pytest
from firebase_admin.auth import InvalidIdTokenError
from flask import Flask, Request, Response, typing
from pytest_mock import MockerFixture
from veritasai.authentication import login_required


@login_required
def dummy_handler(_request: Request) -> typing.ResponseReturnValue:
    """
    A dummy handler for testing purposes.

    :param _request: the incoming request
    :return: an empty successful response
    """
    return Response(status=204)


@pytest.fixture(autouse=True)
def app_context() -> Generator[Flask, None, None]:
    """
    Create a dummy Flask app context for testing.
    """
    flask = Flask(__name__)
    with flask.test_request_context():
        yield flask


def test_returns_error_when_no_token():
    response = dummy_handler(Request.from_values())

    assert response.status_code == 401
    assert response.json == {"error": "bearer token required"}


def test_returns_error_when_authorization_header_is_not_bearer():
    response = dummy_handler(Request.from_values(headers={"Authorization": "Basic test"}))

    assert response.status_code == 401
    assert response.json == {"error": "bearer token required"}


def test_returns_error_when_token_is_invalid(mocker: MockerFixture):
    auth = mocker.patch("veritasai.authentication.decorator.get_auth")
    auth.return_value.verify_id_token.side_effect = InvalidIdTokenError("invalid token")

    response = dummy_handler(Request.from_values(headers={"Authorization": "Bearer invalid"}))

    assert response.status_code == 401
    assert response.json == {"error": "invalid bearer token"}


def test_passes_through_when_token_is_valid(mocker: MockerFixture):
    auth = mocker.patch("veritasai.authentication.decorator.get_auth")
    auth.return_value.verify_id_token.return_value = {"sub": "user-id"}

    response = dummy_handler(Request.from_values(headers={"Authorization": "Bearer valid"}))

    assert response.status_code == 204
    assert response.json is None
