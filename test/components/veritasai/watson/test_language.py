import pytest
from ibm_cloud_sdk_core.authenticators import Authenticator
from veritasai.watson.language import _configure_client

from development.testsupport import ConfigPatch


def test_configure_client_pulls_from_environment_variables(env_var: ConfigPatch):
    env_var.set("WATSON_LANGUAGE_API_KEY", "some-testing-api-key")
    env_var.set("WATSON_LANGUAGE_SERVICE_URL", "https://some-testing-service-url.com")

    client = _configure_client()
    assert client.service_url == "https://some-testing-service-url.com"
    assert client.authenticator.authentication_type() == Authenticator.AUTHTYPE_IAM


def test_configure_client_raises_error_when_missing_api_key(env_var: ConfigPatch):
    env_var.set("WATSON_LANGUAGE_SERVICE_URL", "https://some-testing-service-url.com")

    with pytest.raises(ValueError) as e:
        _configure_client()

    assert str(e.value) == "Watson Natural Language credentials not found in environment"


def test_configure_client_raises_error_when_missing_service_url(env_var: ConfigPatch):
    env_var.set("WATSON_LANGUAGE_API_KEY", "some-testing-api-key")

    with pytest.raises(ValueError) as e:
        _configure_client()

    assert str(e.value) == "Watson Natural Language credentials not found in environment"
