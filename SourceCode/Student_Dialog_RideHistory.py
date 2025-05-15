from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QPushButton, QTableWidget,QLabel
from SourceCode.data201 import db_connection
from SourceCode.Student_Dialog_Wallet import WalletDialog
from SourceCode.Student_Dialog_Route import RouteDialog
from SourceCode.Profile_DialogBox import ProfileDialog


# ----- Ride History Dialog -----
class RideHistoryDialog(QDialog):
    def __init__(self, user_id, login_window, parent):
        super().__init__()
        uic.loadUi("UI_Files/Student_Dialog_RideHistory.ui", self)
        self.user_id = user_id
        self.login_window = login_window
        self.parent = parent
        self.setWindowTitle("Ride History")
        self.populate_table()
        self.name_label = self.findChild(QLabel, "namelabel")
        self.balance_label = self.findChild(QLabel, "balancelabel")
        self.load_user_info()
        self.walletButton = self.findChild(QPushButton, "Wallet")
        self.walletButton.clicked.connect(self.open_wallet)
        self.bookRideBtn = self.findChild(QPushButton, "BookaRide")
        self.bookRideBtn.clicked.connect(self.open_book_ride)
        self.profileButton = self.findChild(QPushButton, "Profile")
        self.profileButton.clicked.connect(self.open_profile)

    def populate_table(self):
        self.rideHistoryTable = self.findChild(QTableWidget, "tableWidget")
        if not self.rideHistoryTable:
            print("Table widget not found.")
            return

        # Connect to MySQL database
        try:


            conn = db_connection()

            cursor = conn.cursor()


            query = "SELECT trip_id, status, sjsu_id, driver_id, bus_stop, start_time FROM trip_history WHERE sjsu_id = %s"
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

    def load_user_info(self):
        try:
            conn = db_connection()
            cursor = conn.cursor()
            query = "SELECT first_name, last_name FROM login WHERE sjsu_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            if result:
                first_name, last_name = result
            else:
                first_name, last_name = "N/A", "N/A"

            query = "SELECT current_balance FROM wallet WHERE sjsu_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            if result:
                (balance,) = result
            else:
                (balance,) = (0.0,)

            self.name_label.setText(str(first_name) + " " + str(last_name))
            self.balance_label.setText(f"{balance:.2f}")
        finally:
            cursor.close()
            conn.close()
    def go_home(self):
        # this will close the ride-history dialog and reveal the StudentDialog again
        self.close()
        # Sign Out button

    def sign_out(self):
        self.close()
        if self.parent:
            self.parent.close()
        self.login_window.show()
    def open_wallet(self):
       self.wallet_dialog = WalletDialog(self.user_id, login_window=self.login_window, parent=self)
       self.wallet_dialog.exec_()
    def open_book_ride(self):
        self.route_dialog = RouteDialog(self.user_id, login_window=self.login_window, parent=self)
        self.route_dialog.exec_()
    def open_profile(self):
        self.profile_dialog = ProfileDialog(self.user_id, parent=self)
        self.profile_dialog.exec_()






