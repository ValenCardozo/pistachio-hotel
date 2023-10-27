import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import getAllRooms, deleteRoom, insertRoom

class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Create Title
        title_label = QLabel("Hotel Pistacho Administración", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(7)  # Cambia esto a un valor más pequeño.
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setFixedHeight(20)
        left_layout.addWidget(title_label)
        left_layout.setContentsMargins(5, 5, 5, 5)  # Ajusta estos valores según lo que necesites.
        left_layout.setSpacing(3)

        # Create a QGroupBox for input fields
        input_group = QGroupBox("Detalles de la habitación")
        input_group.setFixedHeight(500)
        input_layout = QVBoxLayout(input_group)

        cant_personas_label = QLabel("Cant. personas", self)
        cant_personas_label.setFixedHeight(15)
        self.cant_personas_input = QLineEdit(self)
        self.cant_personas_input.setFixedHeight(18)

        description_label = QLabel("Descripción", self)
        description_label.setFixedHeight(15)
        self.description_input = QLineEdit(self)
        self.description_input.setFixedHeight(18)

        price_label = QLabel("Costo p/noche", self)
        price_label.setFixedHeight(15)
        self.price_input = QLineEdit(self)
        self.price_input.setFixedHeight(18)

        create_button = QPushButton("Crear", self)

        input_layout.addWidget(cant_personas_label)
        input_layout.addWidget(self.cant_personas_input)
        input_layout.addWidget(description_label)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(price_label)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(create_button)

        input_layout.setSpacing(5)
        input_layout.setContentsMargins(5, 5, 5, 5)

        left_layout.addWidget(input_group)


        self.rooms_layout = QVBoxLayout()
        right_layout.addLayout(self.rooms_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.populate_rooms()

        central_widget.setLayout(main_layout)
        create_button.clicked.connect(self.add_room)

    def populate_rooms(self):
        # Limpiamos el layout de habitaciones
        for i in reversed(range(self.rooms_layout.count())):
            item = self.rooms_layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            elif isinstance(item, QLayout):
                for j in reversed(range(item.count())):
                    subitem = item.itemAt(j)
                    widget = subitem.widget()
                    if widget is not None:
                        widget.deleteLater()
                while item.count():
                    item.takeAt(0)

        # Luego de limpiar, agregamos los nuevos registros
        rooms = getAllRooms()
        if rooms != []:
            for room in rooms:
                description, cantPersons, price = room[1], room[2], room[3]
                item_layout = QHBoxLayout()
                item_label = QLabel(f"{description} - {cantPersons} personas - ${price}")
                update_button = QPushButton("Actualizar")
                delete_button = QPushButton("Borrar")

                # Conectar el botón de borrar a la función delete_room y pasar la descripción
                delete_button.clicked.connect(lambda desc=description, persons=cantPersons, price_val=price: self.delete_room(desc, persons, price_val))

                item_layout.addWidget(item_label)
                item_layout.addWidget(update_button)
                item_layout.addWidget(delete_button)
                self.rooms_layout.addLayout(item_layout)

    def add_room(self):
        description = self.description_input.text()
        capacity = int(self.cant_personas_input.text())
        price = int(self.price_input.text())
        insertRoom(description, capacity, price)

        self.populate_rooms()


    def delete_room(self, description, cantPersons, price):
        deleteRoom(description, cantPersons, price)

        self.populate_rooms()

def main():
    app = QApplication(sys.argv)
    css = '*{font-size: 15px; background-color: #ffff42; color: #101212;}'
    app.setStyleSheet(css)
    some_app = Admin()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
