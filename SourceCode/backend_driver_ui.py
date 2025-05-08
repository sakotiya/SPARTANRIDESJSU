
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import sys
import datetime

from db_util import db_connection


def query_begin():
    conn = db_connection(config_file='../config/config.ini')
    cursor = conn.cursor()
    return cursor, conn

def query_close(cursor, conn):
    cursor.close()
    conn.close()
    

def get_driver_profile(driver_id):
    cursor, conn = query_begin();
    sql = """SELECT first_name, last_name, driver_id, mobile_phone, email_address, license_number, salary FROM driver where driver_id = %s"""
    search_param = f"{driver_id}"
    cursor.execute(sql, (search_param,))
    input_data = cursor.fetchall()
    query_close(cursor, conn)
    print(input_data)

    driver_profile = {}
    if input_data:
      driver_tuple = input_data[0]
      if len(driver_tuple) == 7:
        driver_profile = {
            "first_name": driver_tuple[0],      # Index 0: 'Emily'
            "last_name": driver_tuple[1],       # Index 1: 'Davis'
            "user_id": driver_tuple[2],         # Index 2: 'D892742864'
            "mobile": str(driver_tuple[3]),     # Index 3: 12885266455 (converted to string)
            "email": driver_tuple[4],           # Index 4: 'emily.davis@csu.edu'
            "license_number": driver_tuple[5],   # Index 5: 'R9470408'
            "salary": driver_tuple[6]
        }
      else:
          print("Error: Input tuple does not have the expected 6 elements.")
    else:
      print("Error: Input list is empty.")
    return driver_profile

def get_routes_by_date(date, driver_id):
    day = date.strftime("%A")
    cursor, conn = query_begin();
    sql = """SELECT assigned_route, shift FROM driver where driver_id = %s"""
    search_param = f"{driver_id}"
    cursor.execute(sql, (search_param,))
    res = cursor.fetchall()
    print(res)
    route = res[0][0]
    shift = res[0][1]
    sql = """
SELECT T1.route_id, T1.stop_name, T1.estimated_time, T2.booking_ct FROM
(SELECT route_id, stop_name, route_name, estimated_time
FROM route where route_name = %s and shift = %s) AS T1
inner join 
(SELECT  route_id, route_name, count(distinct booking_id) as booking_ct FROM
booking
GROUP BY 1, 2) AS T2
ON T1.route_id = T2.route_id and T1.route_name = T2.route_name
ORDER BY estimated_time asc"""
    route_param = f"{route}"
    shift_param = f"{shift}"
    cursor.execute(sql, (route_param, shift_param,))
    rows = cursor.fetchall()
    assigned_routes =[]
    for row in rows:
        route_dict = {
            "route_id": row[0],
            "stop_name": row[1],
            "scheduled_time": str(row[2]), 
            "reserved_count": row[3]
        }
        assigned_routes.append(route_dict)
    query_close(cursor, conn)
    return assigned_routes

def save_profile(updated_data, driver_id):
    return

def get_trip_logs(driver_id):
    cursor, conn = query_begin();
    sql = """SELECT assigned_route, shift FROM driver where driver_id = %s"""
    search_param = f"{driver_id}"
    cursor.execute(sql, (search_param,))
    res = cursor.fetchall()
    print(res)
    route = res[0][0]
    shift = res[0][1]
    sql = """
SELECT min(estimated_time) as start_time,
max(estimated_time) as end_time
FROM route where route_name = %s and  shift = %s"""
    route_param = f"{route}"
    shift_param = f"{shift}"
    cursor.execute(sql, (route_param, shift_param,))
    rows = cursor.fetchall()
    query_close(cursor, conn)
    logs = []
    log = rows[0]
    start = datetime.datetime.strptime(log[0], "%I:%M %p")
    end = datetime.datetime.strptime(log[1], "%I:%M %p")
    duration = (end - start).seconds / 60
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        entry = {}
        entry["day"] = day
        entry["route"] = route
        entry["start_time"] = str(log[0])
        entry["end_time"] = str(log[1])
        entry["working_min"] = str(int(duration))
        logs.append(entry)
    return logs

def get_notifications(driver_id):
    cursor, conn = query_begin();
    search_param = f"{driver_id}"
    sql = """
    SELECT submitted_at, message FROM feedback where driver_id = %s"""
    search_param = f"{driver_id}"
    cursor.execute(sql, (search_param,))
    res = cursor.fetchall()
    query_close(cursor,conn)
    messages = []
    for row in res:
        
        dt_obj = datetime.datetime.strptime(str(row[0]), "%Y-%m-%d %H:%M:%S")
        msg = {
            "date": dt_obj.strftime("%Y-%m-%d"),
            "time": dt_obj.strftime("%H:%M:"),
            "message": str(row[1]), 
        }
        messages.append(msg)
    return messages
