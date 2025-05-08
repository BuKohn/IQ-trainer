from PySide6.QtCore import Qt, Signal, QStringListModel, QRect
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QListView

from core.clickable_button import ClickableButton


class Notes(QWidget):
    return_to_menu_signal = Signal(list)

    def __init__(self, useful_links):
        super().__init__()
        self.useful_links = useful_links
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(10)

        container = QWidget()
        container.setFixedSize(900, 500)  # Фиксированный размер контейнера
        container.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid rgb(55, 107, 113);")
        self.main_layout.addWidget(container)

        # Создаем макет внутри контейнера
        layout_inside_container = QVBoxLayout(container)
        layout_inside_container.setAlignment(Qt.AlignTop)
        layout_inside_container.setContentsMargins(20, 20, 20, 20)  # Внутренние отступы

        title = QLabel("Полезные сайты")
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

        # QListView для отображения списка
        self.model = QStringListModel()
        self.model.setStringList(self.useful_links)

        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setStyleSheet("""
            QListView::item {
                min-height: 40px;
                color: rgb(55, 107, 113);
            }
        """)
        layout_inside_container.addWidget(self.list_view)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_button = ClickableButton("+ Добавить сайт")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.remove_button = ClickableButton("- Удалить сайт")
        self.remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_button)

        layout_inside_container.addLayout(button_layout)

        # Кнопка возврата в меню
        self.return_to_menu_button = ClickableButton("Вернуться в меню")
        self.return_to_menu_button.clicked.connect(self.return_to_menu)
        layout_inside_container.addWidget(self.return_to_menu_button)

    def add_item(self):
        """Добавляет новый элемент в список."""
        current_list = self.model.stringList()
        current_list.append("Добавьте запись")
        self.model.setStringList(current_list)

    def remove_item(self):
        """Удаляет выделенный элемент из списка."""
        index = self.list_view.currentIndex()
        if not index.isValid():
            return

        # Получаем текущий список строк
        current_list = self.model.stringList()

        # Удаляем элемент по индексу
        del current_list[index.row()]

        # Обновляем модель
        self.model.setStringList(current_list)

    def return_to_menu(self):
        self.useful_links = self.model.stringList()
        self.return_to_menu_signal.emit(self.useful_links)