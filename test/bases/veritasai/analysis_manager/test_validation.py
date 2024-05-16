import pytest
from flask.testing import FlaskClient

pytestmark = pytest.mark.function("analysis_manager")


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
    response = client.post("/", data={})

    assert response.status_code == 422
    assert response.json == [
        {
            "input": {},
            "loc": [
                "content",
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        },
        {
            "input": {},
            "loc": [
                "author",
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        },
        {
            "input": {},
            "loc": [
                "publisher",
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        },
        {
            "input": {},
            "loc": [
                "source-url",
            ],
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        },
    ]


def test_all_fields_empty(client: FlaskClient):
    data = {"content": "", "author": "", "publisher": "", "source-url": ""}
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": [
                "content",
            ],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "min_length": 2,
            },
            "input": "",
            "loc": [
                "author",
            ],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": [
                "publisher",
            ],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "error": "input is empty",
            },
            "input": "",
            "loc": [
                "source-url",
            ],
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_content_empty(client: FlaskClient, data: dict[str, str]):
    data["content"] = ""
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": [
                "content",
            ],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_author_empty(client: FlaskClient, data: dict[str, str]):
    data["author"] = ""
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "min_length": 2,
            },
            "input": "",
            "loc": [
                "author",
            ],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_publisher_empty(client: FlaskClient, data: dict[str, str]):
    data["publisher"] = ""
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": ["publisher"],
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_url_empty(client: FlaskClient):
    response = client.post(
        "/",
        data={
            "content": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "Fawkes News",
            "source-url": "",
        },
    )
    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "error": "input is empty",
            },
            "input": "",
            "loc": [
                "source-url",
            ],
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


@pytest.mark.parametrize("field,length", [("content", 5), ("author", 2), ("publisher", 5)])
def test_field_too_short(client: FlaskClient, data: dict[str, str], field: str, length: int):
    data[field] = "a" * (length - 1)
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "min_length": length,
            },
            "input": "a" * (length - 1),
            "loc": [field],
            "msg": f"String should have at least {length} characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_url_invalid_string(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "Behind ye old windmill"
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "error": "relative URL without a base",
            },
            "input": "Behind ye old windmill",
            "loc": [
                "source-url",
            ],
            "msg": "Input should be a valid URL, relative URL without a base",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_url_invalid_domain(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "http://Behind ye old windmill"
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "error": "invalid domain character",
            },
            "input": "http://Behind ye old windmill",
            "loc": [
                "source-url",
            ],
            "msg": "Input should be a valid URL, invalid domain character",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_url_invalid_characters(client: FlaskClient, data: dict[str, str]):
    data["source-url"] = "ttp://#*@)($#$)"
    response = client.post("/", data=data)

    assert response.status_code == 422
    assert response.json == [
        {
            "ctx": {
                "expected_schemes": "'http' or 'https'",
            },
            "input": "ttp://#*@)($#$)",
            "loc": [
                "source-url",
            ],
            "msg": "URL scheme should be 'http' or 'https'",
            "type": "url_scheme",
            "url": "https://errors.pydantic.dev/2.7/v/url_scheme",
        },
    ]
