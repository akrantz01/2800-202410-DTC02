from pathlib import Path

from firebase_admin.credentials import ApplicationDefault, Certificate
from veritasai.firebase import _get_credentials

from development.testsupport import ConfigPatch


def test_loads_from_application_default_credentials():
    credential = _get_credentials()
    assert isinstance(credential, ApplicationDefault)


def test_loads_from_certificate_when_environment_variable_set(env_var: ConfigPatch):
    service_account = Path(__file__).parent / "testdata" / "service_account.json"
    env_var.set("FIREBASE_SERVICE_ACCOUNT", str(service_account))

    credential = _get_credentials()
    assert isinstance(credential, Certificate)
