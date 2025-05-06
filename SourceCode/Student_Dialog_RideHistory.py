from PyQt5 import uic
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QPushButton, QTableWidget
#from ui_helpers import show_flash
from Student_Dialog_Wallet import WalletDialog
import sys
from data201 import db_connection
import pandas as pd


# ----- Ride History Dialog -----
class RideHistoryDialog(QDialog):
    def __init__(self, user_id, login_window, parent):
        super().__init__()
        uic.loadUi("../UI_Files/Student_Dialog_RideHistory.ui", self)
        self.user_id = user_id
        self.login_window = login_window
        self.parent = parent
        self.setWindowTitle("Ride History")
        self.populate_table()
        #show_flash(self, "Each ride costs $2.00", duration_ms=5000)


    def populate_table(self):
        self.rideHistoryTable = self.findChild(QTableWidget, "tableWidget")
        if not self.rideHistoryTable:
            print("Table widget not found.")
            return

        # Connect to MySQL database
        try:


            conn = db_connection(config_file='../config/config.ini')

            cursor = conn.cursor()


            query = "SELECT trip_id, trip_date, status, sjsu_id, driver_id,	shuttle_id,	bus_stop,route_id, start_time FROM trip_history WHERE sjsu_id = %s"
            print("▶ SQL:", query.strip(), "params:", (self.user_id,))
            cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            print("✅ fetched rows:", rows)

            #cursor.execute(query)
            #rides = cursor.fetchall()
        finally:
            # Clean up cursor & connection if they exist
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass
            n_rows = len(rows)
            self.rideHistoryTable.setRowCount(n_rows or 10)
            self.rideHistoryTable.setColumnCount(7)
            self.rideHistoryTable = self.findChild(QTableWidget, "tableWidget")
           # Adjust if your table has more/less columns

            for r, row_data in enumerate(rows):
                for c, val in enumerate(row_data):

                    self.rideHistoryTable.setItem(r, c, QTableWidgetItem(str(val)))

            cursor.close()
            conn.close()

        # Home button
        self.homeButton = self.findChild(QPushButton, "HomeButton")
        if self.homeButton:
            self.homeButton.clicked.connect(self.go_home)

        self.signOutButton = self.findChild(QPushButton, "SignOutButton")
        if self.signOutButton:
            self.signOutButton.clicked.connect(self.sign_out)

    def go_home(self):
        # this will close the ride-history dialog and reveal the StudentDialog again
        self.close()
        # Sign Out button

    def sign_out(self):
        self.close()
        if self.parent:
            self.parent.close()
        self.login_window.show()





