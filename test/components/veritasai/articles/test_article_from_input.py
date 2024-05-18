import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture
from veritasai.articles import Article


@pytest.fixture(autouse=True)
def mock_generate_id(monkeypatch: MonkeyPatch):
    """
    Mock the generate_id function to return a fixed value.
    """

    with monkeypatch.context() as m:
        m.setattr("veritasai.articles.article.generate_id", lambda *_: "some-id")
        yield


def test_minimal_input(mocker: MockerFixture):
    save_content = mocker.patch("veritasai.articles.article.save_content")

    assert Article.from_input("Hello, world!") == Article(id="some-id")

    save_content.assert_called_once_with("some-id", "Hello, world!")


def test_full_input(mocker: MockerFixture):
    save_content = mocker.patch("veritasai.articles.article.save_content")

    assert Article.from_input(
        "Hello, world!",
        "Alice",
        "Twitter",
        "https://example.com",
    ) == Article(
        id="some-id",
        author="Alice",
        publisher="Twitter",
        url="https://example.com",
    )

    save_content.assert_called_once_with("some-id", "Hello, world!")
