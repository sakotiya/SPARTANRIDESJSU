from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton,QComboBox, QDateEdit,QTimeEdit,QMessageBox, QSizePolicy, QVBoxLayout
from SourceCode.data201 import db_connection
from mysql.connector import Error
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os


class RouteDialog(QDialog):
    def __init__(self, user_id, login_window, parent):
        super().__init__()
        uic.loadUi("UI_Files/Student_RouteDetails.ui", self)

        print("🔍 RouteDialog children:")
        for w in self.findChildren(QtWidgets.QWidget):
            print(f"   • {w.objectName():<25} {type(w).__name__}")

        self.user_id = user_id
        self.login_window = login_window
        self.parent = parent
        self.setWindowTitle("Book a Ride")
        self.name_label = self.findChild(QLabel, "namelabel")
        self.balance_label = self.findChild(QLabel, "balancelabel")
        self.load_user_info()

        self.load_route_data()
        # Home Button
        self.homeButton = self.findChild(QPushButton, "HomeButton")
        if self.homeButton:
            self.homeButton.clicked.connect(self.go_home)
        # SignOut
        self.signOutButton = self.findChild(QPushButton, "SignOutButton")
        if self.signOutButton:
            self.signOutButton.clicked.connect(self.sign_out)

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

            query = "SELECT current_balance FROM wallet WHERE sjsu_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            if result:
                (balance,) = result
            else:
                (balance,) = (0.0,)

            self.name_label.setText(str(first_name) + " " + str(last_name))
            self.balance_label.setText(f"{balance:.2f}")
        finally:
            cursor.close()
            conn.close()

    def load_route_data(self):


            # — find your widgets by objectName in the .ui file —
            self.routeCombo = self.findChild(QComboBox, "comboBoxRoute")
            self.stopNameCombo = self.findChild(QComboBox, "comboBoxStopName")
            self.routeTimeCombo = self.findChild(QComboBox, "comboBoxTime")
            self.daySelector = self.findChild(QDateEdit, "dateEdit")
            self.bookButton = self.findChild(QPushButton, "BookRideLabel")
            self.image_label = self.findChild(QLabel, "MapImage")
            # sanity-check
            for name, w in [
                ("routeCombo", self.routeCombo),
                ("stopNameCombo", self.stopNameCombo),
                ("routeTimeCombo", self.routeTimeCombo),
                ("daySelector", self.daySelector),
                ("bookButton", self.bookButton)
            ]:
                if w is None:
                    print(f"❌ couldn’t find widget {name} in UI")
            # 2) Image placeholder

            self.image_label.setGeometry(50, 330, 550, 330)
            #self.image_label.resize(600, 400)




            #self.on_route_changed(self.combo.currentText())
            self.bookButton.clicked.connect(self.book_ride)
            self.routeCombo.currentIndexChanged.connect(self.change_route)

            today = QDate.currentDate()
            self.daySelector.setDate(today)


            img_path = os.path.join("Images/Maps/Bay.png")

            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                scaled = pixmap.scaled(
                550, 330,
                Qt.IgnoreAspectRatio,  # Qt.KeepAspectRatio,
                Qt.SmoothTransformation
        )
                self.image_label.setPixmap(scaled)
            else:
                self.image_label.setText(f"No image for : {img_path}")

    def change_route(self):
        """
        Called when the user selects 'Route'.  Reads route table for all route stops.
        """
        route_name = self.routeCombo.currentText()  # the route_id stored earlier
        print(str(self.user_id) + " : " + str(route_name))

        if route_name == "<Select Route>":
            return

        try:
            conn = db_connection()
            cursor = conn.cursor()

            insert_sql = """
                         select distinct stop_name from route where route_name = %s
                         """
            values = (route_name,)
            cursor.execute(insert_sql, values)
            rows = cursor.fetchall()
            print("change_route rows:", str(rows))

            try:
                self.stopNameCombo.currentIndexChanged.disconnect(self.change_stop_name)
            except TypeError:
                # no existing connection was found
                pass
            self.stopNameCombo.clear()
            self.stopNameCombo.addItem("<Select Stop>")
            for stop in rows:
                self.stopNameCombo.addItem(stop[0])

            self.stopNameCombo.currentIndexChanged.connect(self.change_stop_name)

            fname = route_name.lower() + ".png"
            img_path = os.path.join("Images/Maps", fname)

            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                scaled = pixmap.scaled(
                    550, 330,
                    Qt.IgnoreAspectRatio, #Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)
            else:
                self.image_label.setText(f"No image for '{route_name}': {img_path}")

        except Error as err:
            # if anything goes wrong, catch the exception
            print(f"Error executing query: {err}")
            QMessageBox.information(self, "Error in Booking ride: " + err)
        finally:
            # clean up
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


    def change_stop_name(self):
        """
        Called when the user selects 'Route'.  Reads route table for all route stops.
        """
        route_name = self.routeCombo.currentText()  # the route_name stored earlier
        stop_name = self.stopNameCombo.currentText()  # the stop_name stored earlier
        print(self.user_id + " : " + route_name + " : " + stop_name)

        try:
            conn = db_connection()
            cursor = conn.cursor()

            insert_sql = """
                         select distinct estimated_time from route where route_name = %s AND stop_name = %s
                         """
            values = (route_name, stop_name)
            cursor.execute(insert_sql, values)
            rows = cursor.fetchall()
            print("change_stop_name rows:", str(rows))
            self.routeTimeCombo.clear()
            for time in rows:
                self.routeTimeCombo.addItem(time[0])

        except Error as err:
            # if anything goes wrong, catch the exception
            print(f"Error executing query: {err}")
            QMessageBox.information(self, "Error in Booking ride: " + err)

        finally:
            # clean up
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_route_id(self):
        """
        Called when the user selects 'Route'.  Reads route table for all route stops.
        """
        route_name = self.routeCombo.currentText()  # the route_name stored earlier
        stop_name = self.stopNameCombo.currentText()  # the stop_name stored earlier
        ride_time = self.routeTimeCombo.currentText()  # the ride_time stored earlier
        print(self.user_id + " : " + route_name + " : " + stop_name + " : " + ride_time)

        try:
            conn = db_connection()
            cursor = conn.cursor()

            insert_sql = """
                         select route_id from route where route_name = %s AND stop_name = %s AND estimated_time = %s
                         """
            values = (route_name, stop_name, ride_time)
            cursor.execute(insert_sql, values)
            rows = cursor.fetchall()
            print("get_route_id rows:", str(rows))

            for route in rows:
                route_id = route[0]

        except Error as err:
            # if anything goes wrong, catch the exception
            print(f"Error executing query: {err}")
            QMessageBox.information(self, "Error in Booking ride: " + err)
        finally:
            # clean up
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

        if route_id:
            return route_id
        else:
            return "N/A"

    def book_ride(self):
        """
        Called when the user clicks 'Book'.  Reads selections, INSERTs a new booking row.
        """
        # 1) pull out what they picked
        route_name = self.routeCombo.currentText()  # the route_name stored earlier
        stop_name = self.stopNameCombo.currentText()  # the stop_name stored earlier
        ride_time = self.routeTimeCombo.currentText()  # the route,stop time stored earlier
        ride_date = self.daySelector.date().toString("yyyy-MM-dd")
        route_id = self.get_route_id()

        try:
            conn = db_connection()
            cursor = conn.cursor()

            # insert new booking entry
            insert_sql = """
                    INSERT INTO booking
                      (sjsu_id, bus_stop, day, time, route_name, route_id)
                    VALUES
                      (%s, %s, %s, %s, %s, %s)
                      
                """
            values = (self.user_id, stop_name, ride_date, ride_time, route_name, route_id)
            print("Book Ride: " + str(values))
            cursor.execute(insert_sql, values)
            insert_success = cursor.rowcount > 0

            # update wallet
            insert_sql = """
                        UPDATE wallet SET current_balance=current_balance - %s WHERE sjsu_id=%s
                         """
            values = (2, self.user_id)
            print("wallet update: " + str(values))
            cursor.execute(insert_sql, values)
            wallet_success = cursor.rowcount > 0

            if insert_success and wallet_success:
                print("✅ Book ride success.")
                conn.commit()
            else:
                QMessageBox.information(self, "Unexpected error in Booking ride. Please try again.")
                conn.rollback()

            QMessageBox.information(self,
                                    "Booked!",
                                    f"Your ride from {stop_name}, {ride_date} at {ride_time}\n"
                                    f"for route {route_name} is confirmed.")
            self.close()

        except Error as err:
            # 4) if anything goes wrong, catch the exception
            print(f"❌ Error executing query: {err}")

            QMessageBox.information(self, "Error in Booking ride: " + err)

        finally:
            # 5) clean up
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                # Home button

    def go_home(self):
                # this will close the Route Dialog and reveal the StudentDialog again
        self.close()
                # Sign Out button

    def sign_out(self):
        self.close()
        if self.parent:
            self.parent.close()
        self.login_window.show()

