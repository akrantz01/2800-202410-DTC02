import pytest
from veritasai.articles import Article


@pytest.mark.parametrize("field", ["id", "author", "publisher", "url"])
def test_is_immutable(field: str):
    article = Article(
        id="some-id",
        author="Alice",
        publisher="Twitter",
        url="https://example.com",
    )

    with pytest.raises(AttributeError):
        setattr(article, field, "new-value")


def test_constructor_requires_one_of_id_or_content():
    with pytest.raises(AssertionError, match="One of 'id' or 'content' must be provided."):
        Article(id="some-id", content="Hello, world!")
