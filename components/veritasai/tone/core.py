from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions,
    EntitiesOptions,
    Features,
    KeywordsOptions,
    SentimentOptions,
)
from veritasai.watson import natural_language_client

from .plutchik import plutchik_analyzer
from .summary import summarize_analysis, top_emotions


def analyze(*, url: str | None = None, text: str | None = None) -> dict:
    """
    Analyze the tone of some text.

    Can be used with either a URL or a string of text.

    :param text: a string of text to analyze
    :param url: a URL to analyze
    :return: a dictionary with analysis data
    """
    if not (bool(url) ^ bool(text)):
        raise ValueError("One of 'url' or 'text' must be provided")

    raw = extract_sentiment(url=url, text=text)

    if url:
        title = raw["metadata"]["title"]
        title_analysis = extract_sentiment(text=title)

        raw["title"] = {
            "text": title,
            "sentiment": title_analysis["sentiment"]["document"],
            "emotion": top_emotions(title_analysis["emotion"]["document"]["emotion"]),
        }

    summary = summarize_analysis(raw)
    return plutchik_analyzer(summary)


def extract_sentiment(*, url: str | None = None, text: str | None = None) -> dict:
    """
    Extract sentiment from some text.

    Can be used with either a URL or a string of text. Only one of 'url' or 'text' can be provided.

    :param text: a string of text to analyze
    :param url: a URL to analyze
    :precondition: one of 'url' or 'text' must be provided
    :return: a dictionary with the raw analysis data
    """
    client = natural_language_client()

    features = Features(
        emotion=EmotionOptions(document=True),
        sentiment=SentimentOptions(document=True),
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=10),
        keywords=KeywordsOptions(sentiment=True, emotion=True),
    )
    if text is None:
        features.metadata = {}

    response = client.analyze(features, text=text, url=url, language="en")
    return response.get_result()
