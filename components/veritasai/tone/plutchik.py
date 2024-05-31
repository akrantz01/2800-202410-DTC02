from collections import Counter

from .summary import top_emotions


def evaluate_trust(item: dict) -> str | None:
    """
    Establish if item meets the threshold for trust, or admiration emotions.

    :param item: a dictionary containing nested dictionaries
                with emotion and sentiment keys and float values
    :return: either a string with value of trust or None
    """
    return "trust" if item["emotion"]["disgust"] < 0.05 else None


def return_combined_emotion(emotions: tuple) -> list[str]:
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


def return_dominant_emotion(emotion: str) -> list[str]:
    """
    Match a string and return a corresponding one.

    :param emotion: A string representing an emotion
    :return: A string representing a more intense version of that emotion
    """
    match emotion:
        case "joy":
            return ["ecstatic"]
        case "fear":
            return ["terror"]
        case "anger":
            return ["rage"]
        case "disgust":
            return ["loathing"]
        case "sadness":
            return ["grief"]


def return_lesser_emotions(emotions: tuple) -> list[str]:
    """
    Match a string and return a corrsponding one.

    :param emotion: A string representing an emotion
    :return: A list with a string string representing a less intense version of that emotion
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


def return_key_emotion_metrics(emotion_dict: dict) -> list[str]:
    """
    Return the updated emotion after analysis.

    :param emotion_dict: a dict whose keys are strings and values are floats
    :return: a list with one or two strings
    """
    primary_emotion = max(emotion_dict.items(), key=lambda x: x[1])
    secondary_emotion = min(emotion_dict.items(), key=lambda x: x[1])
    emotion_difference = primary_emotion[1] - secondary_emotion[1]
    return evaluate_emotion_thresholds(primary_emotion, secondary_emotion, emotion_difference)


def evaluate_emotion_thresholds(
    primary_emotion: tuple[str, float],
    secondary_emotion: tuple[str, float],
    emotion_difference: float,
) -> list[str]:
    """
    Compare values in primary and secondary emotions and return a list of one or more strings
     with updated emotions.

    :param primary_emotion: A tuple with a string representing an emotion and a float
                            representing the emotion's strength
    :param seconary_emotion: A tuple with a string representing an emotion and a float
                            representing the emotion's strength
    :param emotion_difference: A float representing the difference between both emotion's values
    :return: a list with one or two strings representing updated emotions and a string representing
    the transformation that took place
    """
    # single intense dominant emotion
    if primary_emotion[1] > 0.5 and emotion_difference > 0.8:
        return [*return_dominant_emotion(primary_emotion[0]), *["intensified"]]
    # combination emotion
    elif primary_emotion[1] > 0.3 and emotion_difference < 0.8:
        return [*return_combined_emotion((primary_emotion[0], secondary_emotion[0])), *["combined"]]
    # normal form (unchanged top two emotions)
    elif primary_emotion[1] > 0.1:
        return [primary_emotion[0], secondary_emotion[0], "unchanged"]
    # weaker emotions
    else:
        return [*return_lesser_emotions((primary_emotion[0], secondary_emotion[0])), *["weakened"]]


def calculate_average_relevance(category: dict) -> float:
    """
    Return the average relevance score for all entities/keywords in the document.

    :param category: a dict with string keys and float values
    :return: a float value representing the average relevance amongst all objects
    """
    relevance_score = {"relevance": 0, "count": 0}
    for relevance_dict in category.values():
        relevance = relevance_dict.get("relevance")
        relevance_score["relevance"] += relevance
        relevance_score["count"] += 1
    return (
        round(relevance_score["relevance"] / relevance_score["count"], 4) if relevance_score else 0,
        4,
    )


def calculate_general_trust(category: dict) -> bool:
    """
    Return whether a group of entities/keywords is generally trusted or not.

    :param category: a dict with string keys and float values
    :return: a boolean
    """
    trust_values = [obj.get("trust") for obj in category.values()]
    trust_count = Counter(trust_values)
    return True if trust_count["no"] < trust_count["yes"] else False


def calculate_emotional_trend(category: dict) -> dict:
    """
    Return the average emotional intensity or trust for a group of entities/keywords.

    :param category: a dict with string keys and float values
    :return: a dict with a string key representing the most common emotion analysis transformation
            and a float value represtining the percentage of all objects it represents
    """
    transform_counter = {}
    total_count = 0
    for _, value in category.items():
        plutchik_transform = value["plutchik"][-1]
        transform_counter[plutchik_transform] = transform_counter.get(plutchik_transform, 0) + 1
        total_count += 1
    for word, count in transform_counter.items():
        transform_counter[word] = round(count / total_count, 2)
    return transform_counter


def calculate_average(category: dict) -> dict:
    """
    Find the average for a group of entities or keywords.

    :param category: a dict with string keys and float values
    :return: a dict with string keys and float values representing the average of category
    """
    # grab the first item from the dict without knowing its key name
    first_entry = next(iter(category.values()))
    total_sum = {emotion: 0 for emotion in first_entry["emotion"]}
    total_count = {emotion: 0 for emotion in first_entry["emotion"]}
    for emotion_dict in category.values():
        emotions = emotion_dict.get("emotion", {})
        # total every emotion value and keep track of how many objects there are
        for emotion, value in emotions.items():
            total_sum[emotion] += value
            total_count[emotion] += 1
    return {
        emotion: round(total_sum[emotion] / total_count[emotion], 4)
        for emotion in total_count
        if total_count[emotion] != 0
    }


def calculate_averages_and_trends(data: dict) -> tuple[dict, bool, dict, dict]:
    """
    Send a dict off to analyzers and aggregate and return the results.

    :param data: a dict of keywords or entities full of different objects containing
    emotion, relevance, trust keys
    :return: a tuple of dicts and a bool
    """
    averaged_emotion_trend = calculate_emotional_trend(data)
    averaged_relevance = calculate_average_relevance(data)
    averaged_trust = calculate_general_trust(data)
    averaged_emotions = calculate_average(data)
    return averaged_emotions, averaged_trust, averaged_relevance, averaged_emotion_trend


def process_category(category_data: dict):
    """
    Take a dictionary full of similar structured items and add new keys/values to it
    representing the averages for each items emotion, trust, relevance,
    and emotional transformations.

    :param category_data: A keywords or entities dictionary with separate objects
    containing emotion, trust, relevance and plutchik keys
    """
    for _, data in category_data.items():
        data["trust"] = "no" if not evaluate_trust(data) else "yes"
        if len(data["emotion"]) == 3:
            data["emotion"].pop("disgust")
        data["plutchik"] = return_key_emotion_metrics(data["emotion"])

    # call a function to calculate metrics and unpack the returned tuple into variables
    averaged_emotions, averaged_trust, averaged_relevance, averaged_emotion_trend = (
        calculate_averages_and_trends(category_data)
    )
    category_data["averaged emotions"] = averaged_emotions
    category_data["general trust"] = averaged_trust
    category_data["averaged relevance"] = averaged_relevance
    category_data["emotion trend"] = averaged_emotion_trend
    return


def plutchik_analyzer(analysis: dict) -> dict:
    """
    Receive an IBM Watson response dictionary and call functions to add relevant analysis
    before returning to frontend.

    :param analysis: a dict of keywords, entities, document, objects with nested dictionaries
    for emotions, sentiment, and relevance
    :return: a smaller dict with filtered versions of the same dictionaries along with new
    keys and values for emotion trends, general trust, average relevance, and averaged emotions
    """
    categories = ["document", "keywords", "entities"]
    if "metadata" in analysis:
        categories.insert(0, "title")

    for category in categories:
        if "emotion" in analysis[category]:
            analysis[category]["trust"] = "no" if not evaluate_trust(analysis[category]) else "yes"
            category_emotions = (
                analysis[category]["emotion"]
                if not category == "document"
                else top_emotions(analysis[category]["emotion"])
            )

            if len(category_emotions) == 3:
                category_emotions.pop("disgust")

            analysis[category]["plutchik"] = return_key_emotion_metrics(category_emotions)
        else:
            process_category(analysis[category])

    return analysis
