import pygame
from PySide6.QtWidgets import QPushButton


class ClickableButton(QPushButton):
    """Класс кнопки с автоматическим воспроизведением звука."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("assets/button_press.wav")
        self.click_sound.set_volume(0.1)

    def mousePressEvent(self, event):
        """Переопределённый метод для обработки нажатия."""
        self.click_sound.play()
        super().mousePressEvent(event)