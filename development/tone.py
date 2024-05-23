import json
import os
from typing import Callable

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    CategoriesOptions,
    EmotionOptions,
    EntitiesOptions,
    Features,
    KeywordsOptions,
    SentimentOptions,
)
from veritasai.config import env


def return_top_emotions(emotions: dict):
    """
    Return the top emotions and disgust for any elements passed in.

    :param emotions: a dictionary of emotions whose keys are strings and whose values are floats
    :return:
    """
    top_emotions = {
        key: value for key, value in sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:2]
    }
    # disgust is used to determine "Trust", so merge it if it's not one of the top two already
    return (
        top_emotions
        if "disgust" in top_emotions
        else top_emotions | {"disgust": emotions["disgust"]}
    )


def generate_stats(analysis, key, condition):
    """
    Run stats against a condition to determine cutoff for inclusion in data.

    :param analysis: a dict with emotion and sentiment keys
    :param key: a string representing the name of a key
    :condition: a lambda function to evaluate item values against
    """
    return {
        key: {
            item["text"]: {
                "emotion": return_top_emotions(item["emotion"]),
                "sentiment": item["sentiment"],
            }
            for item in analysis[key]
            if condition(item)
        }
    }


def parse_analysis_fields(analysis: dict):
    """
    Analyse the dict returned by Watson API and return shortened JSON data for summary generation.

    :param analysis: a dictionary whose strings are keys and whose values are lists, dicts, ints
                    or floats

    """
    metadata = {"metadata": analysis["metadata"]}
    document_stats = {
        "document": {
            "sentiment": analysis["sentiment"]["document"],
            "emotion": return_top_emotions(analysis["emotion"]["document"]["emotion"]),
        }
    }
    keyword_stats = generate_stats(analysis, "keywords", lambda keyword: keyword["relevance"] > 0.8)
    entity_stats = generate_stats(
        analysis,
        "entities",
        lambda entity: entity["confidence"] > 0.9 and entity["relevance"] > 0.1,
    )
    return metadata | {"title": analysis["title"]} | document_stats | keyword_stats | entity_stats


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
    source = (
        {"text": text}
        if text
        else {
            "url": url,
        }
    )
    # Define features for the analysis
    features = Features(
        emotion=EmotionOptions(document=True),
        sentiment=SentimentOptions(document=True),
    )

    # Add empty metadata only when text is None
    if not text:
        features.metadata = {}
        features.categores = CategoriesOptions(limit=3, explanation=True)
        features.entities = EntitiesOptions(emotion=True, sentiment=True)
        features.keywords = KeywordsOptions(sentiment=True, emotion=True)
    natural_language_understanding.set_service_url(env["url"])

    response = natural_language_understanding.analyze(
        features=features,
        **source,
    ).get_result()
    if not os.path.exists("results.txt"):
        with open("results.txt", "w") as f:
            f.write(json.dumps(response))
    return response


def main():
    # TODO: combine emotions according to Plutchik's wheel of emotion
    # TODO return summary based on Plutchik results
    url = "https://www.foxnews.com/politics/michael-cohen-testifies-he-secretly-recorded-trump-lead-up-2016-election"
    # text = "IBM is the worst company on earth"
    analysis = ""
    if not os.path.exists("results.txt"):
        analysis = retrieve_tone_analysis(url)
    else:
        with open("results.txt") as f:
            analysis = json.loads(f.read())
    title_analysis = retrieve_tone_analysis("", text=analysis["metadata"]["title"])

    title = {
        "title": {
            "text": analysis["metadata"]["title"],
            "sentiment": title_analysis["sentiment"]["document"],
            "emotion": return_top_emotions(title_analysis["emotion"]["document"]["emotion"]),
        }
    }
    parsed_analysis = parse_analysis_fields(title | analysis)
    print(parsed_analysis)


main()
