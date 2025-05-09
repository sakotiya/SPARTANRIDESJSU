from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox
)
from data201 import db_connection

class DriverDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver Information")
        self.setMinimumSize(800, 600)

        # Load data from database
        self.conn = db_connection(config_file='config.ini')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM driver")
        self.data = self.cursor.fetchall()
        self.headers = [col[0] for col in self.cursor.description]

        # Setup table
        self.table = QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

        for row_idx, row in enumerate(self.data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        # Add Save and Delete buttons
        self.btnSave = QPushButton("Save Changes")
        self.btnSave.clicked.connect(self.save_changes)

        self.btnDelete = QPushButton("Delete Record")
        self.btnDelete.clicked.connect(self.delete_selected_rows)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btnSave)
        layout.addWidget(self.btnDelete)
        self.setLayout(layout)

        # Set background color
        self.setStyleSheet("background-color: #87CEFA;")

    def save_changes(self):
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")

            pk_value = row_data[0]
            update_parts = ", ".join(f"{self.headers[i]} = %s" for i in range(1, len(self.headers)))
            values = row_data[1:] + [pk_value]
            sql = f"UPDATE driver SET {update_parts} WHERE {self.headers[0]} = %s"
            self.cursor.execute(sql, values)

        self.conn.commit()
        self.refresh_table()

    def delete_selected_rows(self):
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)

        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Please select at least one row to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {len(selected_rows)} selected row(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for row in selected_rows:
                pk_item = self.table.item(row, 0)
                if pk_item is None:
                    continue
                pk_value = pk_item.text()

                # Delete from database
                sql = f"DELETE FROM driver WHERE {self.headers[0]} = %s"
                self.cursor.execute(sql, (pk_value,))

                # Remove from UI
                self.table.removeRow(row)

            self.conn.commit()
            self.refresh_table()

    def refresh_table(self):
        self.cursor.execute("SELECT * FROM driver")
        self.data = self.cursor.fetchall()
        self.table.setRowCount(len(self.data))
        for row_idx, row in enumerate(self.data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
