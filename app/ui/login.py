from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.uic import loadUi
from controllers.user_controller import UserController


class Login(QWidget):
    # Custom signal to emit user_id upon successful login
    login_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        loadUi("app/ui/login.ui", self)

        self.login_button.clicked.connect(self.login_button_clicked)

    def login_button_clicked(self):
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()

        user_id = UserController.authenticate(email, password)

        if user_id is not None:
            print("User authenticated successfully")
            # Emit the signal with the user_id
            self.login_successful.emit(user_id)
        else:
            print("Authentication failed")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Login Failed")
            msg_box.setText(
                "Authentication failed. Please check your email and password.")
            msg_box.setStandardButtons(QMessageBox.StandardButtons.Ok)
            msg_box.exec()
