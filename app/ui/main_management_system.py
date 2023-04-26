from PyQt6 import QtWidgets, uic
from controllers.blood_bank_controller import BloodBankController


class MainManagementSystem(QtWidgets.QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("app/ui/main_management_system.ui", self)

        self.user_id = user_id  # Store the user ID as an attribute of the MainWindow class

        # Connect signals and slots
        self.refresh_inventory_button.clicked.connect(
            self.update_inventory_table)
        self.blood_group_filter.currentTextChanged.connect(
            self.update_inventory_table)

        self.update_inventory_table()
        self.listener = BloodBankController.add_inventory_listener(
            self.on_inventory_changed)

    def on_inventory_changed(self, changes):
        # This method will be called when blood inventory data changes in the Firebase database
        self.update_inventory_table()

    def update_inventory_table(self):
        blood_group = self.blood_group_filter.currentText()

        # Get blood inventory for the selected blood group
        blood_inventory = BloodBankController.get_blood_inventory_by_group(
            blood_group)

        # Update the table widget with the blood inventory
        self.inventory_table.setRowCount(0)  # Clear the table

        for blood_type, quantity in blood_inventory.items():
            row = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row)

            # Add blood type and quantity to the table
            self.inventory_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(blood_type))
            self.inventory_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(quantity)))
