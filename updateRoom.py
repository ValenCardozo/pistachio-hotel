from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from database import updateRoomById

class updateRoomDialog(QDialog):
    def __init__(self, room_id, description, capacity, price, parent=None):
        super().__init__(parent)
        self.room_id = room_id

        layout = QVBoxLayout(self)

        self.description_input = QLineEdit(description)
        self.capacity_input = QLineEdit(str(capacity))
        self.price_input = QLineEdit(str(price))

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Capacidad:"))
        layout.addWidget(self.capacity_input)
        layout.addWidget(QLabel("Precio por noche:"))
        layout.addWidget(self.price_input)
        layout.addWidget(save_button)

    def save_changes(self):
        new_description = self.description_input.text()
        new_capacity = int(self.capacity_input.text())
        new_price = int(self.price_input.text())

        updateRoomById(self.room_id, new_description, new_capacity, new_price)
        self.accept()

    def get_description(self):
        return self.description_input.text()

    def get_capacity(self):
        return int(self.capacity_input.text())

    def get_price(self):
        return int(self.price_input.text())

