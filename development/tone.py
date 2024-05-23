import json
import os

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions,
    EntitiesOptions,
    Features,
    KeywordsOptions,
    SentimentOptions,
)
from veritasai.config import env


def evaluate_trust(item: dict) -> str | None:
    """
    Establish if item meets the threshold for trust, or admiration emotions.

    :param item: a dictionary containing nested dictionaries
                with emotion and sentiment keys and float values
    :return: either a string with value of trust or None
    """
    return "trust" if item["emotion"]["disgust"] < 0.05 else None


def return_combined_emotion(emotions: tuple) -> str:
    """
    Match strings inside a tuple and return corresponding string value.

    :param emotions: a tuple with two string values
    :return: a list representing a combination of the two values
    """
    emotion_map = {
        ("anger", "joy"): ["pride"],
        ("anger", "sadness"): ["envy"],
        ("joy", "sadness"): ["melancholy"],
        ("anger", "disgust"): ["contempt"],
        ("disgust", "sadness"): ["remorse"],
        ("fear", "joy"): ["guilt"],
        ("fear", "sadness"): ["despair"],
        ("disgust", "fear"): ["shame"],
        ("disgust", "joy"): ["morbidness"],
    }
    return emotion_map.get(tuple(sorted(emotions)), "unknown combination")


def return_dominant_emotion(emotion: str) -> str:
    """
    Match a string and return a corresponding one.

    :param emotion: A string representing an emotion
    :return: A string representing a more intense version of that emotion
    """
    match emotion:
        case "joy":
            return "ecstasy"
        case "fear":
            return "terror"
        case "anger":
            return "rage"
        case "disgust":
            return "loathing"
        case "sadness":
            return "grief"


def return_lesser_emotions(emotions: tuple) -> str:
    """
    Match a string and return a corrsponding one.

    :param emotion: A string representing an emotion
    :return: A string representing a less intense version of that emotion
    """
    updated_text = []
    emotion_map = (
        ("joy", "serenity"),
        ("sadness", "pensiveness"),
        ("fear", "apprehension"),
        ("anger", "annoyance"),
        ("disgust", "boredom"),
    )
    for emotion, replacement in emotion_map:
        updated_text.append(replacement if emotion in emotions else emotion)

    return updated_text


def evaluate_emotion_thresholds(
    primary_emotion: tuple[str, float],
    secondary_emotion: tuple[str, float],
    emotion_difference: float,
) -> str | tuple[str, str]:
    """
    Compare values in primary and secondary emotions and return a different string or
    a tuple of strings with an updated emotion.

    :param primary_emotion: A tuple with a string representing an emotion and a float
                            representing the emotion's strength
    :param seconary_emotion: A tuple with a string representing an emotion and a float
                            representing the emotion's strength
    :param emotion_difference: A float representing the difference between both emotion's values
    :return: a string representing an updated emotion or
            a tuple of strings if both emotions are updated
    """
    if primary_emotion[1] > 0.5 and emotion_difference > 0.8:
        return return_dominant_emotion([primary_emotion[0]])
    elif primary_emotion[1] > 0.3 and emotion_difference < 0.8:
        return return_combined_emotion((primary_emotion[0], secondary_emotion[0]))
    elif primary_emotion[1] > 0.1:
        return [primary_emotion[0], secondary_emotion[0]]
    else:
        return return_lesser_emotions((primary_emotion[0], secondary_emotion[0]))


def plutchik_analyser(analysis: dict):
    """
    Return combinations of emotions according to Plutchik's emotion dyads.

    :param: A dict with keys for title, document, keywords and entities
            and dict values that contain keys of emotion and sentiment
    """
    # TODO: run title, document, keywords, entities through each of these
    # TODO: add plutchik strings to dictionaries
    categories = ["title", "document", "keywords", "entities"]
    for category in categories:
        if "emotion" in analysis[category]:
            trust = evaluate_trust(analysis[category])
            # first element is threshold, second is the amount of difference between two emotions
            if len(analysis[category]["emotion"]) == 3:
                analysis[category]["emotion"].pop("disgust")
            primary_emotion = max(analysis[category]["emotion"].items(), key=lambda x: x[1])
            secondary_emotion = min(analysis[category]["emotion"].items(), key=lambda x: x[1])
            emotion_difference = primary_emotion[1] - secondary_emotion[1]
            processed_emotions = evaluate_emotion_thresholds(
                primary_emotion, secondary_emotion, emotion_difference
            )
            analysis[category]["trust"] = "no" if not trust else "yes"
            analysis[category]["plutchik"] = processed_emotions
        else:
            for name, data in analysis[category].items():
                trust = evaluate_trust(analysis[category][name])
                if len(data["emotion"]) == 3:
                    data["emotion"].pop("disgust")
                primary_emotion = max(data["emotion"].items(), key=lambda x: x[1])
                secondary_emotion = min(data["emotion"].items(), key=lambda x: x[1])
                emotion_difference = primary_emotion[1] - secondary_emotion[1]
                processed_emotions = evaluate_emotion_thresholds(
                    primary_emotion, secondary_emotion, emotion_difference
                )
                analysis[category][name]["trust"] = "no" if not trust else "yes"
                analysis[category][name]["plutchik"] = processed_emotions
    return analysis


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

    # Add metadata, keywords and entities only when text is None
    if not text:
        features.metadata = {}
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
    url = "https://www.goodnewsnetwork.org/grandson-surprises-grandfather-by-restoring-1954-pickup-i-never-thought-id-live-to-see-that/"
    #
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
    plutchik_emotions = plutchik_analyser(parsed_analysis)
    print(plutchik_emotions)


main()
