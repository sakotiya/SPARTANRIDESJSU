
import qtawesome as qta
from PyQt5.QtWidgets import QToolButton
import sys
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
        super().__init__(parent)


        self.setWindowTitle("Feedback")
        self.setFixedSize(400, 400)

        # 3) Star rating row
        self.rating = 0
        star_row = QHBoxLayout()
        star_row.setSpacing(4)
        self.stars = []
        for i in range(1, 6):
            btn = QToolButton()
            btn.setObjectName("StarButton")
            btn.setText("★")
            btn.setCheckable(True)
            btn.setFont(QFont("", 32))
            # capture the index in the lambda
            btn.clicked.connect(lambda _, idx=i: self.set_rating(idx))
            star_row.addWidget(btn)
            self.stars.append(btn)
        #card_layout.addLayout(star_row)
        # 4) Submit button
        submit = QPushButton("Submit")
        submit.setObjectName("SubmitButton")
        submit.clicked.connect(self.on_submit)
        #card_layout.addWidget(submit)

    def set_rating(self, idx: int):
        """Highlight stars 1..idx and unhighlight the rest."""
        self.rating = idx
        for i, btn in enumerate(self.stars, start=1):
            btn.setChecked(i <= idx)

    def on_submit(self):
        text = self.text_edit.toPlainText().strip()
        print(f"User feedback: {text!r}")
        print(f"Rating: {self.rating} / 5")
        self.accept()

