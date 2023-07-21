from models.donor import Donor


class DonorController:

    @staticmethod
    def add_donor(donor):
        # Add the donor to the database
        return Donor.add(donor)

    @staticmethod
    def get_donor_by_id(donor_id):
        # Get donor by ID from the database
        return Donor.get_by_id(donor_id)

    @staticmethod
    def get_donor_by_nid(donor_nid):
        # Get donor by NID from the database
        return Donor.get_by_nid(donor_nid)

    @staticmethod
    def is_registered(donor_nid):
        # Check if the donor is registered
        return Donor.is_donor_reg(donor_nid)
    
    @staticmethod
    def get_all_donors():
        # Get all donors from the database
        return Donor.get_all()

    @staticmethod
    def update_donor(donor_id, donor_data):
        # Update the donor in the database
        return Donor.update(donor_id, donor_data)

    @staticmethod
    def delete_donor(donor_id):
        # Delete the donor from the database
        return Donor.delete(donor_id)
