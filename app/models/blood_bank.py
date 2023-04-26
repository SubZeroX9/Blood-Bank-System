from app.models.audit import Audit
from firebase_admin import firestore, db


class BloodBank:

    # Initialize the Firestore database
    db = firestore.client()

    @staticmethod
    def add(quantity, blood_type, donor_id, staff_id, user_id):
        # Add blood to the blood bank and store related information in the database
        blood_bank_ref = BloodBank.db.collection(
            'blood_bank').document(blood_type)

        # Fetch the current quantity of the blood type
        current_quantity = BloodBank.get_quantity(blood_type)

        # Update the blood quantity
        blood_bank_ref.set({
            'quantity': current_quantity + quantity
        }, merge=True)

        # Add audit trail entry for the blood donation
        Audit.add({
            'action': 'add',
            'quantity': quantity,
            'blood_type': blood_type,
            'donor_id': donor_id,
            'staff_id': staff_id,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

    def add_inventory_listener(callback):
        # Create a listener for blood inventory updates
        blood_inventory_ref = db.collection("blood_bank")
        return blood_inventory_ref.on_snapshot(callback)

    @staticmethod
    def withdraw(quantity, blood_type, staff_id, user_id):
        # Withdraw blood from the blood bank and store related information in the database
        blood_bank_ref = BloodBank.db.collection(
            'blood_bank').document(blood_type)

        # Fetch the current quantity of the blood type
        current_quantity = BloodBank.get_quantity(blood_type)

        # Update the blood quantity
        blood_bank_ref.set({
            'quantity': max(0, current_quantity - quantity)
        }, merge=True)

        # Add audit trail entry for the blood withdrawal
        Audit.add({
            'action': 'withdraw',
            'quantity': quantity,
            'blood_type': blood_type,
            'staff_id': staff_id,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

    @staticmethod
    def get_inventory():
        # Get the current blood inventory in the blood bank
        blood_bank_ref = BloodBank.db.collection('blood_bank')
        blood_inventory = blood_bank_ref.get()
        return {doc.id: doc.to_dict()['quantity'] for doc in blood_inventory}

    @staticmethod
    def get_quantity(blood_type):
        # Get the current quantity of a specific blood type in the blood bank
        blood_bank_ref = BloodBank.db.collection(
            'blood_bank').document(blood_type)
        doc = blood_bank_ref.get()
        if doc.exists:
            return doc.to_dict()['quantity']
        else:
            return 0

    @staticmethod
    def initialize_inventory():
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        default_inventory = {blood_group: 0 for blood_group in blood_groups}

        blood_bank_ref = db.collection("blood_bank")

        # Check if blood inventory exists
        blood_inventory = blood_bank_ref.get()

        if not blood_inventory.exists:  # If blood inventory doesn't exist, initialize it
            blood_bank_ref.set(default_inventory)
