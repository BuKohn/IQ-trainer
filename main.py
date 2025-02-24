import sys
from ui.menu import Ui_MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = Ui_MainWindow()
sys.exit(app.exec())