from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
import mysql.connector
from data201 import db_connection

class WalletDialog(QDialog):
    def __init__(self, user_id, login_window, parent):
        super().__init__()
        uic.loadUi("../UI_Files/Student_Dialog_Wallet.ui", self)

        # Debug: print every widget so you know their exact objectName & class
        print("🔍 WalletDialog children:")
        for w in self.findChildren(QtWidgets.QWidget):
            print(f"   • {w.objectName():<25} {type(w).__name__}")

        self.user_id = user_id
        self.login_window = login_window
        self.parent = parent
        self.setWindowTitle("Student Wallet")
        self.load_wallet_data()


    def load_wallet_data(self):
        # 1) Fetch once, safely
        result = None
        try:
            conn = db_connection(config_file='../config/config.ini')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT w.current_balance, w.promo_code, w.spartan_card_no, s.email
                  FROM wallet w
                  JOIN student s ON s.student_id = w.sjsu_id
                 WHERE w.sjsu_id = %s
            """, (self.user_id,))
            result = cursor.fetchone()
        except mysql.connector.Error as e:
            print("❌ Wallet DB error:", e)
        finally:
            # always close if they exist
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

        # 2) Unpack or defaults
        if result:
            balance, promo, card, email = result
        else:
            balance, promo, card, email = 0.0, "N/A", "N/A", "N/A"

        # 3) Update the UI *after* closing the DB
        #
        bal_w = self.findChild(QLabel, "valueCurrentBalance")
        if bal_w:
            bal_w.setText(f"{balance:.2f}")
        else:
            lbl = self.findChild(QLabel, "CurrentBalanceLabel")
            if lbl:
                lbl.setText(f"${balance:.2f}")

        card_w = self.findChild(QLabel, "PaymentMethodLabel")
        if card_w:
            card_w.setText(str(card))


        promo_w = self.findChild(QLabel, "PromoCodeLabel")
        if promo_w:
            promo_w.setText(promo)

        email_w = self.findChild(QLabel, "BillingEmailLabel")
        if email_w:
            email_w.setText(email)
# find and wire up the Home button
        self.homeButton = self.findChild(QPushButton, "HomeButton")
        if self.homeButton:
            self.homeButton.clicked.connect(self.go_home)
        self.signOutButton = self.findChild(QPushButton, "SignOutButton")
        if self.signOutButton:
            self.signOutButton.clicked.connect(self.sign_out)

    def go_home(self):
        # close the ride-history dialog and reveal the StudentDialog again
        self.close()
    def sign_out(self):
        self.close()
        if self.parent:
            self.parent.close()
        self.login_window.show()