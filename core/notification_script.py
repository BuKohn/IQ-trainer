import os
from plyer import notification
import time

FLAG_FILE = "app_running.flag"

while True:
    if not os.path.exists(FLAG_FILE):
        time.sleep(10)
        notification.notify(
            title="IQ тренер",
            message="IQ тесты ждут вашего прохождения!",
            app_name="IQ trainer",
            timeout=10
        )
        time.sleep(10790)