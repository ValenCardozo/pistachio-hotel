from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import *
from datetime import *
from CustomWidgets import *

class Reserves(QMainWindow):
    def __init__(self):
            super().__init__()
            self.setWindowState(Qt.WindowMaximized)

            self.setWindowTitle("Hotel Pistacho - Mis Reservas")
            self.setGeometry(100, 100, 800, 600)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            layout = QVBoxLayout()
            central_widget.setLayout(layout)

            headerWidget = StyledWidget()
            headerLayout = QHBoxLayout()
            headerWidget.setLayout(headerLayout)

            titleLabel = StyledLabel("Mis Reservas")
            headerLayout.addWidget(titleLabel)
            headerLayout.addStretch(1)

            layout.addWidget(headerWidget)

            grid_layout = QGridLayout()

            email_label = QLabel("Correo Electrónico:")
            email_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.email_input = QLineEdit()
            self.email_input.setFixedWidth(150)

            search_button = QPushButton("Buscar")
            search_button.clicked.connect(self.findForMail)
            search_button.setFixedWidth(80)
            search_button.setCursor(QCursor(Qt.PointingHandCursor))
            search_button.setStyleSheet("background-color: #def1ed; color: white; border: 1px solid #def1ed;")
            search_button.setStyleSheet("QPushButton:hover { background-color: #c3ecb9; color: white; border-radius : 20;}")

            grid_layout.addWidget(email_label, 0, 0)
            grid_layout.addWidget(self.email_input, 0, 1)
            grid_layout.addWidget(search_button, 0, 2)
            grid_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed), 0, 3)

            layout.addLayout(grid_layout)

            self.table = QTableWidget()
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(["id","nombre","email","fecha de ingreso","fecha de salia","habitacion","precio", "accion"])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            layout.addWidget(self.table)

    def addReserveModal(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Agregar Reserva")

        formLayout = QFormLayout()

        self.customerFullNameLineEdit = QLineEdit()
        self.customerEmailLineEdit = QLineEdit()

        self.dateEntryLineEdit = QDateEdit()
        self.dateEntryLineEdit.setCalendarPopup(True)
        self.dateEntryLineEdit.setDate(QDate.currentDate())
        self.dateEntryLineEdit.dateChanged.connect(self.changeRoomAmount)

        self.dateOutLineEdit = QDateEdit()
        self.dateOutLineEdit.setCalendarPopup(True)
        self.dateOutLineEdit.setDate(QDate.currentDate())
        self.dateOutLineEdit.dateChanged.connect(self.changeRoomAmount)

        self.roomIdLineEdit = QComboBox(self)
        self.amountLineEdit = QLineEdit()

        date_start = self.dateEntryLineEdit.date()
        date_end = self.dateOutLineEdit.date()

        start_date = datetime(date_start.year(), date_start.month(), date_start.day(), 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime(date_end.year(), date_end.month(), date_end.day(), 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
        availableRooms = searchAvailableRooms(start_date, end_date)

        self.roomDataList = {}
        roomNamesToShow = []
        for room in availableRooms:
            if room[1] not in roomNamesToShow:
                roomNamesToShow.append(room[1])

            roomData = {
                'id': room[0],
                'roomName': room[1],
                'capacity': room[2],
                'price': room[3],
            }
            self.roomDataList[room[1]] = roomData

        self.roomIdLineEdit.currentIndexChanged.connect(self.changeRoomAmount)
        self.roomIdLineEdit.addItems(roomNamesToShow)

        formLayout.addRow("Nombre del Cliente:", self.customerFullNameLineEdit)
        formLayout.addRow("Email del Cliente:", self.customerEmailLineEdit)
        formLayout.addRow("Fecha de Entrada:", self.dateEntryLineEdit)
        formLayout.addRow("Fecha de Salida:", self.dateOutLineEdit)
        formLayout.addRow("Habitación:", self.roomIdLineEdit)
        formLayout.addRow("Monto:", self.amountLineEdit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.insertReserve)
        buttons.rejected.connect(self.dialog.reject)

        formLayout.addRow(buttons)

        self.dialog.setLayout(formLayout)

        self.dialog.exec()

    def changeRoomAmount(self):
        roomName = self.roomIdLineEdit.currentText()
        # amountsPerDay = [100,200,500]

        date_entry = self.dateEntryLineEdit.date()
        date_out = self.dateOutLineEdit.date()

        difference = date_entry.daysTo(date_out)

        self.amountLineEdit.setText(str(self.roomDataList[roomName]['price'] * difference))

    def insertReserve(self):
        form_data = {
            'customer_full_name': self.customerFullNameLineEdit.text(),
            'customer_email': self.customerEmailLineEdit.text(),
            'date_entry': self.dateEntryLineEdit.text(),
            'date_out': self.dateOutLineEdit.text(),
            'room_id': self.roomDataList[self.roomIdLineEdit.currentText()]['id'],
            'amount': self.amountLineEdit.text(),
        }

        insertReservations(form_data)
        self.showAlert("Reserva agregada exitosamente")
        self.updateTableForEmail(self.customerEmailLineEdit.text())
        self.dialog.accept()

    def updateTable(self):
        data = getAllReserves()

        self.table.setRowCount(0)

        self.table.setRowCount(len(data))
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

            delete_button = QPushButton('Borrar')
            delete_button.clicked.connect(self.deleteRow)
            delete_button.setStyleSheet("background-color: red; color: white;")

            self.table.setCellWidget(row, 7, delete_button)

    def findForMail(self):
        self.updateTableForEmail(self.email_input.text())

    def updateTableForEmail(self, email):
        data = getAllReservesForMail(email)

        self.table.setRowCount(0)

        self.table.setRowCount(len(data))
        for row, rowData in enumerate(data):
            self.populateRow(row, [str(rowData['id']),
                str(rowData['customer_full_name']),
                str(rowData['customer_email']),
                str(rowData['date_entry']),
                str(rowData['date_out']),
                str(rowData['description']),
                str(rowData['amount']),
            ])

            today = date.today().strftime("%Y-%m-%d")
            if str(rowData['date_entry']) > today:
                delete_button = QPushButton('Cancelar Reserva')
                delete_button.clicked.connect(self.deleteRow)
                delete_button.setCursor(QCursor(Qt.PointingHandCursor))
                delete_button.setStyleSheet("background-color: #FF7F7F; color: white; border: 1px solid #FF7F7F;")
                delete_button.setStyleSheet("QPushButton:hover { background-color: #FF5050; color: white; border: 1px solid #FF5050; }")

                self.table.setCellWidget(row, 7, delete_button)

    def populateRow(self, row, elements):
        for index, element in enumerate(elements):
            item = QTableWidgetItem(str(element))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, index, item)

    def deleteRow(self):
        button = self.sender()
        if button:
            index = self.table.indexAt(button.pos())
            row = index.row()
            item = self.table.item(row, 0)
            id_value = item.text()

        result = removeReservation(id_value)

        if result:
            self.showAlert("Reserva borrada exitosamente")
        self.updateTableForEmail(self.table.item(row, 2).text())

    def showAlert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setIcon(QMessageBox.Information)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()

def main():
    app = QApplication()
    window = Reserves()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()