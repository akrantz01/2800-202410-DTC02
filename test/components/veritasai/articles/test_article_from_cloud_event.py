import json
from base64 import b64encode
from datetime import datetime

import pytest
from cloudevents.http import CloudEvent
from pytest import FixtureRequest
from veritasai.articles import Article


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


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "author": "Alice",
        "publisher": "Twitter",
        "url": "https://example.com",
    }
)
def test_from_cloud_event(cloud_event: CloudEvent):
    assert Article.from_cloud_event(cloud_event) == Article(
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
    assert Article.from_cloud_event(cloud_event) == Article(
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
    assert Article.from_cloud_event(cloud_event) == Article(
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
    assert Article.from_cloud_event(cloud_event) == Article(
        id="some-id",
        author="Alice",
        publisher="Twitter",
    )


@pytest.mark.cloud_event(
    {
        "author": "Alice",
        "publisher": "Twitter",
        "url": "https://example.com",
    }
)
def test_events_without_ids_are_rejected(cloud_event: CloudEvent):
    with pytest.raises(AssertionError, match="missing article ID"):
        Article.from_cloud_event(cloud_event)


@pytest.mark.cloud_event(
    {
        "id": "some-id",
        "author": "Alice",
        "publisher": "Twitter",
        "url": "https://example.com",
        "content": "Hello, world!",
    }
)
def test_messages_with_inline_content_are_rejected(cloud_event: CloudEvent):
    with pytest.raises(AssertionError, match="content must be stored externally"):
        Article.from_cloud_event(cloud_event)


def test_non_pubsub_events_are_rejected():
    event = CloudEvent(
        attributes={
            "specversion": "1.0",
            "type": "google.cloud.storage.object.v1.finalized",
            "source": "//storage.googleapis.com/projects/_/buckets/MY-BUCKET-NAME",
            "time": datetime.now().isoformat(),
        },
        data={"message": {"data": "dGVzdA=="}},
    )

    with pytest.raises(AssertionError, match="invalid event type"):
        Article.from_cloud_event(event)
