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
    interpret text using IBM Watson

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
    extract the important entities from the ai response

    :param analysis: json string
    :return: relevant_entities as a list of dictionaries
    """
    relevance_cutoff = 0.6
    ai_analysis = json.loads(analysis)
    entities = ai_analysis["entities"]
    relevant_entities = filter(lambda entity: (entity["relevance"] >= relevance_cutoff), entities)
    return list(relevant_entities)


def main():
    # my_input = "IBM has one of the largest workforces in the world"
    my_url = "www.ibm.com"
    analysis = interpret_text(url_input=my_url)
    # interpret_text(text_input=my_input)
    get_relevant_entities(analysis)


if __name__ == "__main__":
    main()
