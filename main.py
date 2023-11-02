from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from updateRoom import *
from PySide6.QtGui import QPixmap
from home import *
from customWidgets import *

class Welcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fafafa; color: #000000;")
        self.setMinimumSize(800, 600)
        self.initUI()

    def initUI(self):
        title_label = QLabel("Hotel Pistachio", self)
        title_font = QFont()
        title_font.setItalic(True)
        title_font.setPointSize(50)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(200, 10, 400, 40)

        self.setWindowTitle("Información del Hotel")
        self.setGeometry(100, 100, 800, 200)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(100, 70, 600, 200)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("Información del hotel")
        self.text_edit.setStyleSheet("border: none;")

        with open('source/archivo.txt', 'r') as file:
            texto = file.read()
            self.text_edit.setPlainText(texto)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(200, 210, 400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.image_paths = ["source/image1.jpeg", "source/image2.jpeg", "source/image3.jpeg", "source/image4.jpeg"]
        self.current_image = 0
        self.load_image()

        self.prev_button = QPushButton(self)
        self.prev_button.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")
        self.prev_button.setGeometry(250, 520, 40, 30)
        self.prev_button.setIcon(QIcon('source/arrow-left.svg'))
        self.prev_button.clicked.connect(self.show_previous_image)

        self.next_button = QPushButton(self)
        self.next_button.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")
        self.next_button.setGeometry(510, 520, 40, 30)
        self.next_button.setIcon(QIcon('source/arrow-rigth.svg'))
        self.next_button.clicked.connect(self.show_next_image)

        self.mainButton = styledButton("Hacer una reserva!", self)
        self.mainButton.clicked.connect(self.openMain)
        self.mainButton.setGeometry(325, 550, 150, 30)

    def load_image(self):
        if 0 <= self.current_image < len(self.image_paths):
            pixmap = QPixmap(self.image_paths[self.current_image])
            self.image_label.setPixmap(pixmap)
            self.image_label.setStyleSheet("border: 2px solid #8db600; border-radius: 10px;")

    def show_previous_image(self):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = len(self.image_paths) - 1
        self.load_image()

    def show_next_image(self):
        self.current_image += 1
        if self.current_image >= len(self.image_paths):
            self.current_image = 0
        self.load_image()

    def openMain(self):
        self.main = home()
        self.main.show()
        self.close()

def main():
    app = QApplication()
    some_app = Welcome()
    some_app.show()
    app.exec()

if __name__ == "__main__":
    main()
