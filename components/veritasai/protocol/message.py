import json
from base64 import b64decode
from dataclasses import dataclass
from functools import cached_property

from cloudevents.http import CloudEvent

from .storage import retrieve_content, save_content


@dataclass(frozen=True)
class Payload:
    """
    The payload sent from the analysis-manager to individual analyzers.
    """

    id: str
    author: str | None = None
    publisher: str | None = None
    url: str | None = None

    @classmethod
    def create(
        cls,
        article_id: str,
        content: str,
        author: str | None = None,
        publisher: str | None = None,
        url: str | None = None,
    ) -> "Payload":
        """
        Create a new Pub/Sub message payload.

        Article content is stored externally in a storage bucket to reduce the size of the message.

        :param article_id: the unique ID of the article
        :param content: the article's content
        :param author: the article's author, if any
        :param publisher: the article's publisher, if any
        :param url: the article's URL, if any
        :return: the created payload
        """
        save_content(article_id, content)

        return cls(id=article_id, author=author, publisher=publisher, url=url)

    @classmethod
    def from_cloud_event(cls, event: CloudEvent) -> "Payload":
        """
        Extract the payload from a Pub/Sub message.

        :param event: the source event
        :return: the sent payload
        """
        assert event.get("type") == "google.cloud.pubsub.topic.v1.messagePublished"

        raw = b64decode(event.data["message"]["data"])
        deserialized = json.loads(raw)

        return cls(**deserialized)

    @cached_property
    def content(self) -> str:
        """
        Retrieve the externally stored article content from the storage bucket.
        """
        content = retrieve_content(self.id)
        if content is None:
            raise ValueError(f"article {self.id!r} not found")

        return content
