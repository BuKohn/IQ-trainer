from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QPushButton, QApplication


class Menu(QWidget):
    start_quiz_signal = Signal()
    show_settings_signal = Signal()
    login_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel()
        title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title_label.setText("IQ Trainer")
        font = QFont()
        font.setFamilies([u"Poor Richard"])
        font.setPointSize(30)
        title_label.setFont(font)
        title_label.setScaledContents(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_container = QHBoxLayout()
        title_container.addStretch()
        title_container.addWidget(title_label)
        title_container.addStretch()

        self.menu_layout = QVBoxLayout()
        self.menu_layout.setContentsMargins(0, 100, 0, 0)
        verticalLayout = QVBoxLayout()
        verticalLayout.setContentsMargins(250, 0, 250, 0)
        verticalLayout.setAlignment(Qt.AlignCenter)
        self.menu_layout.addStretch()
        self.menu_layout.addLayout(title_container)
        self.menu_layout.addLayout(verticalLayout)
        self.menu_layout.addStretch()

        play_button = QPushButton("Играть")
        play_button.setFixedWidth(500)
        play_button.clicked.connect(self.start_quiz)
        verticalLayout.addWidget(play_button)

        login_button = QPushButton("Авторизоваться/Зарегистрироваться")
        login_button.clicked.connect(self.show_login_form)
        verticalLayout.addWidget(login_button)

        settings_button = QPushButton("Настройки")
        settings_button.clicked.connect(self.show_settings)
        verticalLayout.addWidget(settings_button)

        exit_button = QPushButton("Выход")
        verticalLayout.addWidget(exit_button)
        exit_button.clicked.connect(QApplication.quit)

        self.account_label = QLabel("Вы вошли в аккаунт!")
        self.account_label.setVisible(False)
        self.menu_layout.addWidget(self.account_label)

        self.setLayout(self.menu_layout)

    def start_quiz(self):
        self.start_quiz_signal.emit()

    def show_settings(self):
        self.show_settings_signal.emit()

    def show_login_form(self):
        self.login_signal.emit()