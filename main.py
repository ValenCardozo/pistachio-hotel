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
        self.setWindowTitle("Hotel Pistachio")
        layout = QVBoxLayout()

        headerWidget = QWidget()
        headerLayout = QHBoxLayout()
        headerWidget.setLayout(headerLayout)
        
        titleLabel = QLabel("Hotel Pistachio")
        # titleLabel.setStyleSheet("font-size: 20px; color: #007BFF;")

        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch(1)

        self.setAdminButton(headerLayout)
        layout.addWidget(headerWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def setAdminButton(self, layout):
        adminButton = QPushButton('ADMIN')
        layout.addWidget(adminButton)

        adminButton.clicked.connect(self.openAdmin)

    def openAdmin(self):
        self.admin = Admin()
        self.admin.show()

def main():
    app = QApplication(sys.argv)
    some_app = Home()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
