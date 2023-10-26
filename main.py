import sys
from datetime import datetime
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import *
from admin import Admin

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        initDatabase()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hotel Pistachio")
        self.layout = QVBoxLayout()

        headerWidget = QWidget()
        headerLayout = QHBoxLayout()
        headerWidget.setLayout(headerLayout)
        
        titleLabel = QLabel("Hotel Pistachio")
        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch(1)

        self.setAdminButton(headerLayout)
        self.layout.addWidget(headerWidget)

        self.loadFilter()

        # self.searchRooms(self.layout)
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

    def loadFilter(self):
        filterWidget = QWidget()
        filterLayout = QHBoxLayout()
        filterWidget.setLayout(filterLayout)

        labelStart = QLabel("Fecha de inicio:")
        self.dateEditStart = QDateEdit()
        self.dateEditStart.setCalendarPopup(True)
        labelEnd = QLabel("Fecha de fin:")
        self.dateEditEnd = QDateEdit()
        self.dateEditEnd.setCalendarPopup(True)
        searchButton = QPushButton("Buscar")
        searchButton.clicked.connect(self.searchRooms)

        filterLayout.addWidget(labelStart)
        filterLayout.addWidget(self.dateEditStart)
        filterLayout.addWidget(labelEnd)
        filterLayout.addWidget(self.dateEditEnd)
        filterLayout.addWidget(searchButton)
        self.layout.addWidget(filterWidget)

    def loadReservesTable(self, layout, records):
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["id", "customer_full_name", "customer_email", "date_entry", "date_out", "room_id", "amount", "action"])

        table.setRowCount(len(records))

        for i, record in enumerate(records):
            for j, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(i, j, item)

        table.setMinimumSize(600, 400)
        self.layout.addWidget(table)

    def searchRooms(self, layout):
        date_start = self.dateEditStart.date()
        date_end = self.dateEditEnd.date()
        start_date = datetime(date_start.year(), date_start.month(), date_start.day(), 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime(date_end.year(), date_end.month(), date_end.day(), 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
        rooms = searchAvailableRooms(start_date, end_date)
        
        self.loadReservesTable(layout, rooms)

def main():
    app = QApplication(sys.argv)
    some_app = Home()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
