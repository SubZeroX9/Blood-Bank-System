from firebase.firebase_config import *

class Donor:

    @staticmethod
    def add(donor):
        # Add donor to the database
        doc_ref = db.collection('donors').add(donor)
        return doc_ref[1].id

    @staticmethod
    def get_by_id(donor_id):
        # Get donor by ID from the database
        doc_ref = db.collection('donors').document(donor_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    @staticmethod
    def get_all():
        # Get all donors from the database
        docs = db.collection('donors').stream()
        return {doc.id: doc.to_dict() for doc in docs}

    @staticmethod
    def update(donor_id, donor_data):
        # Update donor in the database
        doc_ref = db.collection('donors').document(donor_id)
        doc_ref.update(donor_data)
        return donor_id

    @staticmethod
    def delete(donor_id):
        # Delete donor from the database
        doc_ref = db.collection('donors').document(donor_id)
        doc_ref.delete()
        return donor_id
