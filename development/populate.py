from veritasai.firebase import get_db


def assign_article(article_id: str) -> None:
    article_ref = get_db().collection("articles").document(article_id)
    article_doc = article_ref.get()
    if not article_doc:
        raise KeyError("Article ID does not exist")
    # article = article_doc.to_dict()


def author_exists(author: str) -> bool:
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        return (
            True
            if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower()
            else False
        )


def publisher_exists(publisher: str) -> bool:
    publishers_ref = get_db().collection("publishers").stream()
    for publishers in publishers_ref:
        return (
            True
            if publishers.to_dict()["name"].replace(" ", "").lower()
            == publisher.replace(" ", "").lower()
            else False
        )


def main():
    print(author_exists("Johnsmith   "))
    print(publisher_exists("Old Fashioned News"))


if __name__ == "__main__":
    main()
