from PyQt5 import uic
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QPushButton, QTableWidget

from Student_Dialog_Wallet import WalletDialog
from Student_Dialog_RideHistory import RideHistoryDialog
from Student_Dialog_Route import RouteDialog
from Feedback_Dialog import FeedbackDialog
import sys
from data201 import db_connection



# ----- Student Dialog -----
class StudentDialog(QDialog):
    def __init__(self, user_id, login_window):
        super().__init__()

        uic.loadUi("../UI_Files/Student_Dialog.ui", self)
        self.setWindowTitle("Student - Spartan Ride")
        self.user_id = user_id
        self.login_window = login_window
        from PyQt5.QtWidgets import QPushButton
        print("Buttons:", [b.objectName() for b in self.findChildren(QPushButton)])
        # Connect Ride History button
        self.RideHistory = self.findChild(QPushButton, "RideHistory")
        self.RideHistory.clicked.connect(self.open_ride_history)
        # Connect Wallet Button
        self.walletButton = self.findChild(QPushButton, "Wallet")
        self.walletButton.clicked.connect(self.open_wallet)
        # Feedback
        self.feedbackButton = self.findChild(QPushButton, "Feedback")
        self.feedbackButton.clicked.connect(self.open_feedback)
        #Book the ride
        print("🔘 Buttons in StudentDialog:")
        for b in self.findChildren(QPushButton):
            print("   •", b.objectName())
        self.bookRideBtn = self.findChild(QPushButton, "BookaRide")
        if not self.bookRideBtn:
            print("❌ BookRide button not found – check objectName")
        else:
            self.bookRideBtn.clicked.connect(self.open_book_ride)
        # Signout Button
        self.signOutButton = self.findChild(QPushButton, "SignOut")
        if self.signOutButton:
            self.signOutButton.clicked.connect(self.sign_out)

    def sign_out(self):
        self.close()
        if self.parent():
            self.parent().close()
        self.login_window.show()

    def open_ride_history(self):
        self.ride_dialog = RideHistoryDialog(self.user_id, login_window = self.login_window, parent=self)
        self.ride_dialog.exec_()
        parent = self

    def open_wallet(self):
        self.wallet_dialog = WalletDialog(self.user_id,login_window = self.login_window, parent=self)
        self.wallet_dialog.exec_()

    def open_feedback(self):
        self.feedback_dialog = FeedbackDialog(self.user_id)
        self.feedback_dialog.exec_()

    def open_book_ride(self):
        # instantiate and show modally
        self.route_dialog = RouteDialog(self.user_id, login_window = self.login_window, parent=self)
        self.route_dialog.exec_()

    def open_route(self):
        self.wallet_dialog = WalletDialog(self.user_id,login_window = self.login_window, parent=self)
        self.wallet_dialog.exec_()
