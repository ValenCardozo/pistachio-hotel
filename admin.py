import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from database import getAllRooms, deleteRoom, insertRoom, updateRoomById
from UpdateRoom import *

class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.initUI()
        self.adjust_input_group_width()
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_frame.setFrameShadow(QFrame.Raised)
        header_frame.setMaximumHeight(80)
        header_frame.setStyleSheet("background-color: #8db600; color: white; font-weight: bold; border: 1px solid black;")
        header_layout = QHBoxLayout(header_frame)

        title_label = QLabel("Hotel Pistacho Administración", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setFixedHeight(20)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        main_layout.addWidget(header_frame)

        self.input_group = QGroupBox("Detalles de la habitación")
        self.input_group.setStyleSheet("border: 1px solid #d3d3d3; margin-top: 0.5em;")

        self.input_group.setFixedHeight(400)
        input_layout = QVBoxLayout(self.input_group)

        cant_personas_label = QLabel("Cantidad de personas:", self)
        cant_personas_label.setFixedHeight(30)
        cant_personas_label.setStyleSheet("background-color: #eeeeee; color: #000000;")
        self.cant_personas_input = QLineEdit(self)
        self.cant_personas_input.setFixedHeight(25)

        description_label = QLabel("Descripción:", self)
        description_label.setFixedHeight(30)
        description_label.setStyleSheet("background-color: #eeeeee; color: #000000;")
        self.description_input = QLineEdit(self)
        self.description_input.setFixedHeight(25)

        price_label = QLabel("Costo p/noche:", self)
        price_label.setFixedHeight(30)
        price_label.setStyleSheet("background-color: #eeeeee; color: #000000;")
        self.price_input = QLineEdit(self)
        self.price_input.setFixedHeight(25)

        create_button = QPushButton("Crear", self)
        create_button.setFixedWidth(200)
        create_button.setStyleSheet("background-color: #c3d9af;")

        input_layout.addWidget(cant_personas_label)
        input_layout.addWidget(self.cant_personas_input)
        input_layout.addWidget(description_label)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(price_label)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(create_button)

        left_layout.addWidget(self.input_group)

        self.rooms_layout = QVBoxLayout()
        right_layout.addLayout(self.rooms_layout)

        h_layout = QHBoxLayout()
        h_layout.addLayout(left_layout)
        h_layout.addStretch(1)
        h_layout.addLayout(right_layout)

        main_layout.addLayout(h_layout)

        self.populate_rooms()

        create_button.clicked.connect(self.add_room)

    def populate_rooms(self):
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

        rooms = getAllRooms()
        if rooms != []:
            for room in rooms:
                id, description, cantPersons, price = room[0], room[1], room[2], room[3]

                room_frame = QFrame(self)
                room_frame.setFrameShape(QFrame.StyledPanel)
                room_frame.setFrameShadow(QFrame.Raised)
                room_frame_layout = QVBoxLayout(room_frame)
                room_frame.setMaximumHeight(50)
                room_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                room_frame.setStyleSheet("border: 1px solid black;")

                item_layout = QHBoxLayout()
                item_label = QLabel(f" {description} - {cantPersons} personas - ${price}")
                self.update_button = QPushButton("Actualizar")
                self.update_button.setFixedWidth(75)
                self.update_button.setStyleSheet("background-color: #99dee6; color: #ffffff;")
                self.update_button.clicked.connect(lambda
                    room_id=id,
                    desc=description,
                    persons=cantPersons,
                    price=price: self.show_update_dialog(room_id, desc, persons, price)
                )

                delete_button = QPushButton("Borrar")
                delete_button.setFixedWidth(75)
                delete_button.setStyleSheet("background-color: #ff0125; color: #ffffff;")

                delete_button.clicked.connect(lambda
                    desc=description,
                    persons=cantPersons,
                    price_val=price: self.delete_room(desc, persons, price_val)
                )

                item_layout.addWidget(item_label)
                item_layout.addWidget(self.update_button)
                item_layout.addWidget(delete_button)

                room_frame_layout.addLayout(item_layout)

                self.rooms_layout.addWidget(room_frame)

    def adjust_input_group_width(self):
        self.input_group.setFixedWidth(self.width() * 0.45)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_input_group_width()

    def add_room(self):
        description = self.description_input.text()
        capacity = int(self.cant_personas_input.text())
        price = int(self.price_input.text())
        insertRoom(description, capacity, price)
        self.populate_rooms()


    def delete_room(self, description, cantPersons, price):
        deleteRoom(description, cantPersons, price)
        self.populate_rooms()

    def show_update_dialog(self, room_id, description, capacity, price):
        dialog = UpdateRoomDialog(room_id, description, capacity, price, self)

        if dialog.exec_():
            updated_description = dialog.get_description()
            updated_capacity = dialog.get_capacity()
            updated_price = dialog.get_price()
            self.update_room(room_id, updated_description, updated_capacity, updated_price)

    def update_room(self, room_id, description, capacity, price):
        updateRoomById(room_id, description, capacity, price)
        self.populate_rooms()

def main():
    app = QApplication(sys.argv)
    some_app = Admin()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
