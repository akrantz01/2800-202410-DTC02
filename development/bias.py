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

    print(json.dumps(response, indent=2))


def main():
    # my_input = "IBM has one of the largest workforces in the world"
    my_url = "www.ibm.com"
    interpret_text(url_input=my_url)
    # interpret_text(text_input=my_input)


if __name__ == "__main__":
    main()
