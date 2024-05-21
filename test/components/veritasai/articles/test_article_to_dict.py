import pytest
from veritasai.articles import Article


def test_all_fields_serialized_if_exists():
    article = Article(
        id="123",
        author="John Doe",
        publisher="The New York Times",
        url="https://nytimes.com",
    )
    assert article.to_dict() == {
        "id": "123",
        "author": "John Doe",
        "publisher": "The New York Times",
        "url": "https://nytimes.com",
    }


@pytest.mark.parametrize(
    "field",
    ["author", "publisher", "url"],
)
def test_fields_not_serialized_when_missing(field):
    fields = {
        "id": "123",
        "author": "John Doe",
        "publisher": "The New York Times",
        "url": "https://nytimes.com",
    }
    del fields[field]
    article = Article(**fields)

    assert article.to_dict() == fields
