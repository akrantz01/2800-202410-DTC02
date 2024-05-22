from flask import Request
from pytest import MonkeyPatch
from veritasai.cors.response import allowed_origin


def test_mirrors_request_origin_when_set_to_astrisk(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    request = Request.from_values(method="OPTIONS", headers={"Origin": "http://example.com"})
    assert allowed_origin(request) == "http://example.com"


def test_returns_configured_origin_when_set_to_specific_origin(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "http://configured.com")
    request = Request.from_values(method="OPTIONS", headers={"Origin": "http://example.com"})
    assert allowed_origin(request) == "http://configured.com"


def test_returns_none_when_not_explicitly_configured_and_no_origin_header(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.cors.response.ORIGIN", "*")
    request = Request.from_values(method="OPTIONS")
    assert allowed_origin(request) is None
