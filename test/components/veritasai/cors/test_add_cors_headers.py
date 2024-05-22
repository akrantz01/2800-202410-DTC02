from flask import Request, Response
from pytest import MonkeyPatch
from veritasai.cors.response import add_cors_headers


def test_adds_headers_when_origin_statically_configured(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "http://configured.com")
    request = Request.from_values(method="OPTIONS")

    response = Response()
    add_cors_headers(response, request)

    assert response.headers["Access-Control-Allow-Origin"] == "http://configured.com"
    assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
    assert response.headers["Access-Control-Allow-Headers"] == "Authorization, Content-Type"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_allow_origin_header_does_not_match_request_origin_when_explicitly_configured(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "http://configured.com")
    request = Request.from_values(method="OPTIONS", headers={"Origin": "http://example.com"})

    response = Response()
    add_cors_headers(response, request)

    assert response.headers["Access-Control-Allow-Origin"] == "http://configured.com"


def test_adds_headers_when_origin_set_to_mirror_request(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    request = Request.from_values(method="OPTIONS", headers={"Origin": "http://example.com"})

    response = Response()
    add_cors_headers(response, request)

    assert response.headers["Access-Control-Allow-Origin"] == "http://example.com"
    assert response.headers["Access-Control-Allow-Methods"] == "POST, OPTIONS"
    assert response.headers["Access-Control-Allow-Headers"] == "Authorization, Content-Type"
    assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_does_not_add_headers_when_origin_set_to_mirror_and_no_origin_header_present(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    request = Request.from_values(method="OPTIONS")

    response = Response()
    add_cors_headers(response, request)

    for header in response.headers.keys():
        assert not header.startswith("Access-Control-")
