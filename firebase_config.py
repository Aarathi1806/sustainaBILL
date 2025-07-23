import firebase_admin
from firebase_admin import credentials, firestore
import json, os

if os.getenv("FIREBASE_CREDENTIALS"):
    firebase_config = json.loads(os.environ["FIREBASE_CREDENTIALS"])
    firebase_config["private_key"] = firebase_config["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(firebase_config)
else:
    cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)
db = firestore.client()




