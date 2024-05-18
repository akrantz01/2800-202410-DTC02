import json
from base64 import b64encode
from datetime import datetime

import pytest
from cloudevents.http import CloudEvent
from pytest import FixtureRequest
from pytest_mock import MockerFixture
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


def test_create(mocker: MockerFixture):
    save_content = mocker.patch("veritasai.protocol.message.save_content")

    payload = Payload.create("some-id", "Hello, world!", "Alice", "Twitter", "https://example.com")

    assert payload == Payload(
        id="some-id",
        author="Alice",
        publisher="Twitter",
        url="https://example.com",
    )
    save_content.assert_called_once_with("some-id", "Hello, world!")


def test_create_minimal(mocker: MockerFixture):
    save_content = mocker.patch("veritasai.protocol.message.save_content")

    payload = Payload.create("some-id", "Hello, world!")

    assert payload == Payload(id="some-id")
    save_content.assert_called_once_with("some-id", "Hello, world!")


def test_content_property_when_exists(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.protocol.message.retrieve_content")
    retrieve_content.return_value = "Hello, world!"

    payload = Payload(id="some-id")
    assert payload.content == "Hello, world!"

    retrieve_content.assert_called_once_with("some-id")


def test_content_property_raises_when_does_not_exist(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.protocol.message.retrieve_content")
    retrieve_content.return_value = None

    payload = Payload(id="some-id")
    with pytest.raises(ValueError, match="article 'some-id' not found"):
        _ = payload.content

    retrieve_content.assert_called_once_with("some-id")


def test_content_property_cached(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.protocol.message.retrieve_content")
    retrieve_content.return_value = "Hello, world!"

    payload = Payload(id="some-id")
    for _ in range(3):
        assert payload.content == "Hello, world!"

    retrieve_content.assert_called_once_with("some-id")


def test_content_property_does_not_cache_when_does_not_exist(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.protocol.message.retrieve_content")
    retrieve_content.return_value = None

    payload = Payload(id="some-id")
    for _ in range(3):
        with pytest.raises(ValueError):
            _ = payload.content

    retrieve_content.assert_called_with("some-id")
    assert retrieve_content.call_count == 3


def test_content_property_raises_when_not_exists_then_caches_once_exists(mocker: MockerFixture):
    retrieve_content = mocker.patch("veritasai.protocol.message.retrieve_content")
    retrieve_content.side_effect = [None, "Hello, world!"]

    payload = Payload(id="some-id")
    with pytest.raises(ValueError):
        _ = payload.content

    for _ in range(3):
        assert payload.content == "Hello, world!"

    retrieve_content.assert_has_calls([mocker.call("some-id"), mocker.call("some-id")])
    assert retrieve_content.call_count == 2
