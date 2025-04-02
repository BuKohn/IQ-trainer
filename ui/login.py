from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from psycopg2 import sql

from core.db import connect_db


class Login(QWidget):
    registration_signal = Signal()
    logged_signal = Signal(str, int, list)
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Белый блок фиксированного размера
        self.white_block = QWidget()
        self.white_block.setFixedSize(400, 500)
        self.white_block.setStyleSheet("background-color: white; border-radius: 10px;")

        # Макет для белого блока
        layout = QVBoxLayout(self.white_block)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        login_label = QLabel("Авторизация")
        login_label.setFixedHeight(50)
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial'; 
                font-size: 24px;
                font-weight: bold;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
            }
        """)

        layout.addWidget(login_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")

        self.username_error_label = QLabel("*Неверное имя пользователя", self)
        self.username_error_label.setFixedSize(200, 25)
        self.username_error_label.setStyleSheet("color: red; background-color: transparent; border: none;")
        self.username_error_label.setVisible(False)

        login_layout = QVBoxLayout()
        login_layout.setSpacing(0)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.username_error_label)

        layout.addLayout(login_layout)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.password_error_label = QLabel("*Неверный пароль", self)
        self.password_error_label.setFixedSize(200, 25)
        self.password_error_label.setStyleSheet("color: red; background-color: transparent; border: none;")
        self.password_error_label.setVisible(False)

        password_layout = QVBoxLayout()
        password_layout.setSpacing(0)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.password_error_label)

        layout.addLayout(password_layout)

        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.show_registration_page)

        self.return_to_menu_button = QPushButton("Вернуться в меню", self)
        self.return_to_menu_button.clicked.connect(self.return_to_menu)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.register_button)
        buttons_layout.addWidget(self.return_to_menu_button)
        buttons_layout.setSpacing(15)

        layout.addLayout(buttons_layout)

        # Добавляем белый блок в главный макет
        self.main_layout.addWidget(self.white_block, alignment=Qt.AlignCenter)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Проверка существования пользователя
            cursor.execute(
                sql.SQL("SELECT username, password, high_score, achievements FROM users WHERE username = %s"),
                (username,)
            )
            user = cursor.fetchone()
            print(user)

            if user is not None:
                if user[1] == password:
                    # Успешная авторизация
                    self.logged(user[0], user[2], user[3])
                    self.return_to_menu()
                    self.clear_errors()  # Очищаем ошибки
                    return True
                else:
                    # Неверный пароль
                    self.password_error_label.setVisible(True)
                    self.username_error_label.setVisible(False)
                    return False
            else:
                # Неверное имя пользователя
                self.username_error_label.setVisible(True)
                self.password_error_label.setVisible(False)
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def clear_errors(self):
        """Очищает сообщения об ошибках."""
        self.username_error_label.setVisible(False)
        self.password_error_label.setVisible(False)
        self.username_input.clear()
        self.password_input.clear()

    def logged(self, username, score, achievements):
        self.logged_signal.emit(username, score, achievements)

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
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.white_block = QWidget()
        self.white_block.setFixedSize(400, 500)
        self.white_block.setStyleSheet("background-color: white; border-radius: 10px;")

        # Макет для белого блока
        layout = QVBoxLayout(self.white_block)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        login_label = QLabel("Регистрация")
        login_label.setFixedHeight(50)
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.setStyleSheet("""
                    QLabel {
                        font-family: 'Arial'; 
                        font-size: 24px;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 5px;
                        text-align: center;
                    }
                """)

        layout.addWidget(login_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")

        self.username_error_label = QLabel("", self)
        self.username_error_label.setFixedSize(500, 50)
        self.username_error_label.setStyleSheet("color: red; background-color: transparent; border: none;")
        self.username_error_label.setVisible(False)  # Изначально скрыт

        login_layout = QVBoxLayout()
        login_layout.setSpacing(0)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.username_error_label)

        layout.addLayout(login_layout)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.password_error_label = QLabel("*Пароль должен быть больше 4 символов", self)
        self.password_error_label.setFixedSize(200, 25)
        self.password_error_label.setStyleSheet("color: red; background-color: transparent; border: none;")
        self.password_error_label.setVisible(False)  # Изначально скрыт

        password_layout = QVBoxLayout()
        password_layout.setSpacing(0)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.password_error_label)

        layout.addLayout(password_layout)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Авторизоваться", self)
        self.login_button.clicked.connect(self.show_login_page)

        self.return_to_menu_button = QPushButton("Вернуться в меню", self)
        self.return_to_menu_button.clicked.connect(self.return_to_menu)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.return_to_menu_button)
        layout.addLayout(buttons_layout)

        self.main_layout.addWidget(self.white_block, alignment=Qt.AlignCenter)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if len(password) <= 4:
            self.password_error_label.setVisible(True)
            self.username_error_label.setVisible(False)
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Вставка нового пользователя
            cursor.execute(
                sql.SQL("INSERT INTO users (username, password) VALUES (%s, %s)"),
                (username, password)
            )
            conn.commit()
            self.clear_errors()
            self.return_to_menu()
        except Exception as e:
            self.username_error_label.setText(f"Ошибка: {e}")
            self.password_error_label.setVisible(False)
            self.username_error_label.setVisible(True)
        finally:
            cursor.close()
            conn.close()

    def clear_errors(self):
        """Очищает сообщения об ошибках."""
        self.username_error_label.setVisible(False)
        self.password_error_label.setVisible(False)
        self.username_input.clear()
        self.password_input.clear()

    def show_login_page(self):
        self.login_signal.emit()

    def return_to_menu(self):
        self.return_to_menu_signal.emit()