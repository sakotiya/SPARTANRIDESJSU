from PyQt5 import QtWidgets
from Student_Dialog_ui import Ui_Student_Dialog

class StudentDialog(QtWidgets.QDialog, Ui_Student_Dialog):
    def __init__(self):
        super(StudentDialog, self).__init__()
        self.setupUi(self)

