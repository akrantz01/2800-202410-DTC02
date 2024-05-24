import json

from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    ConceptsOptions,
    EmotionOptions,
    EntitiesOptions,
    Features,
    KeywordsOptions,
    SemanticRolesOptions,
    SentimentOptions,
    SyntaxOptions,
    SyntaxOptionsTokens,
)
from veritasai.config import env


def interpret_text(url_input: str = "", text_input: str = "") -> str:
    """
    Interpret text using IBM Watson.

    :param url_input: a url string
    :param text_input: a text input string
    :return: json string
    """
    load_dotenv()

    authenticator = IAMAuthenticator(env.get("apikey"))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(env.get("url"))

    analysis_features = Features(
        concepts=ConceptsOptions(limit=10),
        emotion=EmotionOptions(document=True),
        entities=EntitiesOptions(limit=20, mentions=True, sentiment=True, emotion=True),
        keywords=KeywordsOptions(limit=20, sentiment=True, emotion=True),
        semantic_roles=SemanticRolesOptions(limit=20, keywords=True, entities=True),
        sentiment=SentimentOptions(),
        syntax=SyntaxOptions(
            sentences=True,
            tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True),
        ),
    )

    if text_input:
        response = natural_language_understanding.analyze(
            text=text_input, features=analysis_features
        ).get_result()
    else:
        analysis_features.metadata = {}
        response = natural_language_understanding.analyze(
            url=url_input, features=analysis_features
        ).get_result()

    return json.dumps(response, indent=2)


def sentence_scan(sentence: dict) -> str:
    """
    Interpret relevant sentences using IBM Watson.

    :param text_input: a sentence input string
    :return: json string
    """
    load_dotenv()

    authenticator = IAMAuthenticator(env.get("apikey"))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(env.get("url"))

    tokens = sentence[0]["tokens"]
    tokens_list = []
    for token in tokens:
        tokens_list.append(token["text"])

    analysis_features = Features(
        emotion=EmotionOptions(document=True, targets=tokens_list),
        # semantic_roles=SemanticRolesOptions(limit=20, keywords=True, entities=True),
        sentiment=SentimentOptions(targets=tokens_list),
    )

    response = natural_language_understanding.analyze(
        text=sentence[0]["text"], features=analysis_features
    ).get_result()

    return json.dumps(response, indent=2)


def get_relevant_entities(analysis: str) -> list[dict]:
    """
    Extract the important entities from the ai response.

    :param analysis: json string
    :return: relevant_entities as a list of dictionaries
    """
    relevance_cutoff = 0.6

    ai_analysis = json.loads(analysis)
    entities = ai_analysis["entities"]
    relevant_entities = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), entities)
    return list(relevant_entities)


def get_relevant_keywords(analysis: str) -> list[dict]:
    """
    Extract the important keywords from the ai response.

    :param analysis: json string
    :return: relevant_keywords as a list of dictionaries
    """
    relevance_cutoff = 0.6

    ai_analysis = json.loads(analysis)
    keywords = ai_analysis["keywords"]
    relevant_keywords = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), keywords)
    return list(relevant_keywords)


def get_sentences(analysis: str) -> list[dict]:
    """
    Extract a list of semantically detected sentences.

    :param analysis: json string
    :return: sentences as a list of dictionaries
    """
    ai_analysis = json.loads(analysis)
    tokens = ai_analysis["syntax"]["tokens"]
    sentences = ai_analysis["syntax"]["sentences"]
    token_index = 0
    for sentence in sentences:
        sentence_end = sentence["location"][1]
        sentence["tokens"] = []
        while token_index < len(tokens) and tokens[token_index]["location"][1] <= sentence_end:
            sentence["tokens"] += [tokens[token_index]]
            token_index += 1
    return sentences


def get_confident_mentions(relevant_entity: dict) -> list[dict]:
    """
    Extract the entity mentions from the relevant entities.
    """
    confidence_cutoff = 0.75

    mentions = relevant_entity["mentions"]
    confident_mentions = filter(
        lambda mention: (mention["confidence"] >= confidence_cutoff), mentions
    )
    return list(confident_mentions)


def get_mention_sentences(confident_mentions: list[dict], sentences: list[dict]) -> list[dict]:
    """
    Extract sentences that contain relevant keyword mentions.
    """
    mention_locations = map(lambda mention: (mention["location"]), confident_mentions)
    sentences_with_mentions = []
    for mention in mention_locations:
        mention_start = mention[0]
        mention_end = mention[1]
        sentences_with_mentions += filter(
            lambda sentence: (
                (mention_start >= sentence["location"][0])
                and (mention_end <= sentence["location"][1])
                and sentence not in sentences_with_mentions
            ),
            sentences,
        )
    return sentences_with_mentions


def get_keyword_sentences(keyword: str, sentences: list[dict]) -> list[dict]:
    """
    Extract sentences that contain relevant keyword mentions.
    """
    sentences_with_keywords = []
    sentences_with_keywords += filter(
        lambda sentence: (keyword in sentence["text"] and sentence not in sentences_with_keywords),
        sentences,
    )
    return sentences_with_keywords


def get_overall_sentiment(analysis: str) -> dict:
    """
    Get the overall sentiment from the scanned text.
    """
    ai_analysis = json.loads(analysis)
    return ai_analysis["sentiment"]["document"]


def get_overall_relevant_emotions(analysis: str) -> dict:
    """
    Get the relevant emotions from the scanned text.

    relevant emotions are whichever emotion(s) have scored above the threshold.
    """
    relevance_threshold = 0.3
    ai_analysis = json.loads(analysis)
    emotions = ai_analysis["emotion"]["document"]["emotion"]
    emotions_copy = emotions.copy()
    for emotion in emotions_copy:
        if emotions_copy[emotion] <= relevance_threshold:
            del emotions[emotion]
    if not emotions:
        return {"neutral": 0}
    emotions["max"] = max(emotions, key=emotions.get)
    # Case for equal
    other_emotions = list(emotions.keys())
    other_emotions.remove("max")
    other_emotions.remove(emotions["max"])
    if other_emotions:
        for emotion in other_emotions:
            if emotions[emotion] == emotions[emotions["max"]]:
                try:
                    emotions["max"].append(emotion)
                except AttributeError:
                    emotions["max"] = [emotions["max"], emotion]
    return emotions


def main():
    # my_input = "IBM has one of the largest workforces in the world"
    my_url = (
        "https://www.cbc.ca/news/canada/first-person-generation-gap-boomers-millennials-1.7211033"
    )
    analysis = interpret_text(url_input=my_url)
    # print(json.loads(analysis)["keywords"])
    # analysis = interpret_text(text_input=my_input)
    sentences = get_sentences(analysis)
    keywords = get_relevant_keywords(analysis)
    keyword_results = {}
    for keyword in keywords:
        keyword_results[keyword["text"]] = get_keyword_sentences(keyword["text"], sentences)
    entities = get_relevant_entities(analysis)
    for entity in entities:
        keyword_results[entity["text"]] = get_mention_sentences(
            get_confident_mentions(entity), sentences
        )
    for keyword in keyword_results:
        sentence_results = sentence_scan(keyword_results[keyword])
        print(get_overall_sentiment(sentence_results))
        print(get_overall_relevant_emotions(sentence_results))


if __name__ == "__main__":
    main()
