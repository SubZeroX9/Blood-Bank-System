import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QGraphicsDropShadowEffect, QFileDialog
from PyQt6.QtCore import Qt, QTimer, QStandardPaths
from PyQt6.QtGui import QColor
from Utils.pdf_exporter import export_records_to_pdf
from controllers.audit_controller import AuditController
from controllers.blood_bank_controller import BloodBankController


class MainManagementSystem(QtWidgets.QMainWindow):

    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("app/ui/main_management_system.ui", self)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.user_id = user_id  # Store the user ID as an attribute of the MainWindow class

        self.tabWidget.currentChanged.connect(self.handle_tab_click)

        self.handle_donations_tab()
        self.handle_daily_issue_tab()
        self.handle_emergency_issue_tab()
        self.handle_audit_tab()
        self.setEffects()
        # Call the function after 100 ms
        QTimer.singleShot(100, self.check_o_minus_avilability)

    def check_o_minus_avilability(self):
        # Check if there is enough O- blood to issue for an emergency
        o_minus_quantity = BloodBankController.get_blood_quantity("O-")
        if o_minus_quantity < 5:
            # There is not enough O- blood to issue for an emergency
            # Show a warning message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(
                "There is not enough O- blood to issue for an emergency")
            msg.setWindowTitle("Warning")
            msg.exec()

    def on_inventory_changed(self, keys, changes, read_time):
        # This method will be called when blood inventory data changes in the Firebase database
        self.update_inventory_table()

    def update_inventory_table(self):
        blood_group = self.blood_group_filter.currentText()

        # Get blood inventory for the selected blood group
        blood_inventory = BloodBankController.get_blood_data_by_group(
            blood_group)

        # Update the table widget with the blood inventory
        self.inventory_table.setRowCount(0)  # Clear the table
        for blood_type, quantity in blood_inventory:
            row = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row)

            # Add blood type and quantity to the table
            self.inventory_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(blood_type))
            self.inventory_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(quantity)))

    def handle_donations_tab(self):
        self.donate_button.clicked.connect(self.DonateBloodClicked)
        for blood_group in self.blood_groups:
            self.blood_group_combo_box.addItem(blood_group)

    def DonateBloodClicked(self):
        full_name = self.full_name_line_edit.text()
        if full_name == "":
            print("Full name is empty")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Donation Failed")
            msg_box.setText(
                "Please enter your full name.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        id_number = self.id_number_line_edit.text()
        if len(id_number) < 9:
            print("ID number is empty")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Donation Failed")
            msg_box.setText(
                "Please enter your ID number.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        blood_group = self.blood_group_combo_box.currentText()
        tech_id = self.tech_id_line_edit.text()
        if len(tech_id) < 9:
            print("Tech ID is empty")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Donation Failed")
            msg_box.setText(
                "Please enter the technician ID.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

        if not BloodBankController.add_blood(blood_group, id_number, full_name, tech_id, self.user_id):
            print("Failed to add blood")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Donation Failed")
            msg_box.setText(
                "Donation failed. Please try again.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return
        else:
            print("Blood added successfully")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Donation Successful")
            msg_box.setText(
                "Blood added successfully.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.full_name_line_edit.setText("")
            self.id_number_line_edit.setText("")
            self.tech_id_line_edit.setText("")

        self.CleanUI()

    def handle_daily_issue_tab(self):
        self.blood_group_filter.addItem("All")
        for blood_group in self.blood_groups:
            self.blood_group_filter.addItem(blood_group)
        # Connect signals and slots
        self.refresh_inventory_button.clicked.connect(
            self.update_inventory_table)
        self.blood_group_filter.currentTextChanged.connect(
            self.update_inventory_table)
        self.issue_blood_button.clicked.connect(self.handle_issue_blood_click)
        self.inventory_table.horizontalHeader().setVisible(True)

        self.update_inventory_table()
        self.inventory_listener = BloodBankController.add_inventory_listener(
            self.on_inventory_changed)

    def handle_emergency_issue_tab(self):
        self.issue_blood_emergency_button.clicked.connect(
            self.handle_issue_blood_emergency_click)

    def handle_audit_tab(self):
        self.records_table.horizontalHeader().setVisible(True)
        self.records_table.verticalHeader().setVisible(True)
        self.records_table.setRowCount(0)
        self.export_button.clicked.connect(self.handle_export_click)
        self.refresh_record_button.clicked.connect(self.handle_refresh_click)
        self.update_records_table()
        self.records_listner = AuditController.add_audit_listener(
            self.on_audit_changed)

    def CleanUI(self):
        self.full_name_line_edit.clear()
        self.id_number_line_edit.clear()
        self.blood_group_combo_box.setCurrentIndex(0)
        self.tech_id_line_edit.clear()

    def handle_tab_click(self, index):
        if self.tabWidget.tabText(index) == "Close All":
            self.close()

    def handle_issue_blood_click(self):
        quantity = self.quantity_spin_box.value()
        staff_id = self.staff_id_line_edit.text()
        blood_group = self.inventory_table.selectedItems()
        if not blood_group:
            massage = "Please select a blood group to issue."
            title = "Blood Group Required"
            text = "Please select a blood group to issue."
            self.WarningMassage(massage, title, text)
            return
        else:
            blood_group = blood_group[0].text()
        if not staff_id:
            massage = "Please enter a staff ID."
            title = "Staff ID Required"
            text = "Please enter a staff ID."
            self.WarningMassage(massage, title, text)
            return

        if not BloodBankController.withdraw_blood(quantity, blood_group, staff_id, self.user_id):
            message = "Failed to issue blood."
            title = "Issue Failed"
            text = "Failed to issue blood. Please try again."
            self.WarningMassage(message, title, text)
            return
        else:
            message = "Blood issued successfully."
            title = "Issue Successful"
            text = "Blood issued successfully."
            self.WarningMassage(message, title, text)

        self.ClearInventoryUI()

    def handle_issue_blood_emergency_click(self):
        blood_group = "O-"
        quantity = self.quantity_spin_box_emergency.value()
        staff_id = self.staff_id_line_edit_emergency.text()

        if not staff_id:
            massage = "Please enter a staff ID."
            title = "Staff ID Required"
            text = "Please enter a staff ID."
            self.WarningMassage(massage, title, text)
            return

        if not BloodBankController.withdraw_blood(quantity, blood_group, staff_id, self.user_id):
            message = "Failed to issue blood."
            title = "Issue Failed"
            text = "Failed to issue blood. Please try again."
            self.WarningMassage(message, title, text)
            return
        else:
            message = "Blood issued successfully."
            title = "Issue Successful"
            text = "Blood issued successfully."
            self.WarningMassage(message, title, text)

    def WarningMassage(self, massage, title, text):
        print(massage)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def ClearInventoryUI(self):
        self.staff_id_line_edit.clear()
        self.quantity_spin_box.setValue(1)
        self.blood_group_combo_box.setCurrentIndex(0)
        self.tech_id_line_edit.clear()

    def setEffects(self):
        self.inventory_table.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=0, yOffset=0, color=QColor(184, 57, 65, 255)))
        self.refresh_inventory_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))
        self.issue_blood_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))
        self.donate_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(0, 0, 0, 127)))
        self.frame_3.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(255, 255, 255, 127)))
        self.frame.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=5, yOffset=5, color=QColor(255, 255, 255, 127)))
        self.tabWidget.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=0, yOffset=0, color=QColor(184, 57, 65, 255)))

    def handle_export_click(self):
        initial_name = "Blood Bank Report.pdf"
        file_name = QFileDialog.getSaveFileName(self, 'Export to PDF',
                                                os.path.join(os.path.expanduser('~'), initial_name), 'PDF(*.pdf)')
        if file_name[0] != '':
            records = AuditController.get_records()
            export_records_to_pdf(records, file_name[0])
        else:
            massage = "Please enter a file name."
            title = "File Name Required"
            text = "Please enter a file name."
            self.WarningMassage(massage, title, text)

    def handle_refresh_click(self):
        self.update_records_table()

    def update_records_table(self):
        records = AuditController.get_records()
        self.records_table.setRowCount(0)  # Clear the table
        self.records_table.setRowCount(len(records))
        for i, record in enumerate(records.values()):
            self.records_table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(record['timestamp'])))
            self.records_table.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(record['action'])))
            self.records_table.setItem(
                i, 2, QtWidgets.QTableWidgetItem(str(record['user_id'])))
            self.records_table.setItem(
                i, 3, QtWidgets.QTableWidgetItem(str(record["technician_id"])))
            self.records_table.setItem(
                i, 4, QtWidgets.QTableWidgetItem(str(record["blood_group"])))
            self.records_table.setItem(
                i, 5, QtWidgets.QTableWidgetItem(str(record["quantity"])))
            if record["action"] == "withdraw":
                record["donor_full_name"] = "-"
                record["donor_id"] = "-"
            else:
                self.records_table.setItem(
                    i, 6, QtWidgets.QTableWidgetItem(str(record["donor_full_name"])))
                self.records_table.setItem(
                    i, 7, QtWidgets.QTableWidgetItem(str(record["donor_id"])))

    def on_audit_changed(self,  keys, changes, read_time):
        self.update_records_table()
