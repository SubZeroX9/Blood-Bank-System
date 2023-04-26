from firebase.firebase_config import *

class Withdrawal:

    @staticmethod
    def add(withdrawal_data):
        # Add withdrawal record to the database
        doc_ref = db.collection('withdrawals').add(withdrawal_data)
        return doc_ref[1].id

    @staticmethod
    def get_all():
        # Get all withdrawal records from the database
        docs = db.collection('withdrawals').stream()
        return {doc.id: doc.to_dict() for doc in docs}
