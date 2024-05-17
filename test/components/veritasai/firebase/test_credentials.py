from pathlib import Path

import pytest
from firebase_admin.credentials import ApplicationDefault, Certificate
from pytest import MonkeyPatch
from veritasai.firebase import get_credentials


@pytest.fixture(autouse=True)
def disable_firebase(monkeypatch: MonkeyPatch):
    """
    Disable the Firebase Admin SDK clients for all tests in this module.
    """
    with monkeypatch.context() as m:
        m.setattr("firebase_admin.initialize_app", lambda credential: None)
        m.setattr("firebase_admin.firestore.client", lambda app: None)

        yield


def test_loads_from_application_default_credentials(monkeypatch: MonkeyPatch):
    with monkeypatch.context() as m:
        m.delenv("FIREBASE_SERVICE_ACCOUNT", raising=False)

        credential = get_credentials()
        assert isinstance(credential, ApplicationDefault)


def test_loads_from_certificate_when_environment_variable_set(monkeypatch: MonkeyPatch):
    service_account = Path(__file__).parent / "testdata" / "service_account.json"

    with monkeypatch.context() as m:
        m.setenv("FIREBASE_SERVICE_ACCOUNT", str(service_account))

        credential = get_credentials()
        assert isinstance(credential, Certificate)
