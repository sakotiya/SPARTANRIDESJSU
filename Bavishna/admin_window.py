from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from drivery import DriverDialog
from student import StudentDialog
from facultyy import FacultyDialog
from dashboard import DashboardDialog

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('admin.ui', self)  
        self.show() 

        self.btnDriver.clicked.connect(self.showDriverInformation)
        self.btnStudent.clicked.connect(self.showStudentInformation)
        self.btnFaculty.clicked.connect(self.showFacultyInformation)
        self.btnDashboard.clicked.connect(self.DashboardInformation)
        self.btnLogout.clicked.connect(self.LogoutInformation)

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
        
