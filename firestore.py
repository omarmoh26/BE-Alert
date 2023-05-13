import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("priv.json")
app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()
