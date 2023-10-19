# Home window: List reservations and filters, show buttons to -> admin, my reserves, and create a reservation 
# TO-DO:
# [X] Create database and tables.
# [] List reserves.
# [] Show admin button.
# [] Show button to create a reservation.
# [] Show button to visit my reserves.

import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import initDatabase
from admin import Admin

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        initDatabase()
    
    def initUI(self):
        layout = layout = QVBoxLayout()
        self.setWindowState(Qt.WindowMaximized)
        # self.addToolBar(Qt.TopToolBarArea, self.initToolBar())
        #admin 
        adminButton = QPushButton('ADMIN')
        layout.addWidget(adminButton)
        adminButton.clicked.connect(self.openAdmin)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def openAdmin(self):
        self.admin = Admin()
        self.admin.show()

    def initToolBar(self):
        toolBar = QToolBar()
        return toolBar

def main():
    app = QApplication(sys.argv)
    css = '*{font-size: 15px; background-color: #fafafa; color: #101212;}'
    app.setStyleSheet(css)
    some_app = Home()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
