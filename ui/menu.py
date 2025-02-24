import json

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (QLabel, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout,
                               QStackedWidget, QScrollArea)

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_question_index = 0
        self.score = 0
        self.questions_data = self.load_questions("assets/questions.json")
        self.user_answers = []
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
        self.resize(702, 383)
        self.setStyleSheet("""
        QMainWindow {
	        background-image: url(assets/back.jpg);
	        background-repeat: no-repeat;
            background-position: center;
            background-attachment: scroll;
            background-size: contain;
        }
        QLabel {
	        background-color: rgb(255, 253, 253);
	        border-radius: 5px;
	        border: 5px solid rgb(55, 107, 113);
        }
        QPushButton {
	        background-color: rgb(255, 253, 253);
	        border-radius: 5px;
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
        """)
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.menu_widget = QWidget()
        self.create_menu_page()
        self.stacked_widget.addWidget(self.menu_widget)

        self.quiz_widget = QWidget()
        self.create_quiz_page()
        self.stacked_widget.addWidget(self.quiz_widget)

        self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def create_menu_page(self):
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

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 100, 0, 0)
        verticalLayout = QVBoxLayout()
        verticalLayout.setContentsMargins(250, 0, 250, 0)
        menu_layout.addStretch()
        menu_layout.addLayout(title_container)
        menu_layout.addLayout(verticalLayout)
        menu_layout.addStretch()

        play_button = QPushButton("Играть")
        play_button.setEnabled(True)
        play_button.clicked.connect(self.start_quiz)
        verticalLayout.addWidget(play_button)

        settings_button = QPushButton("Настройки")
        settings_button.setEnabled(False)
        verticalLayout.addWidget(settings_button)

        exit_button = QPushButton("Выход")
        exit_button.setEnabled(True)
        verticalLayout.addWidget(exit_button)
        exit_button.clicked.connect(self.close)

        self.menu_widget.setLayout(menu_layout)

    def create_quiz_page(self):
        """Создает страницу IQ-теста."""
        self.quiz_layout = QVBoxLayout()
        self.quiz_widget.setLayout(self.quiz_layout)

    def start_quiz(self):
        """Начинает тест, показывая первый вопрос."""
        self.current_question_index = 0
        self.score = 0
        self.stacked_widget.setCurrentIndex(1)
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
        question_label.setPixmap(pixmap.scaled(622, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
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
        result = round(self.score / len(self.questions_data) * 150 + 20)
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
        self.stacked_widget.setCurrentIndex(0)