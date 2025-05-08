from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel
)
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.clickable_button import ClickableButton

class Statistics(QWidget):
    return_to_menu_signal = Signal()

    def __init__(self, tests_scores):
        super().__init__()
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

        title = QLabel("Статистика")
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

        self.layout_inside_container.addWidget(title)

        figure = Figure(facecolor="white")
        self.canvas = FigureCanvas(figure)
        self.layout_inside_container.addWidget(self.canvas)
        self.ax = figure.add_subplot(111)

        x = range(1, len(self.tests_scores) + 1)
        y = self.tests_scores
        self.ax.bar(x, y, color="blue")
        self.ax.set_title("Результаты тестов")
        self.ax.set_xlabel("Номер теста")
        self.ax.set_ylabel("Очки")
        self.ax.set_xticks(range(1, len(self.tests_scores) + 1))

        self.canvas.draw()

        self.return_to_menu_button = ClickableButton("Вернуться в меню")
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        self.layout_inside_container.addWidget(self.return_to_menu_button)

    def update_bar_chart(self, tests_scores):
        self.ax.clear()
        x = range(1, len(tests_scores) + 1)
        y = tests_scores
        self.ax.bar(x, y, color='blue')
        self.ax.set_title("Результаты тестов")
        self.ax.set_xlabel("Номер теста")
        self.ax.set_ylabel("Очки")
        self.ax.set_xticks(range(1, len(self.tests_scores) + 1))

        self.canvas.draw()

    def return_to_menu(self):
        self.return_to_menu_signal.emit()