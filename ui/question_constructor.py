import json
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel, QListWidget, QAbstractItemView, QListWidgetItem, QHBoxLayout
)
from core.clickable_button import ClickableButton
from ui.text import text

class QuestionConstructor(QWidget):
    return_to_custom_quiz_signal = Signal()
    FILE_PATH = "assets/custom_questions.json"

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setup_ui()
        self.custom_questions = []
        self.load_custom_questions()

    def load_custom_questions(self):
        with open(self.FILE_PATH, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        if isinstance(data, dict):
            data = [data]

        self.custom_questions = data

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(10)

        container = QWidget()
        container.setFixedSize(900, 550)
        container.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
        self.main_layout.addWidget(container)

        # Создаем макет внутри контейнера
        self.layout_inside_container = QVBoxLayout(container)
        self.layout_inside_container.setAlignment(Qt.AlignTop)  # Внутренние отступы

        self.title = QLabel(text[self.lang]["qst_construct"]["title"])
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

        self.settings_layout = QVBoxLayout()

        # Поле для названия вопроса
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel(text[self.lang]["qst_construct"]["title_lbl"])
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(text[self.lang]["qst_construct"]["title_input"])
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.title_input)
        self.settings_layout.addLayout(self.title_layout)

        # Поле для сути вопроса
        self.question_layout = QVBoxLayout()
        self.question_label = QLabel(text[self.lang]["qst_construct"]["qst_lbl"])
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText(text[self.lang]["qst_construct"]["qst_input"])
        self.question_layout.addWidget(self.question_label)
        self.question_layout.addWidget(self.question_input)
        self.settings_layout.addLayout(self.question_layout)

        self.answers_layout = QVBoxLayout()
        self.answers_label = QLabel(text[self.lang]["qst_construct"]["answers_lbl"])
        self.answers_list = QListWidget()
        self.answers_list.setSpacing(10)
        self.answers_list.setSelectionMode(QAbstractItemView.NoSelection)

        for i in range(6):
            item = QListWidgetItem()
            widget = QLineEdit()
            widget.setMinimumHeight(40)
            widget.setPlaceholderText(text[self.lang]["qst_construct"]["answer_place"].format(i=i+1))
            self.answers_list.addItem(item)
            self.answers_list.setItemWidget(item, widget)

        self.answers_layout.addWidget(self.answers_label)
        self.answers_layout.addWidget(self.answers_list)
        self.settings_layout.addLayout(self.answers_layout)

        self.correct_answer_layout = QHBoxLayout()
        self.correct_answer_label = QLabel(text[self.lang]["qst_construct"]["cor_ans_lbl"])
        self.correct_answer_input = QLineEdit()
        self.correct_answer_input.setPlaceholderText(text[self.lang]["qst_construct"]["cor_ans_input"])
        self.correct_answer_layout.addWidget(self.correct_answer_label)
        self.correct_answer_layout.addWidget(self.correct_answer_input)
        self.settings_layout.addLayout(self.correct_answer_layout)

        self.save_button = ClickableButton(text[self.lang]["qst_construct"]["save_btn"])
        self.save_button.clicked.connect(self.save_question)
        self.settings_layout.addWidget(self.save_button)

        self.layout_inside_container.addLayout(self.settings_layout)

        self.return_to_custom_quiz_button = ClickableButton(text[self.lang]["qst_construct"]["return_btn"])
        self.return_to_custom_quiz_button.clicked.connect(self.return_to_custom_quiz)
        self.layout_inside_container.addWidget(self.return_to_custom_quiz_button)

        self.alert_label = QLabel("")
        self.alert_label.setStyleSheet("color: black; background-color: transparent; border: none;")
        self.alert_label.setVisible(False)
        self.layout_inside_container.addWidget(self.alert_label)

    def get_answers(self):
        answers = []
        for i in range(self.answers_list.count()):
            item = self.answers_list.item(i)
            widget = self.answers_list.itemWidget(item)
            if isinstance(widget, QLineEdit):
                answer = widget.text().strip()
                if answer:
                    answers.append(answer)
        return answers

    def clear_fields(self):
        self.title_input.clear()
        self.question_input.clear()
        self.correct_answer_input.clear()
        for i in range(self.answers_list.count()):
            item = self.answers_list.item(i)
            widget = self.answers_list.itemWidget(item)
            widget.clear()
        self.alert_label.setVisible(False)

    def save_question(self):
        """Сохраняет данные вопроса."""
        title = self.title_input.text().strip()
        question_text = self.question_input.toPlainText().strip()
        correct_answer = self.correct_answer_input.text().strip()
        answers = self.get_answers()

        if not title or not question_text or not answers or not correct_answer:
            self.alert_label.setVisible(True)
            self.alert_label.setText(text[self.lang]["qst_construct"]["err_empty"])
            return

        if len(answers) < 2:
            self.alert_label.setVisible(True)
            self.alert_label.setText(text[self.lang]["qst_construct"]["err_few_answers"])
            return

        if not correct_answer in answers:
            self.alert_label.setVisible(True)
            self.alert_label.setText(text[self.lang]["qst_construct"]["err_cor_answer"])
            return

        same_title = False
        for entry in self.custom_questions:
            question_title = entry.get("title")
            if title == question_title:
                same_title = True
                break

        if same_title:
            self.alert_label.setVisible(True)
            self.alert_label.setText(text[self.lang]["qst_construct"]["err_unique"])
            return


        self.alert_label.setVisible(True)
        self.alert_label.setText(text[self.lang]["qst_construct"]["success"])

        question_data = {
            "title": title,
            "question_text": question_text,
            "answers": answers,
            "correct_answer": correct_answer
        }

        self.custom_questions.append(question_data)

        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(self.custom_questions, file, ensure_ascii=False, indent=4)

    def apply_language(self, lang):
        self.lang = lang

        self.title.setText(text[self.lang]["qst_construct"]["title"])
        self.title_label.setText(text[self.lang]["qst_construct"]["title_lbl"])
        self.title_input.setPlaceholderText(text[self.lang]["qst_construct"]["title_input"])
        self.question_label.setText(text[self.lang]["qst_construct"]["qst_lbl"])
        self.question_input.setPlaceholderText(text[self.lang]["qst_construct"]["qst_input"])
        self.answers_label.setText(text[self.lang]["qst_construct"]["answers_lbl"])
        for i in range(self.answers_list.count()):
            item = self.answers_list.item(i)
            widget = self.answers_list.itemWidget(item)
            if isinstance(widget, QLineEdit):
                widget.setPlaceholderText(text[self.lang]["qst_construct"]["answer_place"].format(i=i + 1))

        self.correct_answer_label.setText(text[self.lang]["qst_construct"]["cor_ans_lbl"])
        self.correct_answer_input.setPlaceholderText(text[self.lang]["qst_construct"]["cor_ans_input"])

        self.save_button.setText(text[self.lang]["qst_construct"]["save_btn"])
        self.return_to_custom_quiz_button.setText(text[self.lang]["qst_construct"]["return_btn"])

        if self.alert_label.text():
            error_key = None
            for key, value in text[self.lang]["qst_construct"].items():
                if value == self.alert_label.text():
                    error_key = key
                    break
            if error_key:
                self.alert_label.setText(text[self.lang]["qst_construct"][error_key])

    def return_to_custom_quiz(self):
        self.return_to_custom_quiz_signal.emit()