import json
from base64 import b64encode
from datetime import datetime

import pytest
from cloudevents.http import CloudEvent
from pytest import FixtureRequest
from veritasai.protocol import Payload


@pytest.fixture
def cloud_event(request: FixtureRequest) -> CloudEvent:
    """
    Create a new CloudEvent for testing purposes.
    """
    marker = request.node.get_closest_marker("cloud_event")
    if not marker:
        raise ValueError("Test must be marked with `@pytest.mark.cloud_event`")

    if not isinstance(marker.args[0], dict):
        raise ValueError("CloudEvent marker must have a dictionary argument")

    serialized = json.dumps(marker.args[0])
    encoded = b64encode(serialized.encode()).decode()

    return CloudEvent(
        attributes={
            "specversion": "1.0",
            "type": "google.cloud.pubsub.topic.v1.messagePublished",
            "source": "//pubsub.googleapis.com/projects/testing/topic/test",
            "time": datetime.now().isoformat(),
        },
        data={"message": {"data": encoded}},
    )


def test_payloads_are_immutable():
    payload = Payload(id="some-id", author="Alice", publisher="Twitter", url="https://example.com")

    with pytest.raises(AttributeError):
        payload.id = "some-other-id"


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "author": "Alice",
        "publisher": "Twitter",
        "url": "https://example.com",
    }
)
def test_from_cloud_event(cloud_event: CloudEvent):
    assert Payload.from_cloud_event(cloud_event) == Payload(
        id="some-id",
        author="Alice",
        publisher="Twitter",
        url="https://example.com",
    )


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "publisher": "Twitter",
        "url": "https://example.com",
    }
)
def test_from_cloud_event_missing_author(cloud_event: CloudEvent):
    assert Payload.from_cloud_event(cloud_event) == Payload(
        id="some-id",
        publisher="Twitter",
        url="https://example.com",
    )


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "author": "Alice",
        "url": "https://example.com",
    }
)
def test_from_cloud_event_missing_publisher(cloud_event: CloudEvent):
    assert Payload.from_cloud_event(cloud_event) == Payload(
        id="some-id",
        author="Alice",
        url="https://example.com",
    )


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "author": "Alice",
        "publisher": "Twitter",
    }
)
def test_from_cloud_event_missing_url(cloud_event: CloudEvent):
    assert Payload.from_cloud_event(cloud_event) == Payload(
        id="some-id",
        author="Alice",
        publisher="Twitter",
    )


@pytest.mark.cloud_event({"id": "some-id"})
def test_from_cloud_event_minimal(cloud_event: CloudEvent):
    assert Payload.from_cloud_event(cloud_event) == Payload(
        id="some-id",
    )
