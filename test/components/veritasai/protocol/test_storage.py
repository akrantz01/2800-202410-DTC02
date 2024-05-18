import pytest
from google.cloud.exceptions import NotFound, PreconditionFailed
from pytest import MonkeyPatch
from pytest_mock import MockerFixture
from veritasai.protocol.storage import retrieve_content, save_content


@pytest.fixture(autouse=True)
def set_articles_bucket(monkeypatch: MonkeyPatch):
    """
    Set the ARTICLES_BUCKET environment variable to "test-bucket".
    """
    with monkeypatch.context() as m:
        m.setenv("ARTICLES_BUCKET", "test-bucket")

        yield


def test_save_content(mocker: MockerFixture):
    client = mocker.MagicMock()
    mocker.patch("veritasai.protocol.storage._get_client", return_value=client)

    save_content("test-article-id", "Hello, world!")

    client.bucket.assert_called_once_with("test-bucket")
    client.bucket.return_value.blob.assert_called_once_with("test-article-id")
    client.bucket.return_value.blob.return_value.upload_from_string.assert_called_once_with(
        "Hello, world!",
        content_type="text/plain",
        if_generation_match=0,
    )


def test_save_content_when_already_exists(mocker: MockerFixture):
    client = mocker.MagicMock()
    client.bucket.return_value.blob.return_value.upload_from_string.side_effect = (
        PreconditionFailed("id")
    )
    mocker.patch("veritasai.protocol.storage._get_client", return_value=client)

    save_content("test-article-id", "Hello, world!")

    client.bucket.assert_called_once_with("test-bucket")
    client.bucket.return_value.blob.assert_called_once_with("test-article-id")
    client.bucket.return_value.blob.return_value.upload_from_string.assert_called_once_with(
        "Hello, world!",
        content_type="text/plain",
        if_generation_match=0,
    )


def test_retrieve_content_when_exists(mocker: MockerFixture):
    client = mocker.MagicMock()
    client.bucket.return_value.blob.return_value.exists.return_value = True
    client.bucket.return_value.blob.return_value.download_as_string.return_value = b"Hello, world!"
    mocker.patch("veritasai.protocol.storage._get_client", return_value=client)

    assert retrieve_content("test-article-id") == "Hello, world!"

    client.bucket.assert_called_once_with("test-bucket")
    client.bucket.return_value.blob.assert_called_once_with("test-article-id")
    client.bucket.return_value.blob.return_value.download_as_string.assert_called_once()


def test_retrieve_content_when_does_not_exist(mocker: MockerFixture):
    client = mocker.MagicMock()
    client.bucket.return_value.blob.return_value.download_as_string.side_effect = NotFound("id")
    mocker.patch("veritasai.protocol.storage._get_client", return_value=client)

    assert retrieve_content("test-article-id") is None

    client.bucket.assert_called_once_with("test-bucket")
    client.bucket.return_value.blob.assert_called_once_with("test-article-id")
    client.bucket.return_value.blob.return_value.download_as_string.assert_called_once()
