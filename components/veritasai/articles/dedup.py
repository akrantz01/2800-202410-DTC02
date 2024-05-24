from base64 import urlsafe_b64encode
from hashlib import sha3_256


def generate_id(content: str, author: str | None = None, source: str | None = None) -> str:
    """
    Generate a unique ID for an article from its content, author and source.

    The generated ID ignores leading and trailing whitespace in the content, author and source. It
    should be treated as an opaque identifier.

    :param content: The content of the article.
    :param author: The optional author of the article.
    :param source: The optional source of the article.
    :return: The unique id.
    """
    content = content.strip()
    author = author.strip() if author else ""
    source = source.strip() if source else ""

    data = "|".join([content, author, source]).encode("utf-8")
    hash_bytes = sha3_256(data).digest()
    return urlsafe_b64encode(hash_bytes).decode("utf-8")
