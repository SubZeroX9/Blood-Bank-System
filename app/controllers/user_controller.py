# user_controller.py
import requests
from firebase_admin import auth
from firebase.firebase_config import firebase_config


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
