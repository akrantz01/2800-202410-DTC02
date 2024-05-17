from veritasai.firebase import db


def has_article(article_id: str) -> bool:
    """
    Check if a document with the given ID exists in the database.

    :param article_id: the ID of the document to check
    :return: True if the document exists, False otherwise
    """
    document = db.collection("articles").document(article_id).get()
    return document.exists
