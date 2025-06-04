import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel, QListWidget, QAbstractItemView, QListWidgetItem, QHBoxLayout,
    QScrollArea, QSizePolicy
)
from core.clickable_button import ClickableButton
from ui.text import text

class CustomQuiz(QWidget):
    return_to_menu_signal = Signal()
    add_question_signal = Signal()
    FILE_PATH = "assets/custom_questions.json"

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.selected_questions = []
        self.custom_questions = []
        self.load_custom_questions()

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(10)

        self.container = QWidget()
        self.container.setFixedSize(900, 550)
        self.container.setStyleSheet(
            "background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
        self.main_layout.addWidget(self.container)

        # Создаем макет внутри контейнера
        self.layout_inside_container = QVBoxLayout(self.container)
        self.layout_inside_container.setAlignment(Qt.AlignTop)

        self.question_list = QListWidget()
        self.question_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.populate_questions()

        self.button_layout = QHBoxLayout()

        self.delete_question_button = ClickableButton(text[self.lang]["custom_quiz"]["del_qst_btn"])
        self.delete_question_button.clicked.connect(self.delete_selected_questions)

        self.add_question_button = ClickableButton(text[self.lang]["custom_quiz"]["add_qst_btn"])
        self.add_question_button.clicked.connect(self.add_question)

        self.start_quiz_button = ClickableButton(text[self.lang]["custom_quiz"]["start_quiz_btn"])
        self.start_quiz_button.clicked.connect(self.start_quiz)

        self.return_to_menu_button = ClickableButton(text[self.lang]["custom_quiz"]["return_btn"])
        self.return_to_menu_button.clicked.connect(self.return_to_menu)

        self.back_to_settings()

    def load_custom_questions(self):
        with open(self.FILE_PATH, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        if isinstance(data, dict):
            data = [data]

        self.custom_questions = data

    def back_to_settings(self):
        self.score = 0
        self.current_question_index = 0
        self.user_answers = []

        for i in reversed(range(self.layout_inside_container.count())):
            item = self.layout_inside_container.itemAt(i)
            if item:
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                elif item.layout():
                    layout = item.layout()
                    self.clear_layout(layout)
                    self.layout_inside_container.removeItem(item)

        self.title = QLabel(text[self.lang]["custom_quiz"]["title"])
        self.title.setFixedHeight(50)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
                                    QLabel {
                                        font-family: 'Arial'; 
                                        font-size: 24px;
                                        font-weight: bold;
                                        border-radius: 10px;
                                        padding: 5px;
                                        text-align: center;
                                    }
                                """)

        self.layout_inside_container.addWidget(self.title)

        self.layout_inside_container.addWidget(self.question_list)
        self.button_layout.addWidget(self.delete_question_button)
        self.button_layout.addWidget(self.add_question_button)
        self.layout_inside_container.addLayout(self.button_layout)
        self.layout_inside_container.addWidget(self.start_quiz_button)
        self.layout_inside_container.addWidget(self.return_to_menu_button)

    def populate_questions(self):
        """Заполняет список вопросов."""
        self.question_list.clear()
        questions_names = []
        for entry in self.custom_questions:
            questions_names.append(entry.get("title"))

        for question_name in questions_names:
            item = self.create_checkable_item(question_name)
            self.question_list.addItem(item)

    def create_checkable_item(self, text):
        """Создаёт элемент списка с чекбоксом."""
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Добавляем возможность выбора
        item.setCheckState(Qt.Unchecked)  # По умолчанию не выбран
        return item

    def delete_selected_questions(self):
        """Удаляет выбранные вопросы из QListWidget."""
        items_to_remove = []

        for i in range(self.question_list.count()):
            item = self.question_list.item(i)
            if item.checkState() == Qt.Checked:
                items_to_remove.append(item.text())

        for i in reversed(range(self.question_list.count())):
            item = self.question_list.item(i)
            if item.text() in items_to_remove:
                self.question_list.takeItem(i)

        self.custom_questions = [
            question for question in self.custom_questions
            if question.get("title") not in items_to_remove
        ]

        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(self.custom_questions, file, ensure_ascii=False, indent=4)

    def start_quiz(self):
        selected_question_names = []
        for i in range(self.question_list.count()):
            item = self.question_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_question_names.append(item.text())

        self.selected_questions = [
            question for question in self.custom_questions
            if question.get("title") in selected_question_names
        ]

        if len(self.selected_questions) > 0:
            self.show_question()

    def show_question(self):
        for i in reversed(range(self.layout_inside_container.count())):
            item = self.layout_inside_container.itemAt(i)
            if item:
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                elif item.layout():
                    layout = item.layout()
                    self.clear_layout(layout)
                    self.layout_inside_container.removeItem(item)

        if self.current_question_index >= len(self.selected_questions):
            self.show_results()
            return

        question_data = self.selected_questions[self.current_question_index]

        question_label = QLabel(question_data["question_text"])
        question_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        question_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial'; 
                font-size: 24px;
                font-weight: bold;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
            }
        """)
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_inside_container.addWidget(question_label)

        for option in question_data["answers"]:
            button = ClickableButton(option)
            button.setMinimumHeight(40)
            button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
            self.layout_inside_container.addWidget(button)

    def check_answer(self, selected_option):
        question_data = self.selected_questions[self.current_question_index]
        if selected_option == question_data["correct_answer"]:
            self.score += 1

        self.user_answers.append({
            "question": question_data["question_text"],
            "selected_answer": selected_option,
            "correct_answer": question_data["correct_answer"],
            "is_correct": selected_option == question_data["correct_answer"]
        })

        self.current_question_index += 1
        self.show_question()

    def show_results(self):
        for i in reversed(range(self.layout_inside_container.count())):
            widget = self.layout_inside_container.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Создаем контейнер для результатов
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        results_container = QWidget()
        results_layout = QVBoxLayout(results_container)

        # Показываем общий результат
        self.result_label = QLabel(text[self.lang]["custom_quiz"]["res_lbl"].format(score=self.score,
                                                                               selected_questions=len(self.selected_questions)))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.result_label.font()
        font.setPointSize(20)
        self.result_label.setFont(font)
        results_layout.addWidget(self.result_label)

        for answer in self.user_answers:
            answer_container = QWidget()
            answer_container.setFixedSize(840, 500)
            answer_container.setStyleSheet(
                "background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
            answer_layout = QVBoxLayout(answer_container)
            answer_layout.setContentsMargins(20, 20, 20, 20)
            answer_layout.setSpacing(15)

            self.question_label = QLabel(text[self.lang]["custom_quiz"]["qst_lbl"])
            self.question_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.question_label.setStyleSheet("border: none; background-color: transparent;")
            answer_layout.addWidget(self.question_label)

            # Отображаем изображение вопроса
            question = QLabel(answer["question"])
            answer_layout.addWidget(question)

            # Отображаем выбранный ответ
            self.selected_answer_label = QLabel(text[self.lang]["custom_quiz"]["sel_ans_lbl"])
            self.selected_answer_label.setStyleSheet("border: none; background-color: transparent;")
            selected_answer = QLabel(answer["selected_answer"])
            answer_layout.addWidget(self.selected_answer_label)
            answer_layout.addWidget(selected_answer)

            # Отображаем правильный ответ
            self.correct_answer_label = QLabel(text[self.lang]["custom_quiz"]["cor_ans_lbl"])
            self.correct_answer_label.setStyleSheet("border: none; background-color: transparent;")
            correct_answer = QLabel(answer["correct_answer"])
            answer_layout.addWidget(self.correct_answer_label)
            answer_layout.addWidget(correct_answer)

            # Отображаем статус ответа
            self.status_label = QLabel(text[self.lang]["custom_quiz"]["status_lbl"])
            self.status_label.setStyleSheet("border: none; background-color: transparent;")
            status = QLabel(text[self.lang]["custom_quiz"]["correct"] if answer["is_correct"] else text[self.lang]["custom_quiz"]["wrong"])
            status.setStyleSheet("color: green;" if answer["is_correct"] else "color: red;")
            answer_layout.addWidget(self.status_label)
            answer_layout.addWidget(status)

            results_layout.addWidget(answer_container)

        self.back_button = ClickableButton(text[self.lang]["custom_quiz"]["back_btn"])
        self.back_button.clicked.connect(self.back_to_settings)
        results_layout.addWidget(self.back_button)

        scroll_area.setWidget(results_container)

        self.layout_inside_container.addWidget(scroll_area)

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

    def apply_language(self, lang):
        self.lang = lang
        self.delete_question_button.setText(text[self.lang]["custom_quiz"]["del_qst_btn"])
        self.add_question_button.setText(text[self.lang]["custom_quiz"]["add_qst_btn"])
        self.start_quiz_button.setText(text[self.lang]["custom_quiz"]["start_quiz_btn"])
        self.return_to_menu_button.setText(text[self.lang]["custom_quiz"]["return_btn"])
        self.title.setText(text[self.lang]["custom_quiz"]["title"])

    def return_to_menu(self):
        self.return_to_menu_signal.emit()

    def add_question(self):
        self.add_question_signal.emit()