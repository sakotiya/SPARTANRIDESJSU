
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTableWidgetItem

from UI_Python.Driver_MyProfile import Ui_SignUp_Dialog as ProfileUI
from UI_Python.Driver_MyRoutes import Ui_SignUp_Dialog as RoutesUI
from UI_Python.Driver_MyLog import Ui_SignUp_Dialog as LogUI
from UI_Python.Driver_Notification import Ui_SignUp_Dialog as NotificationUI
from db_util import db_connection

import backend_driver_ui as backend
import datetime

# Generic window for each UI type
class ProfileWindow(QDialog):
    
    def __init__(self, user_id):
        super().__init__()
        self.ui = ProfileUI()
        self.ui.setupUi(self)
        self.user_id = user_id
        self.setWindowTitle("Driver Profile")
        self.load_data()
        self.connect_buttons()
        fields = [
        self.ui.lineEdit,
        self.ui.lineEdit_2,
        self.ui.lineEdit_3,
        self.ui.lineEdit_4,
        self.ui.lineEdit_5
        ]
        for field in fields:
            field.setReadOnly(True)
        self.signOutButton = self.findChild(QPushButton, "SignoutButton")
        if self.signOutButton:
            self.signOutButton.clicked.connect(self.sign_out)

    def sign_out(self):
        self.close()
        if self.parent:
            self.parent.close()
        self.login_window.show()

    def load_data(self):
        profile = backend.get_driver_profile(self.user_id)
        self.ui.label_2.setText(f"{profile['first_name']} {profile['last_name']}")
        try:
            self.ui.lineEdit.setText(f"{profile['first_name']} {profile['last_name']}")
            self.ui.lineEdit_2.setText(profile['user_id'])
            self.ui.lineEdit_3.setText(profile['mobile'])
            self.ui.lineEdit_4.setText(profile['email'])
            self.ui.lineEdit_5.setText(profile['license_number'])
        except:
            pass

    def connect_buttons(self):
        self.ui.Login.clicked.connect(self.show_profile)
        self.ui.Login_2.clicked.connect(self.show_routes)
        self.ui.Login_3.clicked.connect(self.show_logs)
        self.ui.Login_4.clicked.connect(self.show_notifications)
        self.ui.Submit.clicked.connect(self.enable_editing)
        self.ui.Submit_2.clicked.connect(self.save_edit)
        
    def show_profile(self):
        self.hide()
        ProfileWindow(self.user_id).exec_()

    def show_routes(self):
        self.hide()
        RoutesWindow(self.user_id).exec_()

    def show_logs(self):
        self.hide()
        LogWindow(self.user_id).exec_()

    def show_notifications(self):
        self.hide()
        NotificationWindow(self.user_id).exec_()
        
    def enable_editing(self):
        editable_fields = [
        self.ui.lineEdit,
        self.ui.lineEdit_2,
        self.ui.lineEdit_3,
        self.ui.lineEdit_4,
        self.ui.lineEdit_5
        ]
        for field in editable_fields:
            field.setReadOnly(False)
            field.setStyleSheet("background-color: #e0f7fa;")  # light cyan
        
    def save_edit(self):
        print("Saving changes...")
        fields = [
        self.ui.lineEdit,
        self.ui.lineEdit_2,
        self.ui.lineEdit_3,
        self.ui.lineEdit_4,
        self.ui.lineEdit_5
        ]
        for field in fields:
            field.setReadOnly(True)
            field.setStyleSheet("")  # resets to default style
        
        updated_data = {
            "name": self.ui.lineEdit.text(),
            "user_id": self.ui.lineEdit_2.text(),
            "mobile": self.ui.lineEdit_3.text(),
            "email": self.ui.lineEdit_4.text(),
            "license_number": self.ui.lineEdit_5.text()
        }
        backend.save_profile(updated_data, self.user_id)


class RoutesWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.ui = RoutesUI()
        self.ui.setupUi(self)
        self.user_id = user_id
        self.setWindowTitle("My Routes")
        self.connect_buttons()
        self.load_data()

    def connect_buttons(self):
        self.ui.Login.clicked.connect(self.show_profile)
        self.ui.Login_2.clicked.connect(self.show_routes)
        self.ui.Login_3.clicked.connect(self.show_logs)
        self.ui.Login_4.clicked.connect(self.show_notifications)

    def load_data(self):
        profile = backend.get_driver_profile(self.user_id)
        self.ui.label_2.setText(f"{profile['first_name']} {profile['last_name']}")
        today = datetime.date.today()
        routes = backend.get_routes_by_date(today, self.user_id)
        table = self.ui.tableWidget
        table.setRowCount(len(routes))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Route ID", "Stop Name", "Scheduled Time", "# Reserved"])
        for row, route in enumerate(routes):
            table.setItem(row, 0, QTableWidgetItem(route['route_id']))
            table.setItem(row, 1, QTableWidgetItem(route['stop_name']))
            table.setItem(row, 2, QTableWidgetItem(route['scheduled_time']))
            table.setItem(row, 3, QTableWidgetItem(str(route['reserved_count'])))

        self.ui.today.setText(str(today))

    def show_profile(self):
        self.hide()
        ProfileWindow(self.user_id).exec_()

    def show_routes(self):
        self.hide()
        RoutesWindow().exec_()

    def show_logs(self):
        self.hide()
        LogWindow(self.user_id).exec_()

    def show_notifications(self):
        self.hide()
        NotificationWindow(self.user_id).exec_()

class LogWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.ui = LogUI()
        self.ui.setupUi(self)
        self.user_id = user_id
        self.setWindowTitle("Trip Logs")
        self.connect_buttons()
        self.load_data()

    def connect_buttons(self):
        self.ui.Login.clicked.connect(self.show_profile)
        self.ui.Login_2.clicked.connect(self.show_routes)
        self.ui.Login_3.clicked.connect(self.show_logs)
        self.ui.Login_4.clicked.connect(self.show_notifications)

    def load_data(self, filter_month=None):
        profile = backend.get_driver_profile(self.user_id)
        self.ui.label_2.setText(f"{profile['first_name']} {profile['last_name']}")
        logs = backend.get_trip_logs(self.user_id)
        table = self.ui.tableWidget
        table.setRowCount(len(logs))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Day", "Route", "Start", "End", "Work Min"])
        for row, log in enumerate(logs):
            table.setItem(row, 0, QTableWidgetItem(log['day']))
            table.setItem(row, 1, QTableWidgetItem(log['route']))
            table.setItem(row, 2, QTableWidgetItem(log['start_time']))
            table.setItem(row, 3, QTableWidgetItem(log['end_time']))
            table.setItem(row, 4, QTableWidgetItem(log['working_min']))
        total_salary = profile['salary']
        self.ui.lineEdit.setText(f"${total_salary:.2f}")

    def show_profile(self):
        self.hide()
        ProfileWindow().exec_()

    def show_routes(self):
        self.hide()
        RoutesWindow().exec_()

    def show_logs(self):
        self.hide()
        LogWindow(self.user_id).exec_()

    def show_notifications(self):
        self.hide()
        NotificationWindow(self.user_id).exec_()

class NotificationWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.ui = NotificationUI()
        self.ui.setupUi(self)
        self.user_id = user_id
        self.setWindowTitle("Notifications")
        self.connect_buttons()
        selected_date = self.ui.selectmonth2.date()                 # QDate object
        selected_month = selected_date.toString("yyyy-MM")      # e.g., "2025-05"
        self.load_data(filter_month = selected_month)

    def connect_buttons(self):
        self.ui.Login.clicked.connect(self.show_profile)
        self.ui.Login_2.clicked.connect(self.show_routes)
        self.ui.Login_3.clicked.connect(self.show_logs)
        self.ui.Login_4.clicked.connect(self.show_notifications)
        self.ui.selectmonth2.dateChanged.connect(self.handle_month_change)


    def load_data(self, filter_month=None):
        profile = backend.get_driver_profile(self.user_id)
        self.ui.label_2.setText(f"{profile['first_name']} {profile['last_name']}")
        messages = backend.get_notifications(self.user_id)
        if filter_month:
            messages = [msg for msg in messages if msg['date'].startswith(filter_month)]
        table = self.ui.tableWidget
        table.setRowCount(len(messages))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Date", "Time", "Message"])
        for row, msg in enumerate(messages):
            table.setItem(row, 0, QTableWidgetItem(msg['date']))
            table.setItem(row, 1, QTableWidgetItem(msg['time']))
            table.setItem(row, 2, QTableWidgetItem(msg['message']))

    def show_profile(self):
        self.hide()
        ProfileWindow(self.user_id).exec_()

    def show_routes(self):
        self.hide()
        RoutesWindow(self.user_id).exec_()

    def show_logs(self):
        self.hide()
        LogWindow(self.user_id).exec_()

    def show_notifications(self):
        self.hide()
        NotificationWindow(self.user_id).exec_()
        
    def handle_month_change(self, selected_date):
        selected_month = selected_date.toString("yyyy-MM")  # ✔️ e.g., "2025-05"
        self.load_data(filter_month=selected_month)

#if __name__ == "__main__":
#    app = QApplication(sys.argv)
 #   window = ProfileWindow(self.user_id)
 #   window.exec_()
