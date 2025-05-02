from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5 import uic

class WalletDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("../UI_Files/Student_Dialog_Wallet.ui", self)  # Load the .ui file directly
        self.user_id = user_id
        self.setWindowTitle("Student Wallet")
        self.load_wallet_data()

    def load_wallet_data(self):
        # Dummy data (replace with DB call later)
        balance = 125.50
        promo = "SPARTAN10"
        card = "Visa **** 1234"
        email = "student@sjsu.edu"

        # ✅ Find each label by its objectName as set in Qt Designer
        self.findChild(QLabel, "CurrentBalanceLabel").setText(f"${balance:.2f}")
        self.findChild(QLabel, "PaymentMethodLabel").setText(card)
        self.findChild(QLabel, "PromoCodeLabel").setText(promo)
        self.findChild(QLabel, "BillingEmailLabel").setText(email)
