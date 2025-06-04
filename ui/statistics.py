from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel
)
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from core.clickable_button import ClickableButton
from ui.text import text

class Statistics(QWidget):
    return_to_menu_signal = Signal()

    def __init__(self, tests_scores, lang):
        super().__init__()
        self.lang = lang
        self.tests_scores = tests_scores
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
        self.layout_inside_container = QVBoxLayout(container)
        self.layout_inside_container.setAlignment(Qt.AlignTop) # Внутренние отступы

        self.title = QLabel(text[self.lang]["stats"]["title"])
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

        figure = Figure(facecolor="white")
        self.canvas = FigureCanvas(figure)
        self.layout_inside_container.addWidget(self.canvas)
        self.ax = figure.add_subplot(111)

        x = range(1, len(self.tests_scores) + 1)
        y = self.tests_scores
        self.ax.bar(x, y, color="blue")
        self.ax.set_title(text[self.lang]["stats"]["ax_title"])
        self.ax.set_xlabel(text[self.lang]["stats"]["ax_x_lbl"])
        self.ax.set_ylabel(text[self.lang]["stats"]["ax_y_lbl"])
        self.ax.set_xticks(range(1, len(self.tests_scores) + 1))

        self.canvas.draw()

        self.return_to_menu_button = ClickableButton(text[self.lang]["stats"]["back_btn"])
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        self.layout_inside_container.addWidget(self.return_to_menu_button)

    def update_bar_chart(self, tests_scores):
        self.ax.clear()
        x = range(1, len(tests_scores) + 1)
        y = tests_scores
        self.ax.bar(x, y, color='blue')
        self.ax.set_title(text[self.lang]["stats"]["ax_title"])
        self.ax.set_xlabel(text[self.lang]["stats"]["ax_x_lbl"])
        self.ax.set_ylabel(text[self.lang]["stats"]["ax_y_lbl"])
        self.ax.set_xticks(range(1, len(self.tests_scores) + 1))

        self.canvas.draw()

    def apply_language(self, lang):
        self.lang = lang
        self.title.setText(text[self.lang]["stats"]["title"])
        self.ax.set_title(text[self.lang]["stats"]["ax_title"])
        self.ax.set_xlabel(text[self.lang]["stats"]["ax_x_lbl"])
        self.ax.set_ylabel(text[self.lang]["stats"]["ax_y_lbl"])
        self.canvas.draw()
        self.return_to_menu_button.setText(text[self.lang]["stats"]["back_btn"])

    def return_to_menu(self):
        self.return_to_menu_signal.emit()