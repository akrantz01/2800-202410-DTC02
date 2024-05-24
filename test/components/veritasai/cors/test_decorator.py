from typing import Generator

import pytest
from flask import Flask, Request, Response, typing
from pytest import MonkeyPatch
from veritasai.cors import handle_cors


@handle_cors
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


def test_passes_through_request_when_non_options_method_and_no_origin_header():
    response = dummy_handler(Request.from_values(method="GET"))

    assert response.status_code == 204

    for header in response.headers.keys():
        assert not header.startswith("Access-Control-")


def test_passes_through_request_when_non_options_method_and_origin_header_present():
    response = dummy_handler(
        Request.from_values(method="GET", headers={"Origin": "http://example.com"})
    )

    assert response.status_code == 204
    assert response.headers["Access-Control-Allow-Origin"] == "http://example.com"
    assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
    assert response.headers["Access-Control-Allow-Headers"] == "Authorization, Content-Type"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_resonds_with_cors_headers_when_options_method_and_origin_explicitly_configured(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "http://configured.com")
    response = dummy_handler(Request.from_values(method="OPTIONS", headers={}))

    assert response.status_code == 204
    assert response.headers["Access-Control-Allow-Origin"] == "http://configured.com"
    assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
    assert response.headers["Access-Control-Allow-Headers"] == "Authorization, Content-Type"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_resonds_with_cors_headers_when_options_method_and_origin_configured_to_mirror(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    response = dummy_handler(
        Request.from_values(method="OPTIONS", headers={"Origin": "http://example.com"})
    )

    assert response.status_code == 204
    assert response.headers["Access-Control-Allow-Origin"] == "http://example.com"
    assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
    assert response.headers["Access-Control-Allow-Headers"] == "Authorization, Content-Type"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_omits_cors_headers_when_options_method_and_no_origin_header_present(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    response = dummy_handler(Request.from_values(method="OPTIONS"))

    assert response.status_code == 204

    for header in response.headers.keys():
        assert not header.startswith("Access-Control-")
