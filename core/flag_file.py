import os

FLAG_FILE = "dist/notification_script/app_running.flag"

def create_flag_file():
    """Создаёт файл-флаг."""
    with open(FLAG_FILE, "w") as f:
        f.write("running")

def remove_flag_file():
    """Удаляет файл-флаг."""
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)