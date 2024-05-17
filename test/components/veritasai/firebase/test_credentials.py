from pathlib import Path

from firebase_admin.credentials import ApplicationDefault, Certificate
from pytest import MonkeyPatch
from veritasai.firebase import _get_credentials


def test_loads_from_application_default_credentials(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:
        m.delenv("FIREBASE_SERVICE_ACCOUNT", raising=False)

        credential = _get_credentials()
        assert isinstance(credential, ApplicationDefault)


def test_loads_from_certificate_when_environment_variable_set(monkeypatch: MonkeyPatch):
    service_account = Path(__file__).parent / "testdata" / "service_account.json"

    with monkeypatch.context() as m:
        m.setenv("FIREBASE_SERVICE_ACCOUNT", str(service_account))

        credential = _get_credentials()
        assert isinstance(credential, Certificate)
