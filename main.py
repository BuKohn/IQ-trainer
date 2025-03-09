import sys
from ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())