import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import initDatabase

# Home window: List reservations and filters, show buttons to -> admin, my reserves, and create a reservation 
# TO-DO:
# [X] Create database and tables.
# [] List reserves.
# [] Show admin button.
# [] Show button to create a reservation.
# [] Show button to visit my reserves.


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        initDatabase()

    def initUI(self):
        self.setWindowState(Qt.WindowMaximized)
        self.show()

def main():
    app = QApplication(sys.argv)
    some_app = Home()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
