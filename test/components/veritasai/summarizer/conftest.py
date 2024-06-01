import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture


@pytest.fixture
def mock_model(mocker: MockerFixture):
    """
    Mock the generative model for summarization.
    """
    return mocker.patch("veritasai.summarizer.model.GenerativeModel")


@pytest.fixture(autouse=True)
def ensure_load_model_does_not_persist_state(monkeypatch: MonkeyPatch):
    """
    Ensure that the `load_model` function does not persist state between tests.

    This is important to ensure that each test case is isolated from one another.
    """
    monkeypatch.setattr("veritasai.summarizer.model._model", None)
