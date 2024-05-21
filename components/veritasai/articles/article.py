import json
from base64 import b64decode
from functools import cached_property

from cloudevents.http import CloudEvent

from .dedup import generate_id
from .storage import retrieve_content, save_content


class Article:
    """
    A representation of an article.

    Stores attributes of the article such as the content, author, publisher and URL. Additionally,
    a unique ID is generated for each article to provide content-based deduplication. The atricle
    content is stored externally in a storage bucket to reduce the size of the message.
    """

    def __init__(self, **kwargs: str | None):
        self.__author = kwargs.get("author")
        self.__publisher = kwargs.get("publisher")
        self.__url = kwargs.get("url")

        article_id = kwargs.get("id")
        content = kwargs.get("content")
        assert bool(article_id) ^ bool(content), "One of 'id' or 'content' must be provided."

        if article_id is not None:
            self.__id = article_id
            self.__content = None
        elif content is not None:
            self.__id = generate_id(content, self.__author, self.__publisher)
            self.__content = content
            save_content(self.__id, content)

    @classmethod
    def from_input(
        cls,
        content: str,
        author: str | None = None,
        publisher: str | None = None,
        url: str | None = None,
    ) -> "Article":
        """
        Create a new article from input data.

        :param content: the article's content
        :param author: the article's author, if any
        :param publisher: the article's publisher, if any
        :param url: the article's URL, if any
        :return: the created article
        """
        return cls(content=content, author=author, publisher=publisher, url=url)

    @classmethod
    def from_cloud_event(cls, event: CloudEvent) -> "Article":
        """
        Extract the payload from a Pub/Sub message.

        :param event: the source event
        :return: the extracted article
        """
        assert (
            event.get("type") == "google.cloud.pubsub.topic.v1.messagePublished"
        ), "invalid event type"

        raw = b64decode(event.data["message"]["data"])
        deserialized = json.loads(raw)

        assert "content" not in deserialized, "content must be stored externally"
        assert "id" in deserialized, "missing article ID"

        return cls(**deserialized)

    @property
    def id(self) -> str:
        """
        The unique ID of the article.
        """
        return self.__id

    @property
    def author(self) -> str | None:
        """
        The name of the article's author, if any.
        """
        return self.__author

    @property
    def publisher(self) -> str | None:
        """
        The name of the article's publisher, if any.
        """
        return self.__publisher

    @property
    def url(self) -> str | None:
        """
        Where the article can be found online, if available.
        """
        return self.__url

    @cached_property
    def content(self) -> str:
        """
        The content of the article.
        """
        if self.__content:
            return self.__content

        content = retrieve_content(self.__id)
        if content is None:
            raise ValueError(f"article {self.__id!r} not found")

        return content

    def __repr__(self) -> str:
        return (
            "Article("
            f"id={self.__id!r}, "
            f"author={self.__author!r}, "
            f"publisher={self.__publisher!r}, "
            f"url={self.__url!r}"
            ")"
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Article):
            return NotImplemented

        return self.__id == value.id
