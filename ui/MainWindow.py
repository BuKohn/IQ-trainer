import json
import os
from PySide6.QtCore import Qt, QLocale
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QLabel
from psycopg2 import sql

from ui.menu import Menu
from ui.quiz import Quiz
from ui.settings import Settings
from ui.login import Login, Registration
from core.db import connect_db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "core/settings.json"
        self.username = None
        self.user_score = 0
        self.setup_ui()

    def load_setting(self, key, default):
        """Загружает настройку из settings.json."""
        if not os.path.exists(self.settings_file):
            return default
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get(key, default)
        except json.JSONDecodeError:
            return default

    def save_setting(self, key, value):
        """Сохраняет настройку в settings.json."""
        settings = {}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except json.JSONDecodeError:
                pass
        settings[key] = value
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    def setup_ui(self):
        self.setStyleSheet(f"""
        QMainWindow{{
	        background-image: url({self.load_setting("background_image", "assets/back1.jpg")});
	        background-repeat: no-repeat;
            background-position: center;
            background-attachment: scroll;
            background-size: contain;
        }}
        """)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.setStyleSheet("""
        QLabel {
	        background-color: rgb(255, 253, 253);
	        border-radius: 5px;
	        border: 5px solid rgb(55, 107, 113);
        }
        QPushButton {
	        background-color: rgb(255, 253, 253);
	        border-radius: 5px;
	        border: 1px solid rgb(178, 224, 235);
	        padding: 10px 10px;
	        color: rgb(55, 107, 113);
	        font: Poor Richard;
	        font-size: 14px;
        }
        QPushButton:hover {
	        color: rgb(45, 97, 100);
	        border: 1px solid rgb(55, 107, 113);
            cursor: pointer;
        }
        QLineEdit {
            background-color: rgb(255, 253, 253);
            border: 2px solid rgb(55, 107, 113);
            border-radius: 5px;
            padding: 8px;
            font: Poor Richard;
            font-size: 14px;
            color: rgb(55, 107, 113);
        }
        QLineEdit:focus {
            border: 2px solid rgb(45, 97, 100);
            outline: none;
        }
        """)

        self.menu_widget = Menu()
        self.menu_widget.start_quiz_signal.connect(self.start_quiz)
        self.menu_widget.show_settings_signal.connect(self.show_settings)
        self.menu_widget.login_signal.connect(self.show_login_page)
        self.stacked_widget.addWidget(self.menu_widget)

        self.quiz_widget = Quiz()
        self.stacked_widget.addWidget(self.quiz_widget)

        self.settings_widget = Settings()
        self.settings_widget.choose_background_signal.connect(self.choose_background)
        self.settings_widget.return_to_menu_signal.connect(self.return_to_menu)
        self.stacked_widget.addWidget(self.settings_widget)

        self.login_widget = Login()
        self.login_widget.registration_signal.connect(self.show_registration_page)
        self.login_widget.logged_signal.connect(self.logged)
        self.login_widget.return_to_menu_signal.connect(self.return_to_menu)
        self.stacked_widget.addWidget(self.login_widget)

        self.registration_widget = Registration()
        self.registration_widget.login_signal.connect(self.show_login_page)
        self.registration_widget.return_to_menu_signal.connect(self.return_to_menu)
        self.stacked_widget.addWidget(self.registration_widget)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def choose_background(self, choice):
        backs = {1: "assets/back1.jpg", 2: "assets/back2.png", 3: "assets/back3.jpg", 4: "assets/back4.jpg"}
        self.setStyleSheet(f"""
        QMainWindow{{
	        background-image: url({backs[choice]});
	        background-repeat: no-repeat;
            background-position: center;
            background-attachment: scroll;
            background-size: contain;
        }}
        """)
        self.save_setting("background_image", backs[choice])

    def logged(self, username, score):
        self.username = username
        self.menu_widget.account_label.setVisible(True)
        self.user_score = score

    def update_score(self, score):
        if score >= self.user_score:
            self.user_score = score
            if self.username:
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        sql.SQL("UPDATE users SET high_score = %s WHERE username = %s"),
                        (score, self.username)
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Ошибка: {e}")
                finally:
                    cursor.close()
                    conn.close()


    def return_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)

    def start_quiz(self):
        self.stacked_widget.removeWidget(self.quiz_widget)
        self.quiz_widget = Quiz()
        self.quiz_widget.return_to_menu_signal.connect(self.return_to_menu)
        self.quiz_widget.update_score_signal.connect(self.update_score)
        self.stacked_widget.insertWidget(1, self.quiz_widget)
        self.stacked_widget.setCurrentIndex(1)

    def show_settings(self):
        self.settings_widget.score_label.setText(f"Ваш лучший счёт: {self.user_score}")
        self.settings_widget.back_buttons_block(self.user_score)
        self.stacked_widget.setCurrentIndex(2)

    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_registration_page(self):
        self.stacked_widget.setCurrentIndex(4)