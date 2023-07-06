import requests
from firebase.firebase_config import *
from models.donor import Donor


class UserController:

    @staticmethod
    def authenticate_user(email, password):
        # Replace with your Firebase project's API key
        api_key = firebase_config["apiKey"]
        auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(auth_url, data=payload)
        result = response.json()

        if 'error' in result:
            print("Authentication failed:", result['error']['message'])
            return None

        print("Authentication succeeded")
        return result['localId']
    
    @staticmethod
    def get_user_role(user_id):
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()['role']
        else:
            return None
    
    @staticmethod
    def update_history(donor_id, history):
        Donor.update_donor_history(donor_id, history)
        
    @staticmethod
    def add_new_donor_history(donor, history):
        Donor.add_new_donor_history(donor, history)

    @staticmethod
    def find_donor(donor_id):
        return Donor.is_donor_reg(donor_id)

    @staticmethod
    def sign_out_user(user_id):
        try:
            auth.revoke_refresh_tokens(user_id)
            print("User signed out successfully")
            return True
        except Exception as e:
            print("Sign out failed. Error:", str(e))
            return False