from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QPushButton
import psycopg2
from psycopg2 import sql

user_data = {}
class Login(QWidget):
    registration_signal = Signal()
    logged_signal = Signal()
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.show_registration_page)
        layout.addWidget(self.register_button)

        self.return_to_menu_button = QPushButton("Вернуться в меню", self)
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        layout.addWidget(self.return_to_menu_button)

        self.setLayout(layout)

    @staticmethod
    def connect_db():
        conn = psycopg2.connect(
            dbname="iq_trainer_users",
            user="postgres",
            password="Kekiv118",
            host="localhost"
        )
        return conn

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            # Проверка существования пользователя
            cursor.execute(
                sql.SQL("SELECT password FROM users WHERE username = %s"),
                (username,)
            )
            user = cursor.fetchone()

            if user and user[0] == password:
                self.logged()
                self.return_to_menu()
                return True
            else:
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def logged(self):
        self.logged_signal.emit()

    def show_registration_page(self):
        self.registration_signal.emit()

    def return_to_menu(self):
        self.return_to_menu_signal.emit()


class Registration(QWidget):
    login_signal = Signal()
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Авторизоваться", self)
        self.login_button.clicked.connect(self.show_login_page)
        layout.addWidget(self.login_button)

        self.return_to_menu_button = QPushButton("Вернуться в меню", self)
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        layout.addWidget(self.return_to_menu_button)

        self.setLayout(layout)

    @staticmethod
    def connect_db():
        conn = psycopg2.connect(
            dbname="iq_trainer_users",
            user="postgres",
            password="Kekiv118",
            host="localhost"
        )
        return conn

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            # Вставка нового пользователя
            cursor.execute(
                sql.SQL("INSERT INTO users (username, password) VALUES (%s, %s)"),
                (username, password)
            )
            conn.commit()
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cursor.close()
            conn.close()
            self.return_to_menu()

    def show_login_page(self):
        self.login_signal.emit()

    def return_to_menu(self):
        self.return_to_menu_signal.emit()