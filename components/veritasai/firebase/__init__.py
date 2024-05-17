from os import environ

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_admin.credentials import ApplicationDefault, Base, Certificate

load_dotenv()


def get_credentials() -> Base:
    """
    Get the credentials for the Firebase Admin SDK.
    """
    credentials = ApplicationDefault()

    if (service_account := environ.get("FIREBASE_SERVICE_ACCOUNT")) is not None:
        credentials = Certificate(service_account)

    return credentials


app = firebase_admin.initialize_app(credential=get_credentials())
db = firestore.client(app=app)

__all__ = ["db"]
