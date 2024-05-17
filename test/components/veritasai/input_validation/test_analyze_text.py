import pytest
from pydantic import ValidationError
from veritasai.input_validation import AnalyzeText


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


def validate(raw):
    try:
        AnalyzeText.model_validate(raw)
    except ValidationError as e:
        return e.errors()


def test_valid_input(data: dict[str, str]):
    assert validate(data) is None


def test_missing_fields():
    assert validate({}) == [
        {
            "input": {},
            "loc": ("content",),
            "msg": "Field required",
            "type": "missing",
            "url": "https://errors.pydantic.dev/2.7/v/missing",
        },
    ]


def test_all_fields_empty():
    data = {"content": "", "author": "", "publisher": "", "source-url": ""}
    assert validate(data) == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": ("content",),
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "min_length": 2,
            },
            "input": "",
            "loc": ("author",),
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": ("publisher",),
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
        {
            "ctx": {
                "error": "input is empty",
            },
            "input": "",
            "loc": ("source-url",),
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_content_empty(data: dict[str, str]):
    data["content"] = ""
    assert validate(data) == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": ("content",),
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_author_empty(data: dict[str, str]):
    data["author"] = ""
    assert validate(data) == [
        {
            "ctx": {
                "min_length": 2,
            },
            "input": "",
            "loc": ("author",),
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_publisher_empty(data: dict[str, str]):
    data["publisher"] = ""
    assert validate(data) == [
        {
            "ctx": {
                "min_length": 5,
            },
            "input": "",
            "loc": ("publisher",),
            "msg": "String should have at least 5 characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_url_empty(data: dict[str, str]):
    data["source-url"] = ""
    assert validate(data) == [
        {
            "ctx": {
                "error": "input is empty",
            },
            "input": "",
            "loc": ("source-url",),
            "msg": "Input should be a valid URL, input is empty",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


@pytest.mark.parametrize("field,length", [("content", 5), ("author", 2), ("publisher", 5)])
def test_field_too_short(data, field, length):
    data[field] = "a" * (length - 1)
    assert validate(data) == [
        {
            "ctx": {
                "min_length": length,
            },
            "input": "a" * (length - 1),
            "loc": (field,),
            "msg": f"String should have at least {length} characters",
            "type": "string_too_short",
            "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
        },
    ]


def test_url_invalid_format(data: dict[str, str]):
    data["source-url"] = "Behind ye old windmill"
    assert validate(data) == [
        {
            "ctx": {
                "error": "relative URL without a base",
            },
            "input": "Behind ye old windmill",
            "loc": ("source-url",),
            "msg": "Input should be a valid URL, relative URL without a base",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_url_invalid_domain(data: dict[str, str]):
    data["source-url"] = "http://Behind ye old windmill"
    assert validate(data) == [
        {
            "ctx": {
                "error": "invalid domain character",
            },
            "input": "http://Behind ye old windmill",
            "loc": ("source-url",),
            "msg": "Input should be a valid URL, invalid domain character",
            "type": "url_parsing",
            "url": "https://errors.pydantic.dev/2.7/v/url_parsing",
        },
    ]


def test_url_invalid_characters(data: dict[str, str]):
    data["source-url"] = "ttp://#*@)($#$)"
    assert validate(data) == [
        {
            "ctx": {
                "expected_schemes": "'http' or 'https'",
            },
            "input": "ttp://#*@)($#$)",
            "loc": ("source-url",),
            "msg": "URL scheme should be 'http' or 'https'",
            "type": "url_scheme",
            "url": "https://errors.pydantic.dev/2.7/v/url_scheme",
        },
    ]
