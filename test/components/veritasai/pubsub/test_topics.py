import pytest
from pytest import MonkeyPatch
from veritasai.pubsub.topics import topic_name_from_environment


def test_missing_environment_variable_without_default_raises_error():
    with pytest.raises(ValueError):
        topic_name_from_environment("TEST_TOPIC")


def test_missing_environment_variable_with_default_returns_default():
    assert topic_name_from_environment("TEST_TOPIC", "default") == "default"


def test_set_but_empty_environment_variable_raises_error(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("TEST_TOPIC", "")

    with pytest.raises(ValueError):
        topic_name_from_environment("TEST_TOPIC")


def test_set_and_non_empty_environment_variable_returns_value(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("TEST_TOPIC", "test-topic")

    assert topic_name_from_environment("TEST_TOPIC") == "test-topic"


def test_set_and_non_empty_environment_variable_with_default_returns_value(
    monkeypatch: MonkeyPatch,
):
    monkeypatch.setenv("TEST_TOPIC", "test-topic")

    assert topic_name_from_environment("TEST_TOPIC", "default") == "test-topic"


def test_set_and_non_empty_environment_variable_has_whitespace_removed(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("TEST_TOPIC", " test-topic ")

    assert topic_name_from_environment("TEST_TOPIC") == "test-topic"
