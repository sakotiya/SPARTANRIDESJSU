from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5 import uic
from data201 import db_connection
import mysql.connector

class WalletDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("../UI_Files/Student_Dialog_Wallet.ui", self)  # Load the .ui file directly
        self.user_id = user_id
        self.setWindowTitle("Student Wallet")
        self.load_wallet_data()

    def load_wallet_data(self):
        try:
            conn = db_connection(config_file='../config/config.ini')  # Your DB connection logic
            cursor = conn.cursor()

            # Query to get wallet info for this student
            query = """
                    SELECT w.current_balance, w.promo_code, w.spartan_card_no, s.email
                    FROM wallet w 
                    JOIN student s 
                    ON s.student_id = w.sjsu_id
                    
                    """
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()

            if result:
                balance, promo, card, email = result
            else:
                balance, promo, card, email = 0.0, "N/A", "N/A", "N/A"

            # Set UI fields
            self.findChild(QLabel, "labelBalance").setText(f"${balance:.2f}")
            self.findChild(QLabel, "labelPromoCode").setText(promo)
            self.findChild(QLabel, "labelPaymentMethod").setText(card)
            self.findChild(QLabel, "labelBillingEmail").setText(email)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"❌ Database error: {err}")






