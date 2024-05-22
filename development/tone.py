from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    CategoriesOptions,
    EmotionOptions,
    EntitiesOptions,
    Features,
    SentimentOptions,
)
from veritasai.config import env


def parse_tone_analysis(analysis: dict):
    """
    Analyse the dict returned by Watson API and return JSON data for display in frontend.

    :param analysis: a dictionary whose strings are keys and whose values are lists, dicts, ints
                    or floats

    """
    print(analysis["entities"])


def retrieve_tone_analysis(url: str, text: str | None = None) -> dict:
    """
    Retrieve the analysis from IBM Watson API and return as a dict.

    :param url: A string representing a url or empty if using text
    :param text: A string of text to analyze, or None if a url is to be used
    :return: a dictionary whose strings are keys and whose values are lists, dicts, ints
            or floats
    """
    authenticator = IAMAuthenticator(env["apikey"])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )
    #
    # if text is provided use it for analysis, otherwise use the url
    source = {"text": text} if text else {"url": url}

    natural_language_understanding.set_service_url(env["url"])

    response = natural_language_understanding.analyze(
        features=Features(
            categories=CategoriesOptions(limit=3, explanation=True),
            entities=EntitiesOptions(emotion=True, sentiment=True),
            emotion=EmotionOptions(document=True),
            sentiment=SentimentOptions(document=True),
        ),
        **source,
    ).get_result()

    return response


def main():
    url = "https://www.foxnews.com/politics/michael-cohen-testifies-he-secretly-recorded-trump-lead-up-2016-election"
    # text = "IBM is the worst company on earth"
    analysis = retrieve_tone_analysis(url)
    parse_tone_analysis(analysis)


main()
