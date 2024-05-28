from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from veritasai.config import env

_client = None


def _configure_client() -> NaturalLanguageUnderstandingV1:
    api_key = env.get("WATSON_LANGUAGE_API_KEY")
    service_url = env.get("WATSON_LANGUAGE_SERVICE_URL")

    if not api_key or not service_url:
        raise ValueError("Watson Natural Language credentials not found in environment")

    authenticator = IAMAuthenticator(apikey=api_key)
    client = NaturalLanguageUnderstandingV1(version="2022-04-07", authenticator=authenticator)
    client.set_service_url(service_url)

    return client


def natural_language_client() -> NaturalLanguageUnderstandingV1:
    """
    Get a configured instance of the Watson Natural Language Understanding client.

    Credentials are automatically read from the environment.

    :return: The configured client.
    """

    global _client

    if _client is None:
        _client = _configure_client()

    return _client
