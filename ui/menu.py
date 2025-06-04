from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QApplication, QPushButton
from core.clickable_button import ClickableButton
from ui.text import text

class Menu(QWidget):
    start_quiz_signal = Signal()
    show_settings_signal = Signal()
    stats_signal = Signal()
    login_signal = Signal()
    notes_signal = Signal()
    feedback_signal = Signal()
    custom_quiz_signal = Signal()

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
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

        self.play_button = ClickableButton(text[self.lang]["menu"]["play_btn"])
        self.play_button.setFixedWidth(500)
        self.play_button.clicked.connect(self.start_quiz)
        verticalLayout.addWidget(self.play_button)

        self.login_button = ClickableButton(text[self.lang]["menu"]["login_btn"])
        self.login_button.clicked.connect(self.show_login_form)
        verticalLayout.addWidget(self.login_button)

        self.settings_button = ClickableButton(text[self.lang]["menu"]["settings_btn"])
        self.settings_button.clicked.connect(self.show_settings)
        verticalLayout.addWidget(self.settings_button)

        self.stats_button = ClickableButton(text[self.lang]["menu"]["stats_btn"])
        self.stats_button.clicked.connect(self.show_stats)
        verticalLayout.addWidget(self.stats_button)

        self.custom_quiz_button = ClickableButton(text[self.lang]["menu"]["custom_quiz_btn"])
        self.custom_quiz_button.clicked.connect(self.show_custom_quiz)
        verticalLayout.addWidget(self.custom_quiz_button)

        self.notes_button = ClickableButton(text[self.lang]["menu"]["notes_btn"])
        self.notes_button.clicked.connect(self.show_notes)
        verticalLayout.addWidget(self.notes_button)

        self.feedback_button = ClickableButton(text[self.lang]["menu"]["feedback_btn"])
        self.feedback_button.clicked.connect(self.show_feedback)
        verticalLayout.addWidget(self.feedback_button)

        self.exit_button = QPushButton(text[self.lang]["menu"]["exit_btn"])
        verticalLayout.addWidget(self.exit_button)
        self.exit_button.clicked.connect(QApplication.quit)

        self.account_label = QLabel(text[self.lang]["menu"]["account_label"])
        self.account_label.setVisible(False)
        self.menu_layout.addWidget(self.account_label)

        self.setLayout(self.menu_layout)

    def apply_language(self, lang):
        self.lang = lang
        self.play_button.setText(text[self.lang]["menu"]["play_btn"])
        self.login_button.setText(text[self.lang]["menu"]["login_btn"])
        self.settings_button.setText(text[self.lang]["menu"]["settings_btn"])
        self.stats_button.setText(text[self.lang]["menu"]["stats_btn"])
        self.custom_quiz_button.setText(text[self.lang]["menu"]["custom_quiz_btn"])
        self.notes_button.setText(text[self.lang]["menu"]["notes_btn"])
        self.feedback_button.setText(text[self.lang]["menu"]["feedback_btn"])
        self.exit_button.setText(text[self.lang]["menu"]["exit_btn"])
        self.account_label.setText(text[self.lang]["menu"]["account_label"])

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

    def show_custom_quiz(self):
        self.custom_quiz_signal.emit()