from pytest_mock import MockerFixture
from veritasai.cache import has_article


def test_document_exists(mocker: MockerFixture):
    db = mocker.MagicMock()
    db.collection.return_value.document.return_value.get.return_value.exists = True
    mocker.patch("veritasai.cache.get_db", return_value=db)

    assert has_article("test-article-id")
    db.collection.assert_called_once_with("articles")
    db.collection.return_value.document.assert_called_once_with("test-article-id")


def test_document_does_not_exist(mocker: MockerFixture):
    db = mocker.MagicMock()
    db.collection.return_value.document.return_value.get.return_value.exists = False
    mocker.patch("veritasai.cache.get_db", return_value=db)

    assert not has_article("test-article-id")
    db.collection.assert_called_once_with("articles")
    db.collection.return_value.document.assert_called_once_with("test-article-id")
