import json
from base64 import b64decode
from dataclasses import dataclass

from cloudevents.http import CloudEvent


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
