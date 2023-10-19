import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)

def main():
    app = QApplication(sys.argv)
    css = '*{font-size: 15px; background-color: #ffffff; color: #101212;}'
    app.setStyleSheet(css)
    some_app = Admin()
    some_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
