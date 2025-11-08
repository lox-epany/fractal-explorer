from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import time
from .fractal_engine import FractalEngine

class FractalWorker(QObject):
    # Сигналы для вывода прогресса, частичных результатов, ошибок, окончания
    progress = pyqtSignal(int)  # от 0 до 100
    stripe_ready = pyqtSignal(object, int, int)  # numpy массив, y_start, y_end
    preview_ready = pyqtSignal(object)  # для быстрого превью
    finished = pyqtSignal(float)  # время работы
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.engine = FractalEngine()

    @pyqtSlot(dict)
    def compute_mandelbrot_adaptive(self, params):
        # Адаптивная прорисовка: превью + полный размер
        try:
            start = time.time()

            # Извлекаем параметры
            xmin, xmax = params['xmin'], params['xmax']
            ymin, ymax = params['ymin'], params['ymax']
            iterations = params['iterations']
            width, height = params['width'], params['height']

            # 1. Быстрое превью в меньшем разрешении
            preview_scale = 4
            preview_w = width // preview_scale
            preview_h = height // preview_scale
            preview_pixels = self.engine.compute_mandelbrot_stripe(
                xmin, xmax, ymin, ymax, iterations,
                preview_w, 0, preview_h
            )
            # Отправляем превью
            self.preview_ready.emit(preview_pixels)
            self.progress.emit(10)

            # 2. Полный расчёт полосами
            stripe_h = 50
            num_stripes = (height + stripe_h - 1) // stripe_h
            for i in range(num_stripes):
                y0 = i * stripe_h
                y1 = min((i + 1) * stripe_h, height)
                pixels = self.engine.compute_mandelbrot_stripe(
                    xmin, xmax, ymin, ymax, iterations,
                    width, y0, y1
                )
                self.stripe_ready.emit(pixels, y0, y1)
                self.progress.emit(10 + int((i + 1) / num_stripes * 90))

            self.finished.emit(time.time() - start)

        except Exception as e:
            self.error.emit(str(e))
