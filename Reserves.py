from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import *

class Reserves(QMainWindow):
    def __init__(self):
            super().__init__()
            self.setWindowState(Qt.WindowMaximized)

            self.setWindowTitle("Tabla de Información")
            self.setGeometry(100, 100, 600, 400)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            layout = QVBoxLayout()
            central_widget.setLayout(layout)

            self.addButton = QPushButton("Agregar Reserva")
            self.addButton.clicked.connect(self.addReserveModal)
            layout.addWidget(self.addButton)

            self.table = QTableWidget()
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(["id","customer_full_name","customer_email","date_entry","date_out","room_id","amount", "Action"])

            self.updateTable()

            self.salida = QLabel()
            self.salida.setText(f"Mis reservas")
            layout.addWidget(self.salida)

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