import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea


class Quiz(QWidget):
    return_to_menu_signal = Signal()

    def __init__(self):
        super().__init__()
        self.score = 0
        self.current_question_index = 0
        self.user_answers = []
        self.questions_data = self.load_questions("assets/questions.json")
        self.setup_ui()

    def load_questions(self, file_path):
        """Загружает вопросы из JSON-файла."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка при чтении JSON из файла {file_path}.")
            return []

    def setup_ui(self):
        self.quiz_layout = QVBoxLayout()
        self.setLayout(self.quiz_layout)
        self.show_question()

    def show_question(self):
        """Показывает текущий вопрос."""
        for i in reversed(range(self.quiz_layout.count())):
            widget = self.quiz_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if self.current_question_index >= len(self.questions_data):
            self.show_results()
            return

        question_data = self.questions_data[self.current_question_index]

        question_label = QLabel()
        question_label.setObjectName("question_label")
        pixmap = QPixmap(question_data["question_image"])
        question_label.setPixmap(
            pixmap.scaled(622, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quiz_layout.addWidget(question_label)

        for option in question_data["options"]:
            button = QPushButton(option)
            button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
            self.quiz_layout.addWidget(button)

    def check_answer(self, selected_option):
        """Проверяет ответ пользователя."""
        question_data = self.questions_data[self.current_question_index]
        if selected_option == question_data["correct_answer"]:
            self.score += 1

        # Сохраняем ответ пользователя
        self.user_answers.append({
            "question_image": question_data["question_image"],
            "selected_answer": selected_option,
            "correct_answer": question_data["correct_answer"],
            "is_correct": selected_option == question_data["correct_answer"]
        })

        # Увеличиваем счетчик правильных ответов
        if selected_option == question_data["correct_answer"]:
            self.score += 1

        self.current_question_index += 1
        self.show_question()

    def show_results(self):
        """Показывает результаты теста."""
        # Очищаем предыдущие виджеты
        for i in reversed(range(self.quiz_layout.count())):
            widget = self.quiz_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Создаем контейнер для результатов
        results_container = QWidget()  # Это наш контейнер
        results_layout = QVBoxLayout(results_container)  # Макет для контейнера

        # Показываем общий результат
        result = round(self.score / len(self.questions_data) * 100 + 20)
        result_label = QLabel(f"Тест завершен!\nВаш результат: {result} IQ")
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = result_label.font()
        font.setPointSize(20)
        result_label.setFont(font)
        results_layout.addWidget(result_label)

        # Показываем детализацию по каждому вопросу
        for answer in self.user_answers:
            question_label = QLabel("Вопрос:")
            question_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            question_label.setStyleSheet("border: none; background-color: transparent;")
            results_layout.addWidget(question_label)

            # Отображаем изображение вопроса
            question_image = QLabel()
            question_image.setStyleSheet("border: none; background-color: transparent;")
            pixmap = QPixmap(answer["question_image"])
            scaled_pixmap = pixmap.scaled(
                300, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            question_image.setPixmap(scaled_pixmap)
            results_layout.addWidget(question_image)

            # Отображаем выбранный ответ
            selected_answer_label = QLabel(f"Ваш ответ:")
            selected_answer_label.setStyleSheet("border: none; background-color: transparent;")
            selected_answer = QLabel(answer["selected_answer"])
            results_layout.addWidget(selected_answer_label)
            results_layout.addWidget(selected_answer)

            # Отображаем правильный ответ
            correct_answer_label = QLabel(f"Правильный ответ:")
            correct_answer_label.setStyleSheet("border: none; background-color: transparent;")
            correct_answer = QLabel(answer["correct_answer"])
            results_layout.addWidget(correct_answer_label)
            results_layout.addWidget(correct_answer)

            # Отображаем статус ответа
            status_label = QLabel("Результат:")
            status_label.setStyleSheet("border: none; background-color: transparent;")
            status = QLabel("Правильно" if answer["is_correct"] else "Неправильно")
            status.setStyleSheet("color: green;" if answer["is_correct"] else "color: red;")
            results_layout.addWidget(status_label)
            results_layout.addWidget(status)

            # Разделитель
            separator = QLabel("-" * 250)
            separator.setStyleSheet("border: none; background-color: transparent;")
            results_layout.addWidget(separator)

        # Кнопка для возврата в главное меню
        back_button = QPushButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)
        results_layout.addWidget(back_button)

        # Добавляем контейнер с результатами в QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Разрешаем изменение размера содержимого
        scroll_area.setWidget(results_container)  # Устанавливаем контейнер как содержимое прокручиваемой области

        # Добавляем QScrollArea на страницу
        self.quiz_layout.addWidget(scroll_area)

    def return_to_menu(self):
        self.return_to_menu_signal.emit()