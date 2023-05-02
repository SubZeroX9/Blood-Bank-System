from models.audit import Audit
from firebase_admin import firestore
from firebase.firebase_config import db, batch, commit_batch


class BloodBank:

    @staticmethod
    def add(blood_type, donor_id, donor_full_name, staff_id, user_id):
        # Add blood to the blood bank and store related information in the database
        blood_bank_ref = db.collection(
            'blood_bank').document("Inventory")
        quantity = 1
        # Fetch the current quantity of the blood type
        current_quantity = BloodBank.get_quantity(blood_type)

        # Update the blood quantity
        batch.set(blood_bank_ref, {
            blood_type: current_quantity + quantity
        }, merge=True)

        # Add audit trail entry for the blood donation
        Audit.add({
            'action': 'Add',
            'quantity': quantity,
            'blood_group': blood_type,
            'donor_id': donor_id,
            'donor_full_name': donor_full_name,
            'technician_id': staff_id,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return commit_batch(batch)

    def add_inventory_listener(callback):
        # Create a listener for blood inventory updates
        blood_inventory_ref = db.collection("blood_bank").document("Inventory")
        return blood_inventory_ref.on_snapshot(callback)

    @staticmethod
    def withdraw(quantity, blood_type, staff_id, user_id):
        # Withdraw blood from the blood bank and store related information in the database
        blood_bank_ref = db.collection(
            'blood_bank').document("Inventory")

        # Fetch the current quantity of the blood type
        current_quantity = BloodBank.get_quantity(blood_type)
        if current_quantity < quantity:
            return False
        # Update the blood quantity
        batch.set(blood_bank_ref, {
            blood_type: max(0, current_quantity - quantity)
        }, merge=True)

        # Add audit trail entry for the blood withdrawal
        Audit.add({
            'action': 'Withdraw',
            'quantity': quantity,
            'blood_group': blood_type,
            'technician_id': staff_id,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return commit_batch(batch)

    @staticmethod
    def withdraw_emergency(quantity, blood_type, staff_id, user_id):
        # Withdraw blood from the blood bank and store related information in the database
        blood_bank_ref = db.collection(
            'blood_bank').document("Inventory")

        # Fetch the current quantity of the blood type
        current_quantity = BloodBank.get_quantity(blood_type)
        if current_quantity < quantity:
            return False
        # Update the blood quantity
        batch.set(blood_bank_ref, {
            blood_type: max(0, current_quantity - quantity)
        }, merge=True)

        # Add audit trail entry for the blood withdrawal
        Audit.add({
            'action': 'Withdraw Emergency',
            'quantity': quantity,
            'blood_group': blood_type,
            'technician_id': staff_id,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        return commit_batch(batch)

    @staticmethod
    def get_inventory():
        # Get the current blood inventory in the blood bank
        blood_bank_ref = db.collection('blood_bank').document("Inventory")
        blood_inventory = blood_bank_ref.get()
        return blood_inventory.to_dict()

    @staticmethod
    def get_quantity(blood_type):
        # Get the current quantity of a specific blood type in the blood bank
        blood_bank_ref = db.collection(
            'blood_bank').document("Inventory")
        doc = blood_bank_ref.get()
        if doc.exists:
            return doc.to_dict()[blood_type]
        else:
            return 0

    @staticmethod
    def initialize_inventory():
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        default_inventory = {blood_group: 0 for blood_group in blood_groups}

        blood_bank_ref = db.collection("blood_bank").document("Inventory")

        # Check if blood inventory exists
        blood_inventory = blood_bank_ref.get()

        if not blood_inventory.exists:  # If blood inventory doesn't exist, initialize it
            print("Initializing blood inventory...")
            blood_bank_ref.set(default_inventory)
