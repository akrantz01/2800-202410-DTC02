import pytest
from flask.testing import FlaskClient
from pytest import MonkeyPatch

pytestmark = pytest.mark.function("analysis_manager")


@pytest.fixture(autouse=True)
def disable_authentication(monkeypatch: MonkeyPatch):
    """
    Disable authentication for testing purposes.
    """
    monkeypatch.setattr("veritasai.authentication.login_required", lambda func: func)


@pytest.fixture
def data() -> dict[str, str]:
    """
    Mock input data to mock the request payload.
    """
    return {
        "content": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "Fawks",
        "source-url": "https://foxnews.com",
    }


def test_missing_fields(client: FlaskClient):
    response = client.post("/", json={})

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["content"],
            "msg": "Field required",
            "type": "missing",
        },
        {
            "loc": [
                "author",
            ],
            "msg": "Field required",
            "type": "missing",
        },
        {
            "loc": [
                "publisher",
            ],
            "msg": "Field required",
            "type": "missing",
        },
    ]


def test_all_fields_empty(client: FlaskClient):
    data = {"content": "", "author": "", "publisher": "", "source-url": ""}
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["content"],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
        },
        {
            "loc": ["author"],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
        },
        {
            "loc": ["publisher"],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
        },
        {
            "loc": ["source-url"],
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
        },
    ]


def test_content_empty(client: FlaskClient, data: dict[str, str]):
    data["content"] = ""
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["content"],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
        },
    ]


def test_author_empty(client: FlaskClient, data: dict[str, str]):
    data["author"] = ""
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["author"],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
        },
    ]


def test_publisher_empty(client: FlaskClient, data: dict[str, str]):
    data["publisher"] = ""
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["publisher"],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
        },
    ]


def test_url_empty(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = ""
    response = client.post("/", json=data)
    assert response.status_code == 422
    assert response.json == [
        {
            "loc": [
                "source-url",
            ],
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
        },
    ]


@pytest.mark.parametrize("field,length", [("content", 5), ("author", 5), ("publisher", 2)])
def test_field_too_short(client: FlaskClient, data: dict[str, str], field: str, length: int):
    data[field] = "a" * (length - 1)
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": [field],
            "msg": f"String should have at least {length} characters",
            "type": "string_too_short",
        },
    ]


def test_url_invalid_string(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "Behind ye old windmill"
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["source-url"],
            "msg": "Input should be a valid URL, relative URL without a base",
            "type": "url_parsing",
        },
    ]


def test_url_invalid_domain(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "http://Behind ye old windmill"
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["source-url"],
            "msg": "Input should be a valid URL, invalid domain character",
            "type": "url_parsing",
        },
    ]


def test_url_invalid_characters(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "ttp://#*@)($#$)"
    response = client.post("/", json=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "loc": ["source-url"],
            "msg": "URL scheme should be 'http' or 'https'",
            "type": "url_scheme",
        },
    ]
