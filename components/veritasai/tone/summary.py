from typing import Callable


def top_emotions(emotions: dict) -> dict:
    """
    Return the top emotions and disgust for any elements passed in.

    :param emotions: a dictionary of emotions whose keys are strings and whose values are floats
    :return: a dictionary containing the top two or three values
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


def generate_stats(analysis: dict, key_name: str, condition: Callable) -> dict:
    """
    Run stats against a condition to determine cutoff for inclusion in data.

    :param analysis: a dict with emotion and sentiment keys
    :param key: a string representing the name of a key
    :condition: a lambda function to evaluate item values against
    :return: a dict with items filtered based on the condition variable
    """
    return {
        item["text"]: {
            "dominant emotions": top_emotions(item["emotion"]),
            "emotion": item["emotion"],
            "sentiment": item["sentiment"],
            "relevance": item["relevance"],
            "count": item["count"] if key_name == "entities" else None,
            "type": item["type"] if key_name == "entities" else None,
        }
        for item in analysis[key_name]
        if condition(item)
    }


def summarize_analysis(analysis: dict) -> dict:
    """
    Analyse the dict returned by Watson API and return shortened JSON data for summary generation.

    :param analysis: a dictionary whose strings are keys and whose values are lists, dicts, ints
                    or floats
    :return: A pared down version of analysis dictionary
    """
    keyword_stats = generate_stats(analysis, "keywords", lambda keyword: keyword["relevance"] > 0.6)
    entity_stats = generate_stats(
        analysis,
        "entities",
        lambda entity: entity["confidence"] > 0.9 and entity["relevance"] > 0.4,
    )

    summary = {
        "document": {
            "sentiment": analysis["sentiment"]["document"],
            # Leave all emotions intact just for document
            "emotion": analysis["emotion"]["document"]["emotion"],
        },
        "keywords": keyword_stats,
        "entities": entity_stats,
    }

    if "metadata" in analysis:
        summary["metadata"] = analysis["metadata"]
        summary["title"] = analysis["title"]

    return summary
