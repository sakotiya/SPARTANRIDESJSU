
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
import configparser
import mysql.connector

class ProfileDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        uic.loadUi("UI_Files/Profile_DialogBox.ui", self)
        self.setWindowTitle("Student Profile")

        self.user_id = user_id
        self.parent = parent

        self.home_button = self.findChild(QPushButton, "HOME_Label")
        if self.home_button:
            self.home_button.clicked.connect(self.go_home)

        self.load_profile_info()

    def load_profile_info(self):
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        db = config["mysql"]

        conn = mysql.connector.connect(
            host=db["host"],
            user=db["user"],
            password=db["password"],
            database=db["database"]
        )
        cursor = conn.cursor()

        user_type = "student" if str(self.user_id).startswith("S") else "faculty"
        table = "student" if user_type == "student" else "faculty"
        email_column = "email" if user_type == "student" else "email_id"

        if user_type == "student":
            query = f"""
                SELECT first_name, {email_column}, phone, course, department, enrollment_year
                FROM {table}
                WHERE {table}_id = %s
            """
        else:
            query = f"""
                SELECT first_name, {email_column}, phone, department, enrollment_year
                FROM {table}
                WHERE {table}_id = %s
            """

        cursor.execute(query, (self.user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            if user_type == "student":
                first_name, email, phone, course, department, enrollment_year = result
            else:
                first_name, email, phone, department, enrollment_year = result
                course = "Not Available"

            self.set_label("Name_Label", f"Name: {first_name}")
            self.set_label("User_id_label", f"SJSU ID: {self.user_id}")
            self.set_label("Email_Label", f"Email id: {email}")
            self.set_label("Contact_label", f"Mobile Phone: {phone}")
            self.set_label("CourseName_label", f"Course Name : {course}")
            self.set_label("Enrollment_Number_label", f"Enrollment No.: {self.user_id}")
            self.set_label("Admission_YearLabel", f"Admission Year : {enrollment_year}")
            self.set_label("Department", f"Department : {department}")
            self.set_label("Account_Status_label", "Account Status : Active")
            self.set_label("Address_label", "Address: California")
        else:
            print("❌ No record found in DB.")

    def set_label(self, object_name, text):
        label = self.findChild(QLabel, object_name)
        if label:
            label.setText(text)

    def go_home(self):
        self.close()  # just close the profile window
        if self.parent:
            self.parent.show()  # re-show StudentDialog if it was hidden
