import firebase_admin
from firebase_admin import credentials, firestore, auth
from Utils.resource_finder import resource_path


cred = credentials.Certificate(
    resource_path("firebase\\bloodbank-f9243-firebase-adminsdk-sqjbj-db358b0b61.json"))
firebase_admin.initialize_app(cred)


firebase_config = {
    "apiKey": "AIzaSyCkKfujRDPsvzwnxxClw6mOt3UOvAF8b3Q",
    "authDomain": "bloodbank-f9243.firebaseapp.com",
    "databaseURL": "https://bloodbank-f9243-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "bloodbank-f9243",
    "storageBucket": "bloodbank-f9243.appspot.com",
    "messagingSenderId": "609091222709",
    "appId": "1:609091222709:web:85bb1d752b7482588492fc"
}

db = firestore.client()
batch = db.batch()

def CreateCustomToken(uid,role):
    additional_claims = {
        'role': role
    }
    auth.create_custom_token(uid, additional_claims)


def commit_batch(batch):
    try:
        batch.commit()
        return True
    except Exception as e:
        print("Batch commit failed. Error:", e)
        return False
