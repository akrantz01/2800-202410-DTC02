from firebase_admin import auth, firestore
from google.cloud.firestore import Client

from .app import init_app


def get_auth() -> auth.Client:
    """
    Get the Firebase Authentication client
    """
    return auth.Client(app=init_app())


def get_db() -> Client:
    """
    Get the Firestore client.
    """
    return firestore.client(app=init_app())


__all__ = ["get_auth", "get_db", "init_app"]
