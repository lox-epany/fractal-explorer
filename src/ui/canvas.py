from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer
import numpy as np


class Canvas(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.image = None
        self.colormap = self._create_colormap()
        self.pending_update = False
        self.draw_timer = QTimer()
        self.draw_timer.timeout.connect(self._deferred_update)
        self.draw_timer.setSingleShot(True)

    def set_fractal_data(self, fractal_data):
        """Устанавливает данные фрактала и планирует отрисовку"""
        self.fractal_data = fractal_data
        self._schedule_update()

    def _schedule_update(self):
        """Планирует отрисовку (дебаунсинг)"""
        if not self.draw_timer.isActive():
            self.draw_timer.start(10)  # 10ms дебаунсинг

    def _deferred_update(self):
        """Отрисовка в основном цикле UI (не блокирует)"""
        if hasattr(self, 'fractal_data'):
            self._create_image_from_data()
            self.update()

    def _create_image_from_data(self):
        """Создаёт QImage из данных фрактала (может быть медленным)"""
        height, width = self.fractal_data.shape
        self.image = QImage(width, height, QImage.Format.Format_RGB32)

        # ОПТИМИЗАЦИЯ: используем bits() для прямого доступа к памяти
        self.image.fill(0)  # Быстрая очистка

        # Преобразуем данные в цвета
        for y in range(height):
            for x in range(width):
                color = self._iterations_to_color(self.fractal_data[y, x])
                self.image.setPixel(x, y, self._qRgb(*color))

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
        # print("iter")
        if iterations < 0:
            return 0, 0, 0  # Чёрный, если вне множества
        return self.colormap[iterations % 256]

    # def update_stripe(self, pixels, y_start, y_end):
    #     """
    #     Обновляет изображение полосой пикселей.
    #     pixels — numpy-массив формы (y_end - y_start, width),
    #     содержащий количество итераций для каждого пикселя.
    #     """
    #     height = y_end - y_start
    #     width = pixels.shape[1]
    #
    #     for y in range(height):
    #         for x in range(width):
    #             color = self._iterations_to_color(pixels[y, x])
    #             self.image.setPixel(x, y_start + y, self._qRgb(*color))
    #
    #     self.update()  # Запрашиваем перерисовку

    def paintEvent(self, event):
        """Только быстрая отрисовка готового изображения"""
        if self.image:
            painter = QPainter(self)
            painter.drawImage(self.rect(), self.image)

    def _qRgb(self, r, g, b):
        """Вспомогательный метод для создания QRgb"""
        return (r << 16) | (g << 8) | b
