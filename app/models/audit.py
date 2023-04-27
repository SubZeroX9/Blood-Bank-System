from firebase.firebase_config import *


class Audit:

    @staticmethod
    def add(audit_data):
        # Add audit record to the database
        doc_ref = db.collection('audit').document()
        batch.set(doc_ref, audit_data)

    @staticmethod
    def get_all():
        # Get all audit records from the database
        docs = db.collection('audit').stream()
        return {doc.id: doc.to_dict() for doc in docs}

    @staticmethod
    def add_audit_listener(callback):
        # Create a listener for audit trail updates
        audit_ref = db.collection("audit")
        return audit_ref.on_snapshot(callback)
