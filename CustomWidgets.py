from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel

class styledButton(QPushButton):
    def __init__(self, text, parent=None):
        super(styledButton, self).__init__(text, parent)
        self.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")

class styledWidget(QWidget):
    def __init__(self):
        super(styledWidget, self).__init__()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class styledLabel(QLabel):
    def __init__(self, text, parent=None):
        super(styledLabel, self).__init__(text, parent)
        self.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")

# Personalización de clases existentes
def customizeExistingClasses():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
    QApplication.instance().setPalette(palette)
    QApplication.setStyle('Fusion')
    QPushButton.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication()
    styled_widget = styledWidget()
    styled_button = styledButton("Haz clic")
    layout = QVBoxLayout(styled_widget)
    layout.addWidget(styled_button)
    styled_widget.show()
    app.exec_()
