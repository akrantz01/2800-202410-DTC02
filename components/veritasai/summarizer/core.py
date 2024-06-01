from .model import load_model


def summarize(text: str) -> str:
    """
    Generated a summary of the given text.

    The summary is generated using Google's Gemini model.

    :param text: The text to summarize
    :return: The summary of the text
    """
    model = load_model()
    response = model.generate_content(text, stream=False)
    return response.text
