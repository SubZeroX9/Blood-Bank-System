from app.models.blood_bank import BloodBank


class BloodBankController:

    @staticmethod
    def add_blood(quantity, blood_type, donor_id, staff_id, user_id):
        # Add blood to the blood bank
        return BloodBank.add(quantity, blood_type, donor_id, staff_id, user_id)

    @staticmethod
    def withdraw_blood(quantity, blood_type, staff_id, user_id):
        # Withdraw blood from the blood bank
        return BloodBank.withdraw(quantity, blood_type, staff_id, user_id)

    @staticmethod
    def get_blood_inventory():
        # Get the current blood inventory in the blood bank
        return BloodBank.get_inventory()

    @staticmethod
    def get_blood_quantity(blood_type):
        # Get the current quantity of a specific blood type in the blood bank
        return BloodBank.get_quantity(blood_type)

    @staticmethod
    def get_all_blood_data():
        # Fetch all blood types and quantities from the database
        inventory = BloodBank.get_inventory()
        return [(blood_type, quantity) for blood_type, quantity in inventory.items()]

    @staticmethod
    def get_blood_data_by_group(blood_group):
        # Fetch blood types and quantities for the given blood group from the database
        inventory = BloodBank.get_inventory()
        blood_data = [(blood_type, quantity) for blood_type,
                      quantity in inventory.items() if blood_type[0] == blood_group]
        return blood_data

    @staticmethod
    def add_inventory_listener(callback):
        # Add a listener for inventory updates in the Firebase database
        return BloodBank.add_inventory_listener(callback)

    @staticmethod
    def initialize_inventory():
        BloodBank.initialize_inventory()
