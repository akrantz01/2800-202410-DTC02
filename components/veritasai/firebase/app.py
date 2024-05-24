import firebase_admin
from firebase_admin import App
from firebase_admin.credentials import ApplicationDefault, Base, Certificate
from veritasai.config import env


def _get_credentials() -> Base:
    """
    Get the credentials for the Firebase Admin SDK.
    """
    credentials = ApplicationDefault()

    if (service_account := env.get("FIREBASE_SERVICE_ACCOUNT")) is not None:
        credentials = Certificate(service_account)

    return credentials


_app = None


def init_app() -> App:
    """
    Initialize the Firebase Admin SDK.
    """
    global _app

    if _app is None:
        _app = firebase_admin.initialize_app(credential=_get_credentials())

    return _app
