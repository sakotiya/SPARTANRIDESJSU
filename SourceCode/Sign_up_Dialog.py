from PyQt5 import uic
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QPushButton, QTableWidget, QLabel
from SourceCode.data201 import db_connection
from SourceCode.Login_Page import SignUpDialog

from  PyQt5 import QtWidgets

class SignUpDialog(QtWidgets.QDialog, Ui_SignUp_Dialog):
    def __init__(self):
        super(SignUpDialog, self).__init__()
        self.setupUi(self)