import sys
from PyQt6.QtWidgets import QApplication
from ui.login import Login
from ui.main_management_system import MainManagementSystem
from controllers.blood_bank_controller import BloodBankController


def on_login_successful(user_id):
    login_window.close()  # Close the login window

    # Create an instance of the main_management_system window and show it
    main_management_system_window = MainManagementSystem(user_id)
    main_management_system_window.show()


if __name__ == "__main__":
    BloodBankController.initialize_inventory()

    app = QApplication(sys.argv)

    login_window = Login()
    # Connect the custom signal to the slot function
    login_window.login_successful.connect(on_login_successful)
    login_window.show()

    sys.exit(app.exec())
