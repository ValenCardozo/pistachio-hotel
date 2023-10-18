# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, 
#     QLabel, QVBoxLayout, 
#     QWidget, QLineEdit, QPushButton)
# from PySide6.QtCore import QSize

import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class Home(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ### this line here is what you'd be looking for
        self.setWindowState(Qt.WindowMaximized)
        ###
        self.show()


def main():
    app = QApplication(sys.argv)
    some_app = Home()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
