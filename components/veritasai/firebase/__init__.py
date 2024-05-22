import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_admin.credentials import ApplicationDefault, Base, Certificate
from google.cloud.firestore import Client
from veritasai.config import env

load_dotenv()


def _get_credentials() -> Base:
    """
    Get the credentials for the Firebase Admin SDK.
    """
    credentials = ApplicationDefault()

    if (service_account := env.get("FIREBASE_SERVICE_ACCOUNT")) is not None:
        credentials = Certificate(service_account)

    return credentials


_app = None


def get_db() -> Client:
    """
    Get the Firestore client.
    """
    global _app

    if _app is None:
        _app = firebase_admin.initialize_app(credential=_get_credentials())

    return firestore.client(app=_app)


__all__ = ["get_db"]
