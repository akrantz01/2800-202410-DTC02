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
from veritasai.logging import get_logger
from veritasai.watson import natural_language_client

from .scores import (
    count_pronouns,
    process_keywords,
    score_adjectives,
    score_keywords,
    score_pronouns,
    score_segments,
)
from .sentences import chunk_sentence

logger = get_logger("veritasai.bias")


def analyze(*, url: str | None = None, text: str | None = None) -> dict:
    """
    Analyze the bias of some text.

    Can be used with either a URL or a string of text.

    :param text: a string of text to analyze
    :param url: a URL to analyze
    :return: a dictionary with analysis data
    """
    if not (bool(url) ^ bool(text)):
        raise ValueError("One of 'url' or 'text' must be provided")

    logger.info("starting document analysis")
    analysis = interpret_text(url=url, text=text)

    adjective_score = score_adjectives(analysis)

    pronoun_count = count_pronouns(analysis)
    pronoun_score = score_pronouns(pronoun_count)

    keywords = process_keywords(analysis)
    keywords_score = score_keywords(keywords)

    logger.info("completed document analysis")

    logger.info("starting sentence analysis")

    for keyword in keywords:
        logger.info("processing keyword: %s", keyword)
        for sentence in keywords[keyword]["sentences"]:
            segments = chunk_sentence(sentence["text"])
            scanned_segments = {
                segment: interpret_text(text=segment, sentiment_only=True) for segment in segments
            }
            sentence["scores"] = score_segments(scanned_segments)

    logger.info("completed sentence analysis")

    return {
        "adjectiveScore": adjective_score,
        "pronounCount": pronoun_count,
        "pronounScore": pronoun_score,
        "keywords": keywords,
        "keywordScore": keywords_score,
        "sentences": True,
        "biasScore": (adjective_score + pronoun_score + keywords_score["score"]) / 3,
    }


def interpret_text(
    *,
    url: str | None = None,
    text: str | None = None,
    sentiment_only: bool = False,
) -> dict:
    """
    Extract sentiment from some text.

    Can be used with either a URL or a string of text. Only one of 'url' or 'text' can be provided.

    :param text: a string of text to analyze
    :param url: a URL to analyze
    :param sentiment_only: whether to only extract sentiment
    :precondition: one of 'url' or 'text' must be provided
    :return: a dictionary with the raw analysis data
    """
    client = natural_language_client()
    features = Features(emotion=EmotionOptions(document=True), sentiment=SentimentOptions())

    if not sentiment_only:
        features.concepts = ConceptsOptions(limit=10)
        features.entities = EntitiesOptions(limit=20, mentions=True, sentiment=True, emotion=True)
        features.keywords = KeywordsOptions(limit=20, sentiment=True, emotion=True)
        features.semantic_roles = SemanticRolesOptions(limit=20, keywords=True, entities=True)
        features.syntax = SyntaxOptions(
            sentences=True,
            tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True),
        )

    if url:
        features.metadata = {}

    response = client.analyze(features, text=text, url=url, language="en")
    return response.get_result()
