import json
from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch
from veritasai.pubsub.publisher import Publisher


def test_raises_error_when_project_id_is_undefined(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("veritasai.pubsub.publisher.project_id", None)

    with pytest.raises(ValueError):
        Publisher("topic")


def test_pulls_project_id_from_environment_when_available():
    publisher = Publisher("topic")
    assert publisher.topic == "projects/test-project/topics/topic"


def test_uses_explicit_project_id_when_provided():
    publisher = Publisher("topic", "some-project")
    assert publisher.topic == "projects/some-project/topics/topic"


def test_formats_topic_name_correctly():
    publisher = Publisher("some-topic", "some-project")
    assert publisher.topic == "projects/some-project/topics/some-topic"


@pytest.fixture
def publisher():
    """
    Create a publisher for testing.
    """
    return Publisher("topic")


def test_publish_publishes_message_to_topic(publisher: Publisher, mock_pubsub: MagicMock):
    message = MagicMock(**{"to_dict.return_value": {"key": "value"}})
    publisher.publish(message)

    mock_pubsub.return_value.publish.assert_called_once_with(
        topic="projects/test-project/topics/topic", data=b'{"key": "value"}'
    )


def test_publish_sends_valid_json(publisher: Publisher, mock_pubsub: MagicMock):
    data = {"key": "value"}
    message = MagicMock(**{"to_dict.return_value": data})

    publisher.publish(message)

    encoded = mock_pubsub.return_value.publish.call_args[1]["data"].decode("utf-8")
    assert json.loads(encoded) == data


def test_publish_waits_for_publish_to_complete(publisher: Publisher, mock_pubsub: MagicMock):
    publisher.publish(MagicMock(**{"to_dict.return_value": {}}))

    mock_pubsub.return_value.publish.return_value.result.assert_called_once()
