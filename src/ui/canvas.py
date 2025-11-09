from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter, QColor
from PyQt6.QtCore import Qt
import numpy as np


class Canvas(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.setMinimumSize(400, 300)  # Минимальный размер, но не фиксированный
        self.image = None  # Будем создавать при первом вычислении
        self.colormap = self._create_colormap()

    def set_fractal_data(self, fractal_data):
        """Устанавливает данные фрактала и создаёт изображение нужного размера"""
        height, width = fractal_data.shape

        # Создаём изображение правильного размера
        self.image = QImage(width, height, QImage.Format.Format_RGB32)

        # Заполняем фракталом
        for y in range(height):
            for x in range(width):
                color = self._iterations_to_color(fractal_data[y, x])
                self.image.setPixel(x, y, self._qRgb(*color))

        # Обновляем отображение
        self.update()
        self.setMinimumSize(width, height)  # Подстраиваем минимальный размер

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
        print("iter")
        if iterations < 0:
            return 127, 127, 127  # Чёрный, если вне множества
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

    # def update_preview(self, pixels):
    #     """
    #     Обновляет изображение целиком (например, превью маленького разрешения).
    #     pixels — numpy-массив формы (height, width).
    #     """
    #     print(1)
    #     height, width = pixels.shape
    #     print(2)
    #     for y in range(height):
    #         for x in range(width):
    #             color = self._iterations_to_color(pixels[y, x])
    #             print(color)
    #             self.image.setPixel(x, y, self._rgb(*color))
    #     self.update()
    #
    # def clear(self):
    #     self.image.fill(QColor(127, 127, 127))
    #     self.update()

    def paintEvent(self, event):
        if self.image:
            painter = QPainter(self)
            # Масштабируем изображение под текущий размер виджета
            painter.drawImage(self.rect(), self.image)

    def _qRgb(self, r, g, b):
        """Вспомогательный метод для создания QRgb"""
        return (r << 16) | (g << 8) | b
