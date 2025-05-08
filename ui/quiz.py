import json
import os
import random
import webbrowser
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSlider, QHBoxLayout
from core.clickable_button import ClickableButton


class Quiz(QWidget):
    return_to_menu_signal = Signal()
    update_score_and_achievements_signal = Signal(int, list)

    def __init__(self, username, user_achievements):
        super().__init__()
        self.username = username
        self.user_achievements = user_achievements
        self.score = 0
        self.current_question_index = 0
        self.user_answers = []
        self.all_questions = self.load_questions("assets/questions.json")
        self.values_for_difficulties = {0: [1, 2], 1: [2, 3], 2: [3, 4]}
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

    def save_progress(self, username, questions_data, difficulty, score, current_question_index, user_answers):
        """Сохраняет прогресс пользователя в JSON-файл."""
        file_path = "core/test_progress.json"
        progress_data = {
            "username": username,
            "questions_data" : questions_data,
            "difficulty": difficulty,
            "score": score,
            "current_question_index": current_question_index,
            "user_answers": user_answers
        }

        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

        if isinstance(data, dict):
            data = [data]

        user_found = False
        for entry in data:
            if entry.get("username") == username:
                entry.update(progress_data)
                user_found = True
                break

        if not user_found:
            data.append(progress_data)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def remove_progress(self, username):
        """Удаляет запись для указанного пользователя из JSON-файла."""
        file_path = "core/test_progress.json"
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        if isinstance(data, dict):
            data = [data]

        data = [entry for entry in data if entry.get("username") != username]

        with open(file_path, "w", encoding="utf-8") as file:
            if len(data) == 1:
                json.dump(data[0], file, ensure_ascii=False, indent=4)
            else:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def load_progress(self):
        file_path = "core/test_progress.json"
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        if isinstance(data, dict):
            data = [data]

        for entry in data:
            if entry.get("username") == self.username:
                self.questions_data = entry.get("questions_data")
                self.selected_difficulty = entry.get("difficulty")
                self.score = entry.get("score")
                self.current_question_index = entry.get("current_question_index")
                self.user_answers = entry.get("user_answers")
                self.show_question()

    def select_random_questions(self, questions, difficulty_values, count):
        """Выбирает случайные вопросы"""
        filtered_questions = [q for q in questions if q["difficulty"] in difficulty_values]
        remaining_questions = [q for q in questions if q not in filtered_questions]

        selected_questions = random.sample(filtered_questions, min(len(filtered_questions), count))

        if len(selected_questions) < count:
            additional_count = count - len(selected_questions)
            additional_questions = random.sample(remaining_questions, min(len(remaining_questions), additional_count))
            selected_questions.extend(additional_questions)

        random.shuffle(selected_questions)

        return selected_questions

    def setup_ui(self):
        self.quiz_layout = QVBoxLayout()
        self.quiz_layout.setContentsMargins(100, 0, 100, 0)
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

        special_tests_label = QLabel("Специальные тесты")
        special_tests_label.setAlignment(Qt.AlignCenter)
        special_tests_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.quiz_layout.addWidget(special_tests_label)

        numeric_button = ClickableButton("Числовое безумие")
        numeric_button.clicked.connect(lambda: self.start_special_quiz("assets/numeric_questions.json"))
        self.quiz_layout.addWidget(numeric_button)

        verbal_button = ClickableButton("Словесное испытание")
        verbal_button.clicked.connect(lambda: self.start_special_quiz("assets/verbal_questions.json"))
        self.quiz_layout.addWidget(verbal_button)

        logic_button = ClickableButton("Логический шторм")
        logic_button.clicked.connect(lambda: self.start_special_quiz("assets/logic_questions.json"))
        self.quiz_layout.addWidget(logic_button)

        button_layout = QHBoxLayout()
        back_button = ClickableButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)
        button_layout.addWidget(back_button)

        start_button = ClickableButton("Начать тест")
        start_button.clicked.connect(self.start_quiz)
        button_layout.addWidget(start_button)

        self.hint_button = ClickableButton(self)
        self.hint_button.setGeometry(10, 10, 50, 50)
        self.hint_button.setIcon(QIcon("assets/hint_icon.png"))
        self.hint_button.setIconSize(self.hint_button.sizeHint())
        self.hint_button.setVisible(False)

        self.quiz_layout.addLayout(button_layout)

        self.load_progress()

    def update_qnumber_label(self, value):
        """Обновляет метку с текущим значением ползунка количества вопросов."""
        self.qnumber_label.setText(f"Количество вопросов: {value}")

    def update_difficulty_label(self, value):
        """Обновляет метку с текущим значением ползунка сложности теста."""
        difficulties = {0: "Легко", 1: "Нормально", 2: "Сложно"}
        self.difficulty_label.setText(f"Сложность: {difficulties[value]}")

    def start_quiz(self):
        selected_qnumber = self.qnumber_slider.value()
        self.selected_difficulty = self.difficulty_slider.value()
        self.questions_data = self.select_random_questions(self.all_questions,
                                                           self.values_for_difficulties[self.selected_difficulty],
                                                           selected_qnumber)
        self.show_question()

    def start_special_quiz(self, questions_file):
        self.selected_difficulty = random.randint(0, 2)
        all_questions = self.load_questions(questions_file)
        self.questions_data = self.select_random_questions(all_questions,
                                                           self.values_for_difficulties[self.selected_difficulty],
                                                           10)
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

        self.hint_button.setVisible(False)

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
            button = ClickableButton(option)
            button.setMinimumHeight(40)
            button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
            self.quiz_layout.addWidget(button)

        if question_data["difficulty"] == 4:
            self.hint_button.setVisible(True)
            self.hint_button.setToolTip(question_data["hint"])

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
        self.save_progress(self.username, self.questions_data, self.selected_difficulty, self.score,
                           self.current_question_index, self.user_answers)
        self.show_question()

    def show_results(self):
        """Показывает результаты теста."""
        self.remove_progress(self.username)

        for i in reversed(range(self.quiz_layout.count())):
            widget = self.quiz_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.hint_button.setVisible(False)

        # Создаем контейнер для результатов
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
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

        for answer in self.user_answers:
            answer_container = QWidget()
            answer_container.setFixedSize(1050, 500)
            answer_container.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
            answer_layout = QVBoxLayout(answer_container)
            answer_layout.setContentsMargins(20, 20, 20, 20)
            answer_layout.setSpacing(15)

            question_label = QLabel("Вопрос:")
            question_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            question_label.setStyleSheet("border: none; background-color: transparent;")
            answer_layout.addWidget(question_label)

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
            answer_layout.addWidget(question_image)

            # Отображаем выбранный ответ
            selected_answer_label = QLabel(f"Ваш ответ:")
            selected_answer_label.setStyleSheet("border: none; background-color: transparent;")
            selected_answer = QLabel(answer["selected_answer"])
            answer_layout.addWidget(selected_answer_label)
            answer_layout.addWidget(selected_answer)

            # Отображаем правильный ответ
            correct_answer_label = QLabel(f"Правильный ответ:")
            correct_answer_label.setStyleSheet("border: none; background-color: transparent;")
            correct_answer = QLabel(answer["correct_answer"])
            answer_layout.addWidget(correct_answer_label)
            answer_layout.addWidget(correct_answer)

            # Отображаем статус ответа
            status_label = QLabel("Результат:")
            status_label.setStyleSheet("border: none; background-color: transparent;")
            status = QLabel("Правильно" if answer["is_correct"] else "Неправильно")
            status.setStyleSheet("color: green;" if answer["is_correct"] else "color: red;")
            answer_layout.addWidget(status_label)
            answer_layout.addWidget(status)

            results_layout.addWidget(answer_container)

        share_container = QWidget()
        share_container.setFixedSize(1050, 200)
        share_container.setStyleSheet(
            "background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
        share_layout = QVBoxLayout(share_container)
        share_layout.setContentsMargins(5, 5, 5, 5)
        share_layout.setSpacing(15)

        share_label = QLabel("Поделиться результатом")
        share_label.setFixedHeight(50)
        share_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        share_buttons_layout = QHBoxLayout()

        share_vk = ClickableButton("ВКонтакте")
        share_vk.clicked.connect(lambda: self.share_on_social_media("vk", result))
        share_buttons_layout.addWidget(share_vk)

        share_tg = ClickableButton("Телеграмм")
        share_tg.clicked.connect(lambda: self.share_on_social_media("telegram", result))
        share_buttons_layout.addWidget(share_tg)

        share_layout.addWidget(share_label)
        share_layout.addLayout(share_buttons_layout)
        results_layout.addWidget(share_container)

        results_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_button = ClickableButton("Вернуться в меню")
        back_button.clicked.connect(self.return_to_menu)
        results_layout.addWidget(back_button)

        scroll_area.setWidget(results_container)

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

    def share_on_social_media(self, platform, result):
        """Открывает окно публикации в выбранной социальной сети."""
        result_url = "https://github.com/BuKohn/IQ-trainer"
        if platform == "vk":
            share_url = f"https://vk.com/share.php?url={result_url}&title=Я+прошёл+тест+на+IQ+и+набрал+{result}+баллов"
        elif platform == "telegram":
            share_url = f"https://t.me/share/url?url={result_url}&text=Я+прошёл+тест+на+IQ+и+набрал+{result}+баллов"
        else:
            print("Неизвестная платформа")
            return

        webbrowser.open(share_url)