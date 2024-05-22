import json

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import CategoriesOptions, Features

authenticator = IAMAuthenticator("{apikey}")
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07", authenticator=authenticator
)

natural_language_understanding.set_service_url("{url}")

response = natural_language_understanding.analyze(
    url="www.ibm.com", features=Features(categories=CategoriesOptions(limit=3))
).get_result()

print(json.dumps(response, indent=2))
