from base64 import urlsafe_b64encode
from hashlib import sha3_256


def generate(content: str, author: str | None = None, source: str | None = None) -> str:
    """
    Generate a document ID from the content, author and source.

    The generated document ID ignores leading and trailing whitespace in the content, author and
    source. It should be treated as an opaque identifier.

    :param content: The content of the document.
    :param author: The optional author of the document.
    :param source: The optional source of the document.
    :return: The document id.
    """
    content = content.strip()
    author = author.strip() if author else ""
    source = source.strip() if source else ""

    data = "|".join([content, author, source]).encode("utf-8")
    hash_bytes = sha3_256(data).digest()
    return urlsafe_b64encode(hash_bytes).decode("utf-8")
