from google.cloud import storage
from google.cloud.exceptions import NotFound, PreconditionFailed
from veritasai.config import env

_client = None


def _get_client() -> storage.Client:
    """
    Get the storage client.

    Automatically creates a new client if one does not already exist.

    :return: the storage client
    """
    global _client

    if _client is None:
        _client = storage.Client()

    return _client


def _get_bucket() -> storage.Bucket:
    """
    Get the storage bucket.

    Retrieves the bucket as configured by the ARTICLES_BUCKET environment variable.

    :return: the storage bucket
    """
    client = _get_client()

    bucket_name = env.get("ARTICLES_BUCKET")
    if bucket_name is None:
        raise ValueError("environment variable ARTICLES_BUCKET is not set")

    return client.bucket(bucket_name)


def save_content(article_id: str, content: str):
    """
    Save the content of an article to a storage bucket.

    :param article_id: the article's unique ID
    :param content: the article's content
    """
    bucket = _get_bucket()
    blob = bucket.blob(article_id)

    try:
        blob.upload_from_string(content, content_type="text/plain", if_generation_match=0)
    except PreconditionFailed:
        # Already uploaded, nothing to do
        pass


def retrieve_content(article_id: str) -> str | None:
    """
    Retrieve the content of an article from a storage bucket.

    :param article_id: the article's unique ID
    :return: the article's content, or None if the article does not exist
    """
    bucket = _get_bucket()
    blob = bucket.blob(article_id)

    try:
        return blob.download_as_string().decode("utf-8")
    except NotFound:
        return None
