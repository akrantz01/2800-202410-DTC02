from os import environ

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_admin.credentials import ApplicationDefault, Certificate

load_dotenv()

credential = ApplicationDefault()
if (service_account := environ.get("FIREBASE_SERVICE_ACCOUNT")) is not None:
    credential = Certificate(service_account)

app = firebase_admin.initialize_app(credential=credential)
db = firestore.client(app=app)

__all__ = ["db"]
