import datetime

import qtawesome as qta
from PyQt5.QtWidgets import QToolButton, QLCDNumber, QMessageBox
import sys
import time
from PyQt5 import uic
from data201 import db_connection
from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit,
    QToolButton, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
class FeedbackDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        uic.loadUi("../UI_Files/feedback.ui", self)

        self.setWindowTitle("Feedback")
        self.setFixedSize(400, 400)
        self.rating = "1"
        self.text_edit = self.findChild(QTextEdit, "textEdit")
        self.b1 = self.findChild(QToolButton, "toolButton_1")
        self.b1.clicked.connect(self.set_rating)
        self.b2 = self.findChild(QToolButton, "toolButton_2")
        self.b2.clicked.connect(self.set_rating)
        self.b3 = self.findChild(QToolButton, "toolButton_3")
        self.b3.clicked.connect(self.set_rating)
        self.b4 = self.findChild(QToolButton, "toolButton_4")
        self.b4.clicked.connect(self.set_rating)
        self.b5 = self.findChild(QToolButton, "toolButton_5")
        self.b5.clicked.connect(self.set_rating)
        self.result_label = self.findChild(QLCDNumber, "ReviewNumber")
        self.submit_button = self.findChild(QPushButton, "SubmitButton")
        self.submit_button.clicked.connect(self.on_submit)


    def set_rating(self):
        """Highlight stars 1..idx and unhighlight the rest."""
        btn = self.sender()
        if isinstance(btn, QToolButton):
            print("You clicked:", btn.text())
            self.result_label.display(int(btn.text()))
            self.rating = btn.text()

    def on_submit(self):
        text = self.text_edit.toPlainText().strip()
        now = datetime.datetime.now()
        # insert new feedback entry
        conn = db_connection()
        cursor = conn.cursor()
        timestamp = int(time.time())
        insert_sql = """
                     INSERT INTO feedback
                         (feedback_id, sjsu_id, message, rating, submitted_at, driver_id)
                     VALUES (%s, %s, %s, %s, %s, %s) 

                     """
        values = ( "f" + str(timestamp)[-3:], self.user_id , text, self.rating, now, "D199719242")
        cursor.execute(insert_sql, values)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"User feedback: {text!r}")
        print(f"Rating: {self.rating} / 5")
        QMessageBox.information(
            self,
            "Feedback Submitted",
            f"Your feedback has been recorded.\nRating: {self.rating} / 5"
        )
        self.hide()





