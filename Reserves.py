import sys
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

            table = QTableWidget()
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(["id","customer_full_name","customer_email","date_entry","date_out","room_id","amount"])

            data = getAllReserves()
            table.setRowCount(len(data))

            for row, rowData in enumerate(data):
                for col, value in enumerate(rowData):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)

            self.salida = QLabel()
            self.salida.setText(f"Mis reservas")
            layout.addWidget(self.salida)

            layout.addWidget(table)

    def addReserveModal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Reserva")

        formLayout = QFormLayout()

        self.customerFullNameLineEdit = QLineEdit()
        self.customerEmailLineEdit = QLineEdit()
        self.dateEntryLineEdit = QLineEdit()
        self.dateOutLineEdit = QLineEdit()
        self.roomIdLineEdit = QLineEdit()
        self.amountLineEdit = QLineEdit()

        formLayout.addRow("Nombre del Cliente:", self.customerFullNameLineEdit)
        formLayout.addRow("Email del Cliente:", self.customerEmailLineEdit)
        formLayout.addRow("Fecha de Entrada:", self.dateEntryLineEdit)
        formLayout.addRow("Fecha de Salida:", self.dateOutLineEdit)
        formLayout.addRow("ID de la Habitación:", self.roomIdLineEdit)
        formLayout.addRow("Monto:", self.amountLineEdit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        formLayout.addRow(buttons)

        dialog.setLayout(formLayout)

        result = dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = Reserves()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()