from PyQt6.QtWidgets import QWidget, QMessageBox, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.uic import loadUi
from controllers.user_controller import UserController


class Login(QWidget):
    # Custom signal to emit user_id upon successful login
    login_successful = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        loadUi("app/ui/login.ui", self)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.exit_button.clicked.connect(self.exit_button_clicked)
        self.login_button.clicked.connect(self.login_button_clicked)

        self.setEffects()

    def setEffects(self):
        self.email_line_edit.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))
        self.password_line_edit.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))
        self.label.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(184, 57, 65, 200)))
        self.label_3.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(255, 255, 255, 127)))
        self.login_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))

    def exit_button_clicked(self):
        self.close()

    def login_button_clicked(self):
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        user_id = UserController.authenticate_user(email, password)

        if user_id:
            print("User authenticated successfully")
            # Emit the signal with the user_id
            print(user_id)
            self.login_successful.emit(user_id)
        else:
            print("Authentication failed")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Login Failed")
            msg_box.setText(
                "Authentication failed. Please check your email and password.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
