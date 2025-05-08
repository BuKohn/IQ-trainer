import atexit
import os.path
import sys
from ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from core.flag_file import create_flag_file, remove_flag_file
from core.add_notification_task_to_scheduler import add_notification_task_to_scheduler

NOTIFICATION_SCRIPT_PATH = os.path.abspath("dist/notification_script/notification_script.exe")

if __name__ == "__main__":
    add_notification_task_to_scheduler(NOTIFICATION_SCRIPT_PATH)
    create_flag_file()
    atexit.register(remove_flag_file)
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())