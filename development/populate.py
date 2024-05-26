from veritasai.firebase import get_db

# def assign_article(article_id: str) -> None:
#     article_ref = get_db().collection("articles").document(article_id)
#     authors_ref = get_db().collection("authors")
#     publishers_ref = get_db().collection("publishers")


def author_exists(author: str) -> bool:
    authors_ref = get_db().collection("authors").stream()
    for authors in authors_ref:
        return (
            True
            if authors.to_dict()["name"].replace(" ", "").lower() == author.replace(" ", "").lower()
            else False
        )


def main():
    print(author_exists("Johnsmith   "))


if __name__ == "__main__":
    main()
