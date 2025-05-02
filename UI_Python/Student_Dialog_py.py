import sys
from PyQt5 import QtWidgets
from Student_Dialog import Ui_Student_Dialog  # <-- Import the auto-generated class

class MyApp(QtWidgets.QMainWindow, Ui_Student_Dialog):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)  # <-- Very important to set up UI
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
