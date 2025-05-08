
import qtawesome as qta
from PyQt5.QtWidgets import QToolButton
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit,
    QToolButton, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi("../UI_Files/Feedback_Dialog.ui", self)

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
        self.submit_button = self.findChild(QPushButton, "SubmitButton")
        self.submit_button.clicked.connect(self.on_submit)




    def set_rating(self):
        """Highlight stars 1..idx and unhighlight the rest."""
        btn = self.sender()
        if isinstance(btn, QToolButton):
            print("You clicked:", btn.text())
            self.rating = btn.text()

    def on_submit(self):
        text = self.text_edit.toPlainText().strip()
        print(f"User feedback: {text!r}")
        print(f"Rating: {self.rating} / 5")
        self.accept()

