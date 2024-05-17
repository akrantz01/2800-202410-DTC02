from pytest_mock import MockerFixture
from veritasai.cache import has_article


def test_document_exists(mocker: MockerFixture):
    db = mocker.patch("veritasai.cache.db")
    db.collection.return_value.document.return_value.get.return_value.exists = True

    assert has_article("test-article-id")
    db.collection.assert_called_once_with("articles")
    db.collection.return_value.document.assert_called_once_with("test-article-id")


def test_document_does_not_exist(mocker: MockerFixture):
    db = mocker.patch("veritasai.cache.db")
    db.collection.return_value.document.return_value.get.return_value.exists = False

    assert not has_article("test-article-id")
    db.collection.assert_called_once_with("articles")
    db.collection.return_value.document.assert_called_once_with("test-article-id")
