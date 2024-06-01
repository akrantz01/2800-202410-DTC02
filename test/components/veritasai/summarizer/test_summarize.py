from unittest.mock import MagicMock

from veritasai.summarizer import summarize

CONTENT = """
This is some test content that needs to be summarized. It is a test content that needs to be
summarized. It talks about the importance of summarizing content. There is some more content that
needs to be summarized. This is a test content that needs to be summarized. It is a test content
that needs to be summarized. It talks about the importance of summarizing content.
"""


def test_passes_text_through_model(mock_model: MagicMock):
    summarize(CONTENT)

    mock_model.return_value.generate_content.assert_called_once_with(CONTENT, stream=False)


def test_returns_response_from_model_without_modification(mock_model: MagicMock):
    mock_model.return_value.generate_content.return_value.text = "This is a summary of the content."

    response = summarize(CONTENT)

    assert response == "This is a summary of the content."
