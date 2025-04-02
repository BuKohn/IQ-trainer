import json
import random

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSlider, QHBoxLayout


class Quiz(QWidget):
    return_to_menu_signal = Signal()
    update_score_and_achievements_signal = Signal(int, list)

    def __init__(self, user_achievements):
        super().__init__()
        self.user_achievements = user_achievements
        self.score = 0
        self.current_question_index = 0
        self.user_answers = []
        self.all_questions = self.load_questions("assets/questions.json")
        self.questions_data = []
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

    def select_random_questions(self, questions, difficulty_values, count):
        """Выбирает случайные вопросы"""
        # Фильтруем вопросы по заданным значениям difficulty
        filtered_questions = [q for q in questions if q["difficulty"] in difficulty_values]
        remaining_questions = [q for q in questions if q not in filtered_questions]

        # Выбираем вопросы из отфильтрованного списка
        selected_questions = random.sample(filtered_questions, min(len(filtered_questions), count))

        # Если вопросов недостаточно, дополняем из оставшихся
        if len(selected_questions) < count:
            additional_count = count - len(selected_questions)
            additional_questions = random.sample(remaining_questions, min(len(remaining_questions), additional_count))
            selected_questions.extend(additional_questions)

        # Перемешиваем итоговый список для случайного порядка
        random.shuffle(selected_questions)

        return selected_questions

    def setup_ui(self):
        self.quiz_layout = QVBoxLayout()
        self.setLayout(self.quiz_layout)

        title = QLabel("Настройка теста")
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

        self.quiz_layout.addWidget(title)

        self.qnumber_label = QLabel("Количество вопросов: 10")
        self.qnumber_label.setAlignment(Qt.AlignCenter)
        self.qnumber_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.quiz_layout.addWidget(self.qnumber_label)

        # Ползунок
        self.qnumber_slider = QSlider(Qt.Horizontal)
        self.qnumber_slider.setMinimum(5)
        self.qnumber_slider.setMaximum(20)
        self.qnumber_slider.setValue(10)
        self.qnumber_slider.setTickPosition(QSlider.TicksBelow)
        self.qnumber_slider.setTickInterval(10)
        self.quiz_layout.addWidget(self.qnumber_slider)

        self.difficulty_label = QLabel("Сложность: Нормально")
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.difficulty_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.quiz_layout.addWidget(self.difficulty_label)

        # Ползунок
        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(0)
        self.difficulty_slider.setMaximum(2)
        self.difficulty_slider.setValue(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)
        self.difficulty_slider.setTickInterval(10)
        self.quiz_layout.addWidget(self.difficulty_slider)

        # Подключение сигнала valueChanged к обработчику
        self.qnumber_slider.valueChanged.connect(self.update_qnumber_label)
        self.difficulty_slider.valueChanged.connect(self.update_difficulty_label)

        button_layout = QHBoxLayout()
        back_button = QPushButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)
        button_layout.addWidget(back_button)

        start_button = QPushButton("Начать тест")
        start_button.clicked.connect(self.start_quiz)
        button_layout.addWidget(start_button)

        self.quiz_layout.addLayout(button_layout)

    def update_qnumber_label(self, value):
        """Обновляет метку с текущим значением ползунка количества вопросов."""
        self.qnumber_label.setText(f"Количество вопросов: {value}")

    def update_difficulty_label(self, value):
        """Обновляет метку с текущим значением ползунка сложности теста."""
        difficulties = {0: "Легко", 1: "Нормально", 2: "Сложно"}
        self.difficulty_label.setText(f"Сложность: {difficulties[value]}")

    def start_quiz(self):
        values_for_difficulties = {0: [1, 2], 1: [2, 3], 2: [3, 4]}
        selected_qnumber = self.qnumber_slider.value()
        self.selected_difficulty = self.difficulty_slider.value()
        self.questions_data = self.select_random_questions(self.all_questions,
                                                           values_for_difficulties[self.selected_difficulty],
                                                           selected_qnumber)
        self.show_question()

    def show_question(self):
        """Показывает текущий вопрос."""
        for i in reversed(range(self.quiz_layout.count())):
            item = self.quiz_layout.itemAt(i)
            if item:
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                elif item.layout():
                    layout = item.layout()
                    self.clear_layout(layout)
                    self.quiz_layout.removeItem(item)

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
            button.setMinimumHeight(40)
            button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
            self.quiz_layout.addWidget(button)

    def check_answer(self, selected_option):
        """Проверяет ответ пользователя."""
        question_data = self.questions_data[self.current_question_index]
        if selected_option == question_data["correct_answer"]:
            self.score += question_data["difficulty"] * 10

        # Сохраняем ответ пользователя
        self.user_answers.append({
            "question_image": question_data["question_image"],
            "selected_answer": selected_option,
            "correct_answer": question_data["correct_answer"],
            "is_correct": selected_option == question_data["correct_answer"]
        })

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
        difficulty_sum = sum([self.questions_data[i]["difficulty"] for i in range(len(self.questions_data))])
        result = round(self.score / difficulty_sum * 10 + 20)
        result_label = QLabel(f"Тест завершен!\nВаш результат: {result} IQ")
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = result_label.font()
        font.setPointSize(20)
        result_label.setFont(font)
        results_layout.addWidget(result_label)

        achievements = []
        if result == 20 and self.selected_difficulty == 0 and "Одарённый, но наоборот" not in self.user_achievements:
            achievements.append("Одарённый, но наоборот")
        if result == 120 and self.selected_difficulty == 2 and "Гений" not in self.user_achievements:
            achievements.append("Гений")
        if (90 < result < 110 and (self.selected_difficulty == 1 or self.selected_difficulty == 2)
                and "Середняк" not in self.user_achievements):
            achievements.append("Середняк")

        for achievement in achievements:
            achievement_label = QLabel(f"Получено достижение: {achievement}")
            achievement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            achievement_label.setStyleSheet("""QLabel {
                            border: 5px solid rgb(226, 231, 63);
                            font-family: 'Arial'; 
                            font-size: 20px;
                            font-weight: bold;
                        }
                        """)
            results_layout.addWidget(achievement_label)

        self.update_score_and_achievements(self.score, achievements)

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

    def update_score_and_achievements(self, score, achievements):
        self.update_score_and_achievements_signal.emit(score, achievements)

    def clear_layout(self, layout):
        """Рекурсивно очищает макет, удаляя все виджеты и вложенные макеты."""
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            if item:
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                elif item.layout():
                    self.clear_layout(item.layout())