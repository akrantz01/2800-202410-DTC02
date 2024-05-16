import json
from pathlib import Path

import pytest
from functions_framework import create_app

PROJECT_DIR = Path(__file__).parent.parent


@pytest.fixture
def app():
    """
    Create a new function application instance.
    """

    instance = create_app(source=PROJECT_DIR / "main.py", target="handler")
    instance.config.update({"TESTING": True})

    yield instance


@pytest.fixture
def client(app):
    """
    Retrieve the client for the function handler.
    """
    return app.test_client()


def test_all_fields_empty(client):
    response = client.post(
        "/",
        data={"text-to-analyze": "", "author": "", "publisher": "", "source-url": ""},
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 2 characters",
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert response.status_code == 422


def test_author_empty(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "",
            "publisher": "Fawks",
            "source-url": "https://foxnews.com",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 5 characters",
    }
    assert response.status_code == 422


def test_publisher_empty(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "",
            "source-url": "https://foxnews.com",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 2 characters",
    }
    assert response.status_code == 422


def test_url_empty(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "Fawkes News",
            "source-url": "",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert response.status_code == 422


def test_all_fields_too_short(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "g",
            "author": "j",
            "publisher": "j",
            "source-url": "",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 2 characters",
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert response.status_code == 422


def test_textarea_too_short(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "j",
            "author": "Boris Newsman",
            "publisher": "Fawks",
            "source-url": "https://foxnews.com",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 10 characters",
    }
    assert response.status_code == 422


def test_author_too_short(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Puppy wins Nobel Prize and immediately eats it.",
            "author": "Me",
            "publisher": "Fawks",
            "source-url": "https://foxnews.com",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 5 characters",
    }
    assert response.status_code == 422


def test_publisher_too_short(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Puppy wins Nobel Prize and immediately eats it.",
            "author": "George Strombolopolous",
            "publisher": "C",
            "source-url": "https://foxnews.com",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "string_too_short": "String should have at least 2 characters",
    }
    assert response.status_code == 422


def test_url_invalid_string(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "Fawkes News",
            "source-url": "Behind ye old windmill",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "url_parsing": "Input should be a valid URL, relative URL without a base",
    }
    assert response.status_code == 422


def test_url_invalid_domain(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "Fawkes News",
            "source-url": "ftp://Behind ye old windmill",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "url_parsing": "Input should be a valid URL, invalid domain character",
    }
    assert response.status_code == 422


def test_url_invalid_characters(client):
    response = client.post(
        "/",
        data={
            "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
            "author": "Guy Fawkes",
            "publisher": "Fawkes News",
            "source-url": "http://@#%$&%$#%^$#@$",
        },
    )
    result = json.loads(response.text)
    assert result == {
        "url_parsing": "Input should be a valid URL, empty host",
    }
    assert response.status_code == 422
