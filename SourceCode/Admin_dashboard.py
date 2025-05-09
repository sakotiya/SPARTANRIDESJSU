from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt 
from data201 import db_connection
from matplotlib.patches import Circle

class DashboardDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 1800, 1200)


        # connect the database
        self.conn = db_connection(config_file='../config/config_wh.ini')
        self.cursor = self.conn.cursor()

        # Main container widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # === Vertical layout for whole window ===
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # === Header layout (logo + title) ===
        header_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("/Users/bavishna/Documents/Bavishna_Masters/DATA201/SJSU_Shuttle_project/SpartanLogo.png")  # <-- Use your real path
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)

        # Title
        title_label = QLabel("Spartan Shuttle Data Analysis")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-left: 10px;")

        # Add logo and title to header
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # === Chart Grid ===
        grid_layout = QGridLayout()

        # Row 1
        grid_layout.addWidget(self.create_pie_chart(), 0, 0)
        grid_layout.addWidget(self.create_rating_linechart(), 0, 1, 1, 2)

        # Row 2
        grid_layout.addWidget(self.create_bar_chart(), 1, 0, 3, 1)
        grid_layout.addWidget(self.create_hbarchart(), 1, 1)
        grid_layout.addWidget(self.create_donutchart5(), 1, 2)

        # Row 3
        grid_layout.addWidget(self.create_barchart6(), 3, 1)
        grid_layout.addWidget(self.create_stemchart7(), 3, 2)

        # Stretch config (optional but helpful)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 2)
        grid_layout.setColumnStretch(2, 2)
        grid_layout.setRowStretch(0, 4)
        grid_layout.setRowStretch(1, 3)
        grid_layout.setRowStretch(3, 3)
        grid_layout.setRowStretch(1, 4) 

        # === Add header and grid to main layout ===
        main_layout.addLayout(header_layout)
        main_layout.addLayout(grid_layout)
        self.setStyleSheet("background-color: #cceeff;")
        #central_widget.setStyleSheet("background-color: #e6f2ff;")


    def create_pie_chart(self):
        query = """
        SELECT 
            status,
            COUNT(sjsu_id) AS student_count FROM trip
            GROUP BY status ORDER BY 
            student_count DESC
        """
        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(3, 2))
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(250, 160) 
        ax = fig.add_subplot(111)
        ax.pie(df['student_count'], labels=df['status'], autopct='%1.1f%%', textprops={'fontsize': 7})
        ax.set_title("Trips by Status", fontsize=9)
        #fig.tight_layout(pad=0.1)
        fig.subplots_adjust(right=0.85)
        return FigureCanvas(fig)

    def create_bar_chart(self):
        query = """
        SELECT time, COUNT(sjsu_id) AS student_count 
        FROM booking 
        GROUP BY time
        """
        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        
        ax.bar(df['time'], df['student_count'], color = "indigo")
        ax.set_xlabel("Time", fontsize = 7)
        ax.set_ylabel("Student Count", fontsize = 5)
        ax.set_title("Booking Trends", fontsize = 8)
        ax.set_ylim(200, 300)
        
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df['time'], rotation=90, ha='right', fontsize=7)
        fig.subplots_adjust(bottom=0.3)
        canvas = FigureCanvas(fig)
        return canvas


    def create_rating_linechart(self):
        query = """
        SELECT driver_id, AVG(rating) AS rating
        FROM feedback
        GROUP BY driver_id
        """
        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        # Line plot using index
        ax.plot(range(len(df)), df['rating'], marker='o', color ="coral")
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df['driver_id'], rotation=90, ha='right',fontsize = 7)

        ax.set_xlabel("Driver ID", fontsize = 8)
        ax.set_ylabel("Average Rating", fontsize = 8)
        ax.set_title("Average Driver Ratings")
        
        fig.tight_layout()
        return FigureCanvas(fig)

    def create_hbarchart(self):
        query = """
            SELECT day, COUNT(*) AS num_bookings
            FROM booking
            GROUP BY day
            ORDER BY day
        """
        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)

        ax.barh(df['day'], df['num_bookings'], color = "red")
        ax.tick_params(axis='y', labelsize=7)
        ax.tick_params(axis='x', labelsize=7)
        ax.set_xlabel("Number of Bookings", fontsize = 8)
        ax.set_ylabel("Day", fontsize = 8)
        ax.set_title("Bookings by Day", fontsize = 8)
        ax.set_xlim(240, 300)
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        return canvas



    def create_donutchart5(self):
        query = """
        SELECT 
            route_name,
            COUNT(sjsu_id) AS num_of_persons
        FROM route JOIN trip using (route_id)
        GROUP BY route_name
        order by route_name
        """
        df = pd.read_sql(query, self.conn)

        color_list = ['blue', 'green', 'orange', 'yellow']
        fig = Figure(figsize=(3, 2))
        ax = fig.add_subplot(111)

        ax.pie(df['num_of_persons'],labels=df['route_name'],autopct='%1.1f%%', 
            textprops={'fontsize': 8}, colors = color_list)

        # Create the donut hole
        centre_circle = Circle((0, 0), 0.70, color='white', linewidth=0)
        ax.add_artist(centre_circle)
        ax.axis('equal')
        ax.set_title("Number of Persons by Routes", fontsize=9)
        canvas = FigureCanvas(fig)
        return canvas

    def create_barchart6(self):
        query = """
        SELECT count(sjsu_id) as num_of_persons, role
        FROM student_faculty
        group by role
        """

        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(3, 2))
        ax = fig.add_subplot(111)
        
        ax.bar(df['role'], df['num_of_persons'], color = "yellowgreen")
        ax.set_xlabel("Number of persons", fontsize = 6)
        ax.set_ylabel("role", fontsize = 7)
        ax.set_title("Faculty vs Student shuttle preference", fontsize = 8)
        canvas = FigureCanvas(fig)
        return canvas

    def create_stemchart7(self):
        query = """
        SELECT 
            driver_id,
            COUNT(*) AS total_trips
        FROM feedback
        GROUP BY driver_id
        ORDER BY total_trips DESC
        """

        df = pd.read_sql(query, self.conn)
        fig = Figure(figsize=(3, 2))
        ax = fig.add_subplot(111)

        ax.stem(df['driver_id'], df['total_trips'])
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df['driver_id'], rotation=75, ha='right',fontsize=5)
        ax.set_title("Drivers based on number of trips", fontsize = 7)
        ax.set_xlabel("Driver ID",fontsize = 7)
        ax.set_ylabel("Number of trips", fontsize = 7)
        fig.subplots_adjust(bottom=0.35)
        canvas = FigureCanvas(fig)
        return canvas

