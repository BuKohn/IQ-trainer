import winreg


def add_notification_task_to_scheduler(executable_path):
    """Добавляет исполняемый файл в папку автозагрузки."""
    """
        Добавляет исполняемый файл в автозагрузку через реестр.
        :param executable_path: Абсолютный путь к исполняемому файлу.
        """
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, "MyAppName", 0, winreg.REG_SZ, f'"{executable_path}"')
    winreg.CloseKey(key)