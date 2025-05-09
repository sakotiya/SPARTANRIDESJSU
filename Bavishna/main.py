import sys
from PyQt5.QtWidgets import QApplication
from admin_window import MainWindow
  # or admin_window if you renamed it

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
