from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout

from core.clickable_button import ClickableButton


class Settings(QWidget):
    choose_background_signal = Signal(int)
    change_text_size_signal = Signal(bool)
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.settings_layout = QGridLayout()
        self.settings_layout.setSpacing(10)
        self.settings_layout.setContentsMargins(100, 15, 100, 15)
        self.setLayout(self.settings_layout)

        choose_back_label = QLabel("Выбор фона")
        choose_back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        choose_back_label.setFixedHeight(50)

        self.score_label = QLabel()
        self.score_label.setFixedHeight(50)

        back1 = ClickableButton("1")
        back1.clicked.connect(lambda: self.choose_background(1))
        self.back2 = ClickableButton("2")
        self.back2.setEnabled(False)
        self.back2.clicked.connect(lambda: self.choose_background(2))
        self.back3 = ClickableButton("3")
        self.back3.setEnabled(False)
        self.back3.clicked.connect(lambda: self.choose_background(3))
        self.back4 = ClickableButton("4")
        self.back4.setEnabled(False)
        self.back4.clicked.connect(lambda: self.choose_background(4))

        back_button = ClickableButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)

        back2_layout = QVBoxLayout()
        self.back2_stop_label = QLabel("Необходимо очков: 50")
        self.back2_stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back2_stop_label.setFixedHeight(25)
        back2_layout.addWidget(self.back2)
        back2_layout.addWidget(self.back2_stop_label)
        back2_layout.setSpacing(2)

        back3_layout = QVBoxLayout()
        self.back3_stop_label = QLabel("Необходимо очков: 100")
        self.back3_stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back3_stop_label.setFixedHeight(25)
        back3_layout.addWidget(self.back3)
        back3_layout.addWidget(self.back3_stop_label)
        back3_layout.setSpacing(2)

        back4_layout = QVBoxLayout()
        self.back4_stop_label = QLabel("Необходимо очков: 150")
        self.back4_stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back4_stop_label.setFixedHeight(25)
        back4_layout.addWidget(self.back4)
        back4_layout.addWidget(self.back4_stop_label)
        back4_layout.setSpacing(2)

        self.size_label = QLabel("Размер текста")
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setFixedHeight(50)

        self.change_size_layout = QHBoxLayout()
        normal_size_button = ClickableButton("Обычный размер")
        normal_size_button.setFixedHeight(50)
        normal_size_button.clicked.connect(lambda: self.change_text_size(False))
        big_size_button = ClickableButton("Большой размер")
        big_size_button.setFixedHeight(50)
        big_size_button.clicked.connect(lambda: self.change_text_size(True))
        self.change_size_layout.addWidget(normal_size_button)
        self.change_size_layout.addWidget(big_size_button)

        self.achievements_label = QLabel("Достижения")
        self.achievements_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.achievements_label.setFixedHeight(50)

        self.achievements_layout = QHBoxLayout()
        all_achievements = ["Одарённый, но наоборот", "Гений", "Середняк"]
        for achievement in all_achievements:
            achievement_label = QLabel(f"{achievement}")
            achievement_label.setFixedHeight(50)
            achievement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            achievement_label.setStyleSheet("""QLabel {
                            border: 2px solid rgb(205, 9, 9);
                            font-family: 'Arial';
                        }
                        """)
            self.achievements_layout.addWidget(achievement_label)

        self.settings_layout.addWidget(choose_back_label, 0, 0, 1, 4)
        self.settings_layout.addWidget(self.score_label, 1, 0, 1, 4)
        self.settings_layout.addWidget(back1, 2, 0)
        self.settings_layout.addLayout(back2_layout, 2, 1)
        self.settings_layout.addLayout(back3_layout, 2, 2)
        self.settings_layout.addLayout(back4_layout, 2, 3)
        self.settings_layout.addWidget(self.size_label, 3, 0, 1, 4)
        self.settings_layout.addLayout(self.change_size_layout, 4, 0, 1, 4)
        self.settings_layout.addWidget(self.achievements_label, 7, 0, 1, 4)
        self.settings_layout.addLayout(self.achievements_layout, 8, 0, 1, 4)
        self.settings_layout.addWidget(back_button, 9, 0, 1, 4)

    def choose_background(self, choice):
        self.choose_background_signal.emit(choice)

    def back_buttons_block(self, score):
        if score < 50:
            self.back2.setEnabled(False)
            self.back2_stop_label.setVisible(True)
            self.back3.setEnabled(False)
            self.back3_stop_label.setVisible(True)
            self.back4.setEnabled(False)
            self.back4_stop_label.setVisible(True)
        elif 50 <= score < 100:
            self.back2.setEnabled(True)
            self.back2_stop_label.setVisible(False)
            self.back3.setEnabled(False)
            self.back3_stop_label.setVisible(True)
            self.back4.setEnabled(False)
            self.back4_stop_label.setVisible(True)
        elif 100 <= score < 150:
            self.back2.setEnabled(True)
            self.back2_stop_label.setVisible(False)
            self.back3.setEnabled(True)
            self.back3_stop_label.setVisible(False)
            self.back4.setEnabled(False)
            self.back4_stop_label.setVisible(True)
        else:
            self.back2.setEnabled(True)
            self.back2_stop_label.setVisible(False)
            self.back3.setEnabled(True)
            self.back3_stop_label.setVisible(False)
            self.back4.setEnabled(True)
            self.back4_stop_label.setVisible(False)

    def update_achievement_labels(self, achievements):
        for i in range(self.achievements_layout.count()):
            achievement_label = self.achievements_layout.itemAt(i).widget()
            style = (
                "QLabel {border: 2px solid rgb(58, 197, 53);}"
                if achievement_label.text() in achievements
                else "QLabel {border: 2px solid rgb(205, 9, 9);}"
            )
            achievement_label.setStyleSheet(style)

    def change_text_size(self, is_big):
        self.change_text_size_signal.emit(is_big)

    def return_to_menu(self):
        self.return_to_menu_signal.emit()