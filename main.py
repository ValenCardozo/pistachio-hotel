import sys
from datetime import datetime
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import *
from admin import Admin
from Reserves import Reserves
from CustomWidgets import * 

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        initDatabase()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hotel Pistachio")
        self.layout = QVBoxLayout()

        headerWidget = StyledWidget()
        headerLayout = QHBoxLayout()
        headerWidget.setLayout(headerLayout)
        
        titleLabel = QLabel("Hotel Pistachio")
        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch(1)

        self.setReservesButton(headerLayout)
        self.layout.addWidget(headerWidget)

        self.setAdminButton(headerLayout)
        self.layout.addWidget(headerWidget)

        self.loadFilter()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        self.setMinimumSize(800, 600)
        
    def setAdminButton(self, layout):
        adminButton = QPushButton('ADMIN')
        layout.addWidget(adminButton)

        adminButton.clicked.connect(self.openAdmin)

    def openAdmin(self):
        self.admin = Admin()
        self.admin.show()

    def setReservesButton(self, layout):
        adminButton = QPushButton('Mis Reservas')
        layout.addWidget(adminButton)

        adminButton.clicked.connect(self.openReserves)

    def openReserves(self):
        self.reserves = Reserves()
        self.reserves.show()

    def setCreateReserveButton(self):
        createReserve = QPushButton('Reservar')
        createReserve.clicked.connect(self.createReserve)
        
        return createReserve

    def createReserve(self):
        self.addModal = Reserves()
        self.addModal.addReserveModal()

    def loadFilter(self):
        filterWidget = QWidget()
        filterLayout = QHBoxLayout()
        filterWidget.setLayout(filterLayout)

        labelStart = QLabel("Fecha de inicio:")
        self.dateEditStart = QDateEdit()
        self.dateEditStart.setCalendarPopup(True)
        self.dateEditStart.setDate(QDate.currentDate())

        labelEnd = QLabel("Fecha de fin:")
        self.dateEditEnd = QDateEdit()
        self.dateEditEnd.setCalendarPopup(True)
        self.dateEditEnd.setDate(QDate.currentDate().addMonths(1))

        searchButton = QPushButton("Buscar")
        searchButton.clicked.connect(self.searchRooms)

        filterLayout.addWidget(labelStart)
        filterLayout.addWidget(self.dateEditStart)
        filterLayout.addWidget(labelEnd)
        filterLayout.addWidget(self.dateEditEnd)
        filterLayout.addWidget(searchButton)
        self.layout.addWidget(filterWidget)

    def updateReservesTable(self, records):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Descripción", "Cant. Personas", "Precio por noche", "Acción"])
        self.table.setRowCount(len(records))

        for i, record in enumerate(records):
            for j, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, j, item)
            
            button = self.setCreateReserveButton()
            self.table.setCellWidget(i, 4, button)

        self.table.setMinimumSize(600, 400)


    def searchRooms(self):
        date_start = self.dateEditStart.date()
        date_end = self.dateEditEnd.date()
        start_date = datetime(date_start.year(), date_start.month(), date_start.day(), 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime(date_end.year(), date_end.month(), date_end.day(), 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
        rooms = searchAvailableRooms(start_date, end_date)

        self.updateReservesTable(rooms)

def main():
    app = QApplication(sys.argv)
    some_app = Home()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
