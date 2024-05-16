import json

import requests


def test_all_fields_empty():
    form_data = {"text-to-analyze": "", "author": "", "publisher": "", "source-url": ""}
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 2 characters",
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert result.status_code == 422


def test_textarea_empty():
    form_data = {
        "text-to-analyze": "",
        "author": "Boris Newsman",
        "publisher": "Fawks",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 10 characters",
    }
    assert result.status_code == 422


def test_author_empty():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "",
        "publisher": "Fawks",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 5 characters",
    }
    assert result.status_code == 422


def test_publisher_empty():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 2 characters",
    }
    assert result.status_code == 422


def test_url_empty():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "Fawkes News",
        "source-url": "",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert result.status_code == 422


def test_all_fields_too_short():
    form_data = {
        "text-to-analyze": "g",
        "author": "j",
        "publisher": "j",
        "source-url": "",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 2 characters",
        "url_parsing": "Input should be a valid URL, input is empty",
    }
    assert result.status_code == 422


def test_textarea_too_short():
    form_data = {
        "text-to-analyze": "j",
        "author": "Boris Newsman",
        "publisher": "Fawks",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 10 characters",
    }
    assert result.status_code == 422


def test_author_too_short():
    form_data = {
        "text-to-analyze": "Puppy wins Nobel Prize and immediately eats it.",
        "author": "Me",
        "publisher": "Fawks",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 5 characters",
    }
    assert result.status_code == 422


def test_publisher_too_short():
    form_data = {
        "text-to-analyze": "Puppy wins Nobel Prize and immediately eats it.",
        "author": "George Strombolopolous",
        "publisher": "C",
        "source-url": "https://foxnews.com",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "string_too_short": "String should have at least 2 characters",
    }
    assert result.status_code == 422


def test_url_invalid_string():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "Fawkes News",
        "source-url": "Behind ye old windmill",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "url_parsing": "Input should be a valid URL, relative URL without a base",
    }
    assert result.status_code == 422


def test_url_invalid_domain():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "Fawkes News",
        "source-url": "ftp://Behind ye old windmill",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "url_parsing": "Input should be a valid URL, invalid domain character",
    }
    assert result.status_code == 422


def test_url_invalid_characters():
    form_data = {
        "text-to-analyze": "Yesterday's news tomorrow, Tonight at 5.",
        "author": "Guy Fawkes",
        "publisher": "Fawkes News",
        "source-url": "http://@#%$&%$#%^$#@$",
    }
    result = requests.post("http://localhost:8080", data=form_data)
    result_json = json.loads(result.text)
    assert result_json == {
        "url_parsing": "Input should be a valid URL, empty host",
    }
    assert result.status_code == 422
