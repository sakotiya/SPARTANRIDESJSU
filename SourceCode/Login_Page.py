
import sys
import configparser
import mysql.connector
from PyQt5 import QtWidgets
from UI_Python.Login_Page_ui import Ui_LoginPage
from SourceCode.Student_Dialog import StudentDialog
from UI_Python.Sign_Up_Dialog_ui import Ui_SignUp_Dialog
from SourceCode.Admin_window import UI_Admin
from SourceCode.main import ProfileWindow


class SignUpDialog(QtWidgets.QDialog, Ui_SignUp_Dialog):
    def __init__(self):
        super(SignUpDialog, self).__init__()
        self.setupUi(self)


class LoginWindow(QtWidgets.QMainWindow, Ui_LoginPage):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)

        # Connect UI buttons
        self.join.clicked.connect(self.authenticate_user)
        self.SignUp.clicked.connect(self.open_signup_dialog)

        # Initialize DB
        self.db = self.connect_to_db()

    def connect_to_db(self):
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        return mysql.connector.connect(
            host=config["mysql"]["host"],
            user=config["mysql"]["user"],
            password=config["mysql"]["password"],
            database=config["mysql"]["database"]
        )

    def authenticate_user(self):
        role = self.roleSelector.currentText()
        sjsu_id = self.EnterYourEmailUser.text().strip()
        password = self.Password_2.text().strip()

        if not sjsu_id or not password:
            QtWidgets.QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")
            return

        # Prefix role validation
        if role == "Student" and not sjsu_id.startswith("S"):
            QtWidgets.QMessageBox.warning(self, "Invalid ID", "Student IDs must start with 'S'.")
            return
        if role == "Faculty" and not sjsu_id.startswith("F"):
            QtWidgets.QMessageBox.warning(self, "Invalid ID", "Faculty IDs must start with 'F'.")
            return
        if role == "Driver" and not sjsu_id.startswith("D"):
            QtWidgets.QMessageBox.warning(self, "Invalid ID", "Driver IDs must start with 'D'.")
            return
        if role == "Admin" and not sjsu_id.startswith("A"):
            QtWidgets.QMessageBox.warning(self, "Invalid ID", "Admin IDs must start with 'A'.")
            return

        cursor = self.db.cursor()
        query = "SELECT * FROM login WHERE sjsu_id = %s AND password = %s"
        cursor.execute(query, (sjsu_id, password))
        result = cursor.fetchone()

        if result:
            self.open_role_window(role, sjsu_id)
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

    def open_role_window(self, role, user_id):
        print("role: " + role)
        print("user: " + self.EnterYourEmailUser.text().strip())
        if role in ["Student", "Faculty"]:
            self.hide()
            self.dialog = StudentDialog(user_id, login_window=self)
            self.dialog.exec_()
            if not getattr(self.dialog, "launched_from_profile", False):
                self.show()
        elif role == "Admin" and self.EnterYourEmailUser.text().strip().startswith("A"):
            self.hide()
            self.dialog = UI_Admin(user_id)
            self.dialog.show()
        elif role == "Driver" and self.EnterYourEmailUser.text().strip().startswith("D"):
            self.hide()
            self.dialog = ProfileWindow(user_id=user_id)
            self.dialog.exec_()
            self.show()
        else:
            QtWidgets.QMessageBox.information(self, "Access", f"No window implemented for role: {role}")

    def open_signup_dialog(self):
        self.signup_dialog = SignUpDialog()
        self.signup_dialog.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
