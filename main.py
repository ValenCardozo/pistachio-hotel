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
        self.setWindowState(Qt.WindowMaximized)

        # Agregar un encabezado con botones y título
        headerWidget = QWidget()
        headerLayout = QHBoxLayout()
        headerWidget.setLayout(headerLayout)
        # Agregar botones o elementos al encabezado (puedes personalizar esto)
        headerLayout.addWidget(QLabel("Hotel Pistachio"))
        headerLayout.addWidget(QPushButton("Botón 1"))
        headerLayout.addWidget(QPushButton("Botón 2"))
        headerLayout.addStretch(2) # Espaciador para empujar "ADMIN" a la derecha

        self.setAdminButton(headerLayout)
        layout.addWidget(headerWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def setAdminButton(self, layout):
        adminButton = QPushButton('ADMIN')
        adminButton.setStyleSheet("background-color:DodgerBlue; color: white; border: 1px solid #007BFF; border-radius: 2px;")
        layout.addWidget(adminButton)

        adminButton.clicked.connect(self.openAdmin)

    def openAdmin(self):
        self.admin = Admin()
        self.admin.show()

def main():
    app = QApplication(sys.argv)
    css = '*{font-size: 15px; background-color: #fafafa; color: #101212;}'
    app.setStyleSheet(css)
    some_app = Home()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
