from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import *

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

            # Encabezado personalizado en la esquina superior izquierda
            header_label = QLabel("Hotel Pistacho - Mis Reservas")
            header_label.setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px; padding: 10px;")
            layout.addWidget(header_label, alignment=Qt.AlignTop | Qt.AlignLeft)

            grid_layout = QGridLayout()

            email_label = QLabel("Correo Electrónico:")
            email_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.email_input = QLineEdit()
            self.email_input.setFixedWidth(150)
            search_button = QPushButton("Buscar")
            search_button.clicked.connect(self.updateTableForEmail)
            search_button.setFixedWidth(80)

            grid_layout.addWidget(email_label, 0, 0)
            grid_layout.addWidget(self.email_input, 0, 1)
            grid_layout.addWidget(search_button, 0, 2)
            grid_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed), 0, 3)  # Espacio en la derecha

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
        self.roomIdLineEdit.currentIndexChanged.connect(self.changeRoomAmount)
        self.roomIdLineEdit.addItems(['comfort','suite','presidential']) #Editar

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
        roomId = self.roomIdLineEdit.currentIndex()
        amountsPerDay = [100,200,500]

        date_entry = self.dateEntryLineEdit.date()
        date_out = self.dateOutLineEdit.date()

        difference = date_entry.daysTo(date_out)

        self.amountLineEdit.setText(str(amountsPerDay[roomId] * difference))

    def insertReserve(self):
        form_data = {
            'customer_full_name': self.customerFullNameLineEdit.text(),
            'customer_email': self.customerEmailLineEdit.text(),
            'date_entry': self.dateEntryLineEdit.text(),
            'date_out': self.dateOutLineEdit.text(),
            'room_id': self.roomIdLineEdit.text(),
            'amount': self.amountLineEdit.text(),
        }

        insertReservations(form_data)
        self.showAlert("Reserva agregada exitosamente")
        self.updateTable()
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

    def updateTableForEmail(self):
        data = getAllReservesForMail(self.email_input.text())

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
        self.updateTable()

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