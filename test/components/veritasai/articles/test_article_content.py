import pytest
from pytest_mock import MockerFixture
from veritasai.articles import Article


def test_does_not_attempt_to_fetch_remote_content_when_content_is_provided(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    save_conent = mocker.patch("veritasai.articles.article.save_content")

    payload = Article(content="Hello, world!")
    assert payload.content == "Hello, world!"

    retrieve_content.assert_not_called()
    save_conent.assert_called_once()


def test_remote_content_exists(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    retrieve_content.return_value = "Hello, world!"

    payload = Article(id="some-id")
    assert payload.content == "Hello, world!"

    retrieve_content.assert_called_once_with("some-id")


def test_raises_when_remote_content_does_not_exist(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    retrieve_content.return_value = None

    payload = Article(id="some-id")
    with pytest.raises(ValueError, match="article 'some-id' not found"):
        _ = payload.content

    retrieve_content.assert_called_once_with("some-id")


def test_caches_result(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    retrieve_content.return_value = "Hello, world!"

    payload = Article(id="some-id")
    for _ in range(3):
        assert payload.content == "Hello, world!"

    retrieve_content.assert_called_once_with("some-id")


def test_does_not_cache_when_remote_content_does_not_exist(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    retrieve_content.return_value = None

    payload = Article(id="some-id")
    for _ in range(3):
        with pytest.raises(ValueError):
            _ = payload.content

    retrieve_content.assert_called_with("some-id")
    assert retrieve_content.call_count == 3


def test_raises_when_remote_content_does_not_exists_then_caches_once_exists(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.articles.article.retrieve_content")
    retrieve_content.side_effect = [None, "Hello, world!"]

    payload = Article(id="some-id")
    with pytest.raises(ValueError):
        _ = payload.content

    for _ in range(3):
        assert payload.content == "Hello, world!"

    retrieve_content.assert_has_calls([mocker.call("some-id"), mocker.call("some-id")])
    assert retrieve_content.call_count == 2
