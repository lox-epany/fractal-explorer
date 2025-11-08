from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter, QColor
from PyQt6.QtCore import Qt
import numpy as np


class Canvas(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.width = width
        self.height = height
        self.setMinimumSize(width, height)

        # Создаём пустое изображение формата RGB32
        self.image = QImage(self.width, self.height, QImage.Format.Format_RGB32)
        self.image.fill(QColor(127, 127, 127))  # Черный фон

        # Создаём палитру цветов для отображения фрактала
        self.colormap = self._create_colormap()

    @staticmethod
    def _create_colormap():
        """Создаёт цветовую палитру с плавным градиентом"""
        colors = []
        for i in range(256):
            if i < 64:
                r, g, b = 0, 0, i * 4
            elif i < 128:
                r, g, b = 0, (i - 64) * 4, 255
            elif i < 192:
                r, g, b = (i - 128) * 4, 255, 255
            else:
                r, g, b = 255, 255, 255
            colors.append((r, g, b))
        return colors

    def _iterations_to_color(self, iterations):
        """Преобразует количество итераций в RGB цвет по палитре"""
        if iterations < 0:
            return 0, 0, 0  # Чёрный, если вне множества
        return self.colormap[iterations % 256]

    def update_stripe(self, pixels, y_start, y_end):
        """
        Обновляет изображение полосой пикселей.
        pixels — numpy-массив формы (y_end - y_start, width),
        содержащий количество итераций для каждого пикселя.
        """
        height = y_end - y_start
        width = pixels.shape[1]

        for y in range(height):
            for x in range(width):
                color = self._iterations_to_color(pixels[y, x])
                self.image.setPixel(x, y_start + y, self._qRgb(*color))

        self.update()  # Запрашиваем перерисовку

    def update_preview(self, pixels):
        """
        Обновляет изображение целиком (например, превью маленького разрешения).
        pixels — numpy-массив формы (height, width).
        """
        height, width = pixels.shape
        for y in range(height):
            for x in range(width):
                color = self._iterations_to_color(pixels[y, x])
                self.image.setPixel(x, y, self._qRgb(*color))
        self.update()

    def clear(self):
        self.image.fill(QColor(127, 127, 127))
        self.update()

    def paintEvent(self, event):
        """Отрисовка """
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    @staticmethod
    def _rgb(r, g, b):
        """Преобразует RGB к формату QColor.rgb"""
        from PyQt6.QtGui import QColor
        return QColor(r, g, b).rgb()
