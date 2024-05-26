from firebase_admin import firestore
from veritasai.firebase import get_db


def assign_article(article_id: str) -> None:
    article_ref = get_db().collection("articles").document(article_id)
    article_doc = article_ref.get()
    if not article_doc:
        raise KeyError("Article ID does not exist")
    article = article_doc.to_dict()
    if not author_exists(article["author"]):
        if not publisher_exists(article["publisher"]):
            create_publisher(article, article_id)
        create_author(article, article_id)
    else:
        author_id = get_author_id(article["author"])
        publisher_id = get_publisher_id(article["publisher"])
        publisher_ref = get_db().collection("publishers").document(publisher_id)
        publisher_ref.update(
            {
                "authors": firestore.ArrayUnion([author_id]),
                "articles": firestore.ArrayUnion([article_id]),
            }
        )
        author_ref = get_db().collection("authors").document(author_id)
        author_ref.update(
            {
                "publishedFor": firestore.ArrayUnion([publisher_id]),
                "articles": firestore.ArrayUnion([article_id]),
            }
        )


def author_exists(author: str) -> bool:
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        return (
            True
            if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower()
            else False
        )


def create_author(article: dict, article_id: str) -> None:
    publishers_ref = get_db().collection("publishers").stream()
    for publisher in publishers_ref:
        if (
            publisher.to_dict()["name"].replace(" ", "").lower()
            == article["publisher"].replace(" ", "").lower()
        ):
            author = {
                "aiScore": article["aiScore"],
                "biasScore": article["biasScore"],
                "articles": [article_id],
                "name": article["author"],
                "publishedFor": [publisher.id],
            }
            timestamp, author_ref = get_db().collection("authors").add(author)
            publisher_ref = get_db().collection("publishers").document(publisher.id)
            publisher_ref.update({"authors": firestore.ArrayUnion([author_ref.id])})


def publisher_exists(publisher: str) -> bool:
    publishers_ref = get_db().collection("publishers").stream()
    for publishers in publishers_ref:
        return (
            True
            if publishers.to_dict()["name"].replace(" ", "").lower()
            == publisher.replace(" ", "").lower()
            else False
        )


def create_publisher(article: dict, article_id: str) -> None:
    publisher = {
        "aiScore": article["aiScore"],
        "biasScore": article["biasScore"],
        "articles": [article_id],
        "name": article["publisher"],
        "authors": [],
    }
    get_db().collection("publishers").add(publisher)


def get_publisher_id(publisher: str) -> str:
    publishers_ref = get_db().collection("publishers").stream()
    for publishers in publishers_ref:
        if (
            publishers.to_dict()["name"].replace(" ", "").lower()
            == publisher.replace(" ", "").lower()
        ):
            return publishers.id


def get_author_id(author: str) -> str:
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower():
            return authors.id


def main():
    # article = {
    #     "aiScore": 0.69,
    #     "biasScore": 0.420,
    #     "publisher": "Questionable News",
    #     "author": "John Smith",
    # }
    # print(author_exists("Johnsmith   "))
    # print(publisher_exists("Old Fashioned News"))
    # create_publisher(article, "demo")
    # create_author(article, "demo")
    print(get_publisher_id("Questionable News"))
    assign_article("demo")


if __name__ == "__main__":
    main()
