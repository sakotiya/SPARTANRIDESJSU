from PyQt5 import uic
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QPushButton, QTableWidget

from Student_Dialog_Wallet import WalletDialog
import sys
from data201 import db_connection
import pandas as pd


# ----- Ride History Dialog -----
class RideHistoryDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("../UI_Files/Student_Dialog_RideHistory.ui", self)
        self.user_id = user_id
        self.setWindowTitle("Ride History")
        self.populate_table()

    def populate_table(self):
        self.rideHistoryTable = self.findChild(QTableWidget, "tableWidget")
        if not self.rideHistoryTable:
            print("Table widget not found.")
            return

        # Connect to MySQL database
        try:


            conn = db_connection(config_file='../config/config.ini')

            cursor = conn.cursor()


            query = "SELECT trip_id, trip_date, status, sjsu_id, driver_id,	shuttle_id,	bus_stop,route_id, start_time FROM trip_history "
            cursor.execute(query)
            rides = cursor.fetchall()

            self.rideHistoryTable = self.findChild(QTableWidget, "tableWidget")
            self.rideHistoryTable.setRowCount(len(rides))
            self.rideHistoryTable.setColumnCount(7)  # Adjust if your table has more/less columns

            for row, trip in enumerate(rides):
                for col, val in enumerate(trip):
                    self.rideHistoryTable.setItem(row, col, QTableWidgetItem(str(val)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        self.rideHistoryTable.setRowCount(10)

# ----- Student Dialog -----
class StudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Student_Dialog.ui", self)
        self.setWindowTitle("Student - Spartan Ride")

        self.user_id = "U001"  # Replace with dynamic ID if needed

        # Connect Ride History button
        self.RideHistory = self.findChild(QPushButton, "RideHistory")
        self.RideHistory.clicked.connect(self.open_ride_history)
        # Connect Wallet Button
        self.walletButton = self.findChild(QPushButton, "Wallet")
        if self.walletButton:
            print("✅ Wallet button found")
            self.walletButton.clicked.connect(self.open_wallet)
        else:
            print("❌ Wallet button NOT found — check objectName")
        if self.walletButton:
            self.walletButton.clicked.connect(self.open_wallet)
    def open_ride_history(self):
        self.ride_dialog = RideHistoryDialog(self.user_id)
        self.ride_dialog.exec_()

    def open_wallet(self):
        self.wallet_dialog = WalletDialog(self.user_id)
        self.wallet_dialog.exec_()


# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentDialog()
    window.show()
    sys.exit(app.exec_())



