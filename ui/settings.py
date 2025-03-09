from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


class Settings(QWidget):
    choose_background_signal = Signal(int)
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.settings_layout = QVBoxLayout()
        self.setLayout(self.settings_layout)

        background_layout = QHBoxLayout()
        back1 = QPushButton("1")
        back1.clicked.connect(lambda: self.choose_background(1))
        back2 = QPushButton("2")
        back2.clicked.connect(lambda: self.choose_background(2))
        back3 = QPushButton("3")
        back3.clicked.connect(lambda: self.choose_background(3))
        back4 = QPushButton("4")
        back4.clicked.connect(lambda: self.choose_background(4))
        background_layout.addWidget(back1)
        background_layout.addWidget(back2)
        background_layout.addWidget(back3)
        background_layout.addWidget(back4)
        back_button = QPushButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)

        choose_back_label = QLabel("Выбор фона")
        choose_back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        choose_back_label.resize(self.width(), 400)
        self.settings_layout.addWidget(choose_back_label)
        self.settings_layout.addLayout(background_layout)
        self.settings_layout.addStretch()
        self.settings_layout.addWidget(back_button)

    def choose_background(self, choice):
        self.choose_background_signal.emit(choice)

    def return_to_menu(self):
        self.return_to_menu_signal.emit()