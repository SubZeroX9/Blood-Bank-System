import firebase_admin
from firebase_admin import auth


class UserController:

    @staticmethod
    def authenticate(email, password):
        # Check user credentials in the Firebase Authentication
        try:
            user = auth.get_user_by_email(email)
            if user is not None:
                # Verify the password
                user_record = auth.verify_password(
                    password, user.password_hash, user.password_salt)
                if user_record:
                    return user.uid  # Return the user ID
        except Exception as e:
            print("Error:", e)
            return None  # Return None if authentication fails
