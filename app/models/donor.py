from firebase.firebase_config import *

class Donor:

    @staticmethod
    def add(donor):
        # Add donor to the database
        doc_ref = db.collection('donors').add(donor)
        return doc_ref[1].id

    @staticmethod
    def add_new_donor_history(donor, donor_history):
        doc_ref = db.collection('donors').document()
        batch.set(doc_ref, donor)
        medical_ref = doc_ref.collection('medical_history').document()
        batch.set(medical_ref, donor_history)

    @staticmethod
    def is_donor_reg(donor_id):
        # Get donor by ID from the database
        doc_ref = db.collection('donors').where(field_path='id', op_string='==', value=donor_id).stream()
        for doc in doc_ref:
            if doc.exists:
                return True
            else:
                return False

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
    def get_donations_quantity(donor_id):
        # Get the current quantity of a specific blood type in the blood bank
        doc_ref = list(db.collection(
            'donors').where(field_path='id', op_string='==',value=donor_id).stream())[0].reference
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()["num_of_dons"]
        else:
            return 0
        
    @staticmethod
    def update_donor_history(donor_id, donor_history):
        query = list(db.collection('donors').where(field_path='id', op_string='==',value=donor_id).stream())
        doc_ref = query[0].reference
        dons_qty = Donor.get_donations_quantity(donor_id)
        batch.set(doc_ref, {"num_of_dons": dons_qty+1}, merge=True)
        medical_ref = doc_ref.collection('medical_history').document()
        batch.set(medical_ref, donor_history)

    @staticmethod
    def delete(donor_id):
        # Delete donor from the database
        doc_ref = db.collection('donors').document(donor_id)
        doc_ref.delete()
        return donor_id
