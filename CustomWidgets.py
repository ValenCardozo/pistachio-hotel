from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super(StyledButton, self).__init__(text, parent)
        self.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")

class StyledWidget(QWidget):
    def __init__(self):
        super(StyledWidget, self).__init__()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class StyledLabel(QLabel):
    def __init__(self, text, parent=None):
        super(StyledLabel, self).__init__(text, parent)
        self.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")

# Personalización de clases existentes
def customizeExistingClasses():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
    QApplication.instance().setPalette(palette)
    QApplication.setStyle('Fusion')
    QPushButton.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    styled_widget = StyledWidget()
    styled_button = StyledButton("Haz clic")
    layout = QVBoxLayout(styled_widget)
    layout.addWidget(styled_button)
    styled_widget.show()
    sys.exit(app.exec_())
