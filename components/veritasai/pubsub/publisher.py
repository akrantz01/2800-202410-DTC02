import json
from typing import Protocol

from google.cloud.pubsub import PublisherClient
from veritasai.config import env


class Serializable(Protocol):
    """
    Protocol for objects that can be serialized to a dictionary.
    """

    def to_dict(self) -> dict:
        """
        Serialize the object to a dictionary.
        """
        ...


class Publisher:
    """
    Publishes messages to a topic.
    """

    def __init__(self, topic: str, project: str | None = None):
        """
        Initialize a publisher.

        The project ID is automatically determined from the environment when available. If it is not
        available, it must be provided.using the GOOGLE_CLOUD_PROJECT environment variable.

        :param topic: The name of the topic to publish to.
        :param project: The name of the project that owns the topic.
        """

        if project is None:
            project = env.get("GOOGLE_CLOUD_PROJECT")
        if project is None:
            raise ValueError("unknown project ID")

        self.__topic = f"projects/{project}/topics/{topic}"
        self.__client = PublisherClient()

    @property
    def topic(self) -> str:
        """
        The fully qualified name of the topic.
        """
        return self.__topic

    def publish(self, message: Serializable):
        """
        Publish the message to the appropriate topic.

        :param message: The message to publish.
        """
        data = json.dumps(message.to_dict()).encode("utf-8")
        result = self.__client.publish(topic=self.__topic, data=data)

        result.result()
