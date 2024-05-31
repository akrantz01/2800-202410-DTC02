from unittest.mock import MagicMock

from veritasai.summarizer.model import load_model
from vertexai.generative_models import HarmBlockThreshold


def test_uses_latest_model_version(mock_model: MagicMock):
    load_model()

    assert mock_model.called
    assert mock_model.call_args.kwargs.get("model_name") == "gemini-1.5-flash-001"


def test_blocks_only_egregious_safety_violations(mock_model: MagicMock):
    load_model()

    assert mock_model.called

    safety_settings = mock_model.call_args.kwargs.get("safety_settings")
    assert safety_settings is not None

    for setting in safety_settings.values():
        assert setting == HarmBlockThreshold.BLOCK_ONLY_HIGH


def test_load_model_caches_model(mock_model: MagicMock):
    load_model()
    load_model()

    assert mock_model.call_count == 1
    assert mock_model.called
