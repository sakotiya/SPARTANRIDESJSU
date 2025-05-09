from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from Admin_drivery import DriverDialog
from Admin_student import StudentDialog
from Admin_facultyy import FacultyDialog
from Admin_dashboard import DashboardDialog
from UI_Python.admin import Ui_Admin
from PyQt5.QtWidgets import QDialog, QLabel
from data201 import db_connection

class UI_Admin(QMainWindow, Ui_Admin):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi('../UI_Files/admin.ui', self)
        self.user_id = user_id
        self.name_label = self.findChild(QLabel, "namelabel")
        self.admin_label = self.findChild(QLabel, "adminlabel")
        self.load_user_info()

        self.btnDriver.clicked.connect(self.showDriverInformation)
        self.btnStudent.clicked.connect(self.showStudentInformation)
        self.btnFaculty.clicked.connect(self.showFacultyInformation)
        self.btnDashboard.clicked.connect(self.DashboardInformation)
        self.btnLogout.clicked.connect(self.LogoutInformation)

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

            self.name_label.setText(str(first_name) + " " + str(last_name))
            self.admin_label.setText(self.user_id)
        finally:
            cursor.close()
            conn.close()

    def showDriverInformation(self):
        self.hide()
        self._driverDialog = DriverDialog()
        self._driverDialog.exec_()
        self.show()

    def showStudentInformation(self):
        self.hide()
        self._studentDialog = StudentDialog()
        self._studentDialog.exec_()
        self.show()


    def showFacultyInformation(self):
        self.hide()
        self._facultyDialog = FacultyDialog()
        self._facultyDialog.exec_()
        self.show()
        
    def DashboardInformation(self):
        self._dashboardDialog = DashboardDialog()
        self._dashboardDialog.show()

    def LogoutInformation(self):
        self.close()
        
