from models.blood_bank import BloodBank


class BloodBankController:

    @staticmethod
    def add_blood(blood_type, donor_id, donor_full_name, staff_id, user_id):
        # Add blood to the blood bank
        return BloodBank.add(blood_type, donor_id, donor_full_name, staff_id, user_id)

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
        blood_data = []
        if blood_group == "All":
            for blood_type, quantity in inventory.items():
                blood_data.append((blood_type, quantity))
        else:
            compatible_blood_types = BloodBankController.get_compatible_blood_types(
                blood_group)
            for blood_type in compatible_blood_types:
                if blood_type in inventory:
                    blood_data.append((blood_type, inventory[blood_type]))

        return blood_data

    @staticmethod
    def get_compatible_blood_types(blood_group):
        compatibility = {
            "A+": ["A+", "A-", "O+", "O-"],
            "A-": ["A-", "O-"],
            "B+": ["B+", "B-", "O+", "O-"],
            "B-": ["B-", "O-"],
            "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            "AB-": ["A-", "B-", "AB-", "O-"],
            "O+": ["O+", "O-"],
            "O-": ["O-"]
        }
        return compatibility.get(blood_group, [])

    @staticmethod
    def add_inventory_listener(callback):
        # Add a listener for inventory updates in the Firebase database
        return BloodBank.add_inventory_listener(callback)

    @staticmethod
    def initialize_inventory():
        BloodBank.initialize_inventory()
