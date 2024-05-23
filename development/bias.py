import json
import os

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

load_dotenv()

authenticator = IAMAuthenticator(os.environ.get("WatsonKey"))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=authenticator
)

natural_language_understanding.set_service_url(os.environ.get("WatsonURL"))

response = natural_language_understanding.analyze(
    url="www.ibm.com",
    features=Features(
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
        metadata={},
    ),
).get_result()

print(json.dumps(response, indent=2))
