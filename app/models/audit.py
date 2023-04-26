from google.cloud import firestore
from firebase.firebase_config import *

db = firestore.Client()


class Audit:

    @staticmethod
    def add(audit_data):
        # Add audit record to the database
        doc_ref = db.collection('audit').add(audit_data)
        return doc_ref[1].id

    @staticmethod
    def get_all():
        # Get all audit records from the database
        docs = db.collection('audit').stream()
        return {doc.id: doc.to_dict() for doc in docs}
