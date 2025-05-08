from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QApplication, QPushButton
from core.clickable_button import ClickableButton

class Menu(QWidget):
    start_quiz_signal = Signal()
    show_settings_signal = Signal()
    stats_signal = Signal()
    login_signal = Signal()
    notes_signal = Signal()
    feedback_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("IQ Trainer")
        title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title_label.setStyleSheet("""QLabel{font-size: 30px; font-family: Poor Richard}""")
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

        play_button = ClickableButton("Играть")
        play_button.setFixedWidth(500)
        play_button.clicked.connect(self.start_quiz)
        verticalLayout.addWidget(play_button)

        login_button = ClickableButton("Авторизоваться/Зарегистрироваться")
        login_button.clicked.connect(self.show_login_form)
        verticalLayout.addWidget(login_button)

        settings_button = ClickableButton("Настройки")
        settings_button.clicked.connect(self.show_settings)
        verticalLayout.addWidget(settings_button)

        stats_button = ClickableButton("Статистика")
        stats_button.clicked.connect(self.show_stats)
        verticalLayout.addWidget(stats_button)

        notes_button = ClickableButton("Полезные сайты")
        notes_button.clicked.connect(self.show_notes)
        verticalLayout.addWidget(notes_button)

        feedback_button = ClickableButton("Оставить отзыв")
        feedback_button.clicked.connect(self.show_feedback)
        verticalLayout.addWidget(feedback_button)

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

    def show_stats(self):
        self.stats_signal.emit()

    def show_login_form(self):
        self.login_signal.emit()

    def show_notes(self):
        self.notes_signal.emit()

    def show_feedback(self):
        self.feedback_signal.emit()