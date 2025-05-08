from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel
)
import requests
from core.clickable_button import ClickableButton

class Feedback(QWidget):
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfzfEBPogDHWSQ-rzaxMU3pxI-xk73B7MEK1Djg57YDDwuMQw/formResponse"
        self.field_names = {
            "name": "entry.601811216",
            "feedback": "entry.2102964646"
        }
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(10)

        container = QWidget()
        container.setFixedSize(900, 500)
        container.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
        self.main_layout.addWidget(container)

        # Создаем макет внутри контейнера
        layout_inside_container = QVBoxLayout(container)
        layout_inside_container.setAlignment(Qt.AlignTop)
        layout_inside_container.setContentsMargins(20, 20, 20, 20)  # Внутренние отступы

        title = QLabel("Оставить отзыв")
        title.setFixedHeight(50)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
                            QLabel {
                                font-family: 'Arial'; 
                                font-size: 24px;
                                font-weight: bold;
                                border-radius: 10px;
                                padding: 5px;
                                text-align: center;
                            }
                        """)

        layout_inside_container.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя...")
        layout_inside_container.addWidget(self.name_input)
        self.feedback_text = QTextEdit()
        self.feedback_text.setPlaceholderText("Введите ваш отзыв здесь...")
        layout_inside_container.addWidget(self.feedback_text)

        self.send_button = ClickableButton("Отправить отзыв")
        self.send_button.clicked.connect(self.send_feedback)
        layout_inside_container.addWidget(self.send_button)

        self.error_label = QLabel()
        self.error_label.setFixedSize(400, 15)
        self.error_label.setStyleSheet("color: red; background-color: transparent; border: none;")
        self.error_label.setVisible(False)
        layout_inside_container.addWidget(self.error_label)

        self.return_to_menu_button = ClickableButton("Вернуться в меню")
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        layout_inside_container.addWidget(self.return_to_menu_button)

    def send_feedback(self):
        """Отправляет отзыв через Google Forms."""
        name = self.name_input.text().strip()
        feedback = self.feedback_text.toPlainText().strip()

        if not name or not feedback:
            self.error_label.setText("*Пожалуйста, заполните все поля")
            self.error_label.setVisible(True)
            return

        try:
            # Формируем данные для отправки
            data = {
                self.field_names["name"]: name,
                self.field_names["feedback"]: feedback
            }

            response = requests.post(self.form_url, data=data)

            if response.status_code == 200:
                self.name_input.clear()
                self.feedback_text.clear()
                self.error_label.setVisible(False)
            else:
                self.error_label.setText(f"*Ошибка: {response.status_code}")
                self.error_label.setVisible(True)

        except Exception as e:
            self.error_label.setText(f"*Ошибка: {str(e)}")
            self.error_label.setVisible(True)

    def return_to_menu(self):
        self.return_to_menu_signal.emit()