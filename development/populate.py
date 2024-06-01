from firebase_admin import firestore
from veritasai.firebase import get_db


def assign_article(article_id: str) -> None:
    """
    Assign an article to an author and publisher.

    If an author doesn't exist, an author will be created. If a publisher doesn't exist, a publisher
    will be created. Publishers are always created before authors, so an author will not exist
    without a publisher.

    :param article_id: a string for the article id of the article that was just created
    :raises KeyError: if the article does not exist in the DB
    """
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
        # update ai/bias score
        publisher_ref.update(
            {
                "authors": firestore.ArrayUnion([author_id]),
                "articles": firestore.ArrayUnion([article_id]),
            }
        )
        author_ref = get_db().collection("authors").document(author_id)
        # update ai/bias score
        author_ref.update(
            {
                "publishedFor": firestore.ArrayUnion([publisher_id]),
                "articles": firestore.ArrayUnion([article_id]),
            }
        )


def author_exists(author: str) -> bool:
    """
    Check if the author exists in the DB.

    :param author: The author name
    """
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        return (
            True
            if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower()
            else False
        )


def create_author(article: dict, article_id: str) -> None:
    """
    Create an author in the DB.

    :param article: a dictionary representing the article from the DB
    :param article_id: the article id
    """
    ai_score = 0
    bias_score = 0
    if "ai" in article:
        ai_score = article["ai"]["aiScore"]
    if "bias" in article:
        bias_score = article["bias"]["aiScore"]
    publishers_ref = get_db().collection("publishers").stream()
    for publisher in publishers_ref:
        if (
            publisher.to_dict()["name"].replace(" ", "").lower()
            == article["publisher"].replace(" ", "").lower()
        ):
            author = {
                "aiScore": ai_score,
                "biasScore": bias_score,
                "articles": [article_id],
                "name": article["author"],
                "publishedFor": [publisher.id],
            }
            timestamp, author_ref = get_db().collection("authors").add(author)
            publisher_ref = get_db().collection("publishers").document(publisher.id)
            publisher_ref.update({"authors": firestore.ArrayUnion([author_ref.id])})


def publisher_exists(publisher: str) -> bool:
    """
    Check if the publisher exists in the DB.

    :param publisher: The publisher name
    """
    publishers_ref = get_db().collection("publishers").stream()
    for publishers in publishers_ref:
        return (
            True
            if publishers.to_dict()["name"].replace(" ", "").lower()
            == publisher.replace(" ", "").lower()
            else False
        )


def create_publisher(article: dict, article_id: str) -> None:
    """
    Create a publisher in the DB.

    :param article: a dictionary representing the article from the DB
    :param article_id: the article id
    """
    ai_score = 0
    bias_score = 0
    if "ai" in article:
        ai_score = article["ai"]["aiScore"]
    if "bias" in article:
        bias_score = article["bias"]["aiScore"]
    publisher = {
        "aiScore": ai_score,
        "biasScore": bias_score,
        "articles": [article_id],
        "name": article["publisher"],
        "authors": [],
    }
    get_db().collection("publishers").add(publisher)


def get_publisher_id(publisher: str) -> str:
    """
    Get the publisher ID.

    :param publisher: the publisher name
    :return: publisher ID as a string
    """
    publishers_ref = get_db().collection("publishers").stream()
    for publishers in publishers_ref:
        if (
            publishers.to_dict()["name"].replace(" ", "").lower()
            == publisher.replace(" ", "").lower()
        ):
            return publishers.id


def get_author_id(author: str) -> str:
    """
    Get the author ID.

    :param author: the author name
    :return: author ID as a string
    """
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower():
            return authors.id


def add_history(article_id: str, user_id: str) -> None:
    """
    Add the article to the users history.

    :param article_id: the firestore id of the article
    :param user_id: the firestore id of the user
    """
    get_db().collection("users").document(user_id).collection("history").document(article_id).set(
        {"dateScanned": firestore.SERVER_TIMESTAMP}
    )


def update_author_bias(author_id: str = "", author_name: str = "") -> None:
    """
    Update the author bias score in firestore.

    :param author_id" the firestore id for the author - optional
    :param author_name" the name of the author if id is not available - optional - overrides id
    """
    if author_name:
        author_id = get_author_id(author_name)
    author_ref = get_db().collection("authors").document(author_id)
    author = author_ref.get().to_dict()
    total_score = 0
    total_count = 0
    for article in author["articles"]:
        total_score += float(
            get_db().collection("articles").document(article).get().to_dict()["bias"]["biasScore"]
        )
        total_count += 1
    author_ref.update({"biasScore": total_score / total_count})


def update_author_ai(author_id: str = "", author_name: str = "") -> None:
    """
    Update the author ai score in firestore.

    :param author_id" the firestore id for the author - optional
    :param author_name" the name of the author if id is not available - optional - overrides id
    """
    if author_name:
        author_id = get_author_id(author_name)
    author_ref = get_db().collection("authors").document(author_id)
    author = author_ref.get().to_dict()
    total_score = 0
    total_count = 0
    for article in author["articles"]:
        total_score += float(
            get_db().collection("articles").document(article).get().to_dict()["ai"]["aiScore"]
        )
        total_count += 1
    author_ref.update({"aiScore": total_score / total_count})


def update_publisher_bias(publisher_id: str = "", publisher_name: str = "") -> None:
    """
    Update the publisher bias score in firestore.

    :param publisher_id" the firestore id for the publisher - optional
    :param publisher_name: the name of the publisher if id is not available
                          - optional - overrides id
    """
    if publisher_name:
        publisher_id = get_publisher_id(publisher_name)
    publisher_ref = get_db().collection("publishers").document(publisher_id)
    publisher = publisher_ref.get().to_dict()
    total_score = 0
    total_count = 0
    for article in publisher["articles"]:
        total_score += float(
            get_db().collection("articles").document(article).get().to_dict()["bias"]["biasScore"]
        )
        total_count += 1
    publisher_ref.update({"biasScore": total_score / total_count})


def update_publisher_ai(publisher_id: str = "", publisher_name: str = "") -> None:
    """
    Update the publisher ai score in firestore.

    :param publisher_id" the firestore id for the publisher - optional
    :param publisher_name: the name of the publisher if id is not available
                          - optional - overrides id
    """
    if publisher_name:
        publisher_id = get_publisher_id(publisher_name)
    publisher_ref = get_db().collection("publishers").document(publisher_id)
    publisher = publisher_ref.get().to_dict()
    total_score = 0
    total_count = 0
    for article in publisher["articles"]:
        total_score += float(
            get_db().collection("articles").document(article).get().to_dict()["ai"]["aiScore"]
        )
        total_count += 1
    publisher_ref.update({"aiScore": total_score / total_count})


def main():
    """
    Drive the program.
    """
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
    # print(get_publisher_id("Questionable News"))
    # assign_article("demo")
    # add_history("demo", "K8n5TZsfPogedpftAREoQVhJ7Dc2")
    update_publisher_ai(publisher_name="Fun Time News")


if __name__ == "__main__":
    main()
