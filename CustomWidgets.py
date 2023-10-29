from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel

# Clase personalizada para un QPushButton con estilo
class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super(StyledButton, self).__init__(text, parent)
        self.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")
        self.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        print("Botón clicado")

# Clase personalizada para un QWidget con estilo
class StyledWidget(QWidget):
    def __init__(self):
        super(StyledWidget, self).__init__()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
        self.setPalette(palette)
        self.setAutoFillBackground(True)

# Personalización de clases existentes
def customizeExistingClasses():
    # Personalización de QWidget
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(141, 182, 0))  # Pistacho
    QApplication.instance().setPalette(palette)
    QApplication.setStyle('Fusion')

    # Personalización de QPushButton
    QPushButton.setStyleSheet("background-color: #8db600; color: white; font-weight: bold;")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Crear una instancia de la clase personalizada StyledWidget
    styled_widget = StyledWidget()

    # Crear una instancia de la clase personalizada StyledButton
    styled_button = StyledButton("Haz clic")

    # Configurar un diseño y agregar el botón al widget
    layout = QVBoxLayout(styled_widget)
    layout.addWidget(styled_button)

    # Personalizar clases existentes
    # customizeExistingClasses()

    styled_widget.show()
    sys.exit(app.exec_())
