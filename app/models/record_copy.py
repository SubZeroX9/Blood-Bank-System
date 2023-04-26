from google.cloud import firestore
from firebase.firebase_config import *

db = firestore.Client()


class RecordCopy:

    @staticmethod
    def add(record_copy_data):
        # Add record copy to the database
        doc_ref = db.collection('record_copies').add(record_copy_data)
        return doc_ref[1].id

    @staticmethod
    def get_by_id(record_copy_id):
        # Get record copy by ID from the database
        doc_ref = db.collection('record_copies').document(record_copy_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    @staticmethod
    def get_all():
        # Get all record copies from the database
        docs = db.collection('record_copies').stream()
        return {doc.id: doc.to_dict() for doc in docs}

    @staticmethod
    def update(record_copy_id, record_copy_data):
        # Update record copy in the database
        doc_ref = db.collection('record_copies').document(record_copy_id)
        doc_ref.update(record_copy_data)
        return record_copy_id

    @staticmethod
    def delete(record_copy_id):
        # Delete record copy from the database
        doc_ref = db.collection('record_copies').document(record_copy_id)
        doc_ref.delete()
        return record_copy_id
