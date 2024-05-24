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
        while tokens[token_index]["location"][1] <= sentence_end:
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
        mention_start = mention["location"][0]
        mention_end = mention["location"][1]
        sentences_with_mentions += filter(
            lambda sentence: (
                (mention_start >= sentence["location"][0])
                and (mention_end <= sentence["location"][1])
                and sentence not in sentences_with_mentions
            ),
            sentences,
        )
    return sentences_with_mentions


def main():
    # my_input = "IBM has one of the largest workforces in the world"
    my_url = "www.ibm.com"
    analysis = interpret_text(url_input=my_url)
    # interpret_text(text_input=my_input)
    get_relevant_entities(analysis)


if __name__ == "__main__":
    main()
