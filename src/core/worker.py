from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np
from .fractal_engine import FractalEngine


class FractalWorker(QThread):
    # Сигналы для общения с главным потоком
    progress_updated = pyqtSignal(int)  # Прогресс в %
    calculation_finished = pyqtSignal(np.ndarray)  # Готовый результат
    error_occurred = pyqtSignal(str)  # Ошибка

    def __init__(self, fractal_type, params):
        super().__init__()
        self.fractal_type = fractal_type
        self.params = params
        self.is_cancelled = False
        self.engine = FractalEngine()

    def run(self):
        """Основной метод, выполняется в отдельном потоке"""
        try:
            self.progress_updated.emit(10)  # Начало вычислений

            if self.is_cancelled:
                return

            # Вычисляем фрактал
            if self.fractal_type == "Mandelbrot":
                result = self.engine.calculate_mandelbrot(**self.params)
            elif self.fractal_type == "Julia":
                result = self.engine.calculate_julia(
                    self.params['c_real'], self.params['c_imag'],
                    **{k: v for k, v in self.params.items() if k not in ['c_real', 'c_imag']}
                )
            else:
                raise ValueError(f"Unknown fractal type: {self.fractal_type}")

            if self.is_cancelled:
                return

            self.progress_updated.emit(100)  # Вычисления завершены
            self.calculation_finished.emit(result)

        except Exception as e:
            self.error_occurred.emit(f"Ошибка вычислений: {str(e)}")

    def cancel(self):
        """Отмена вычислений"""
        self.is_cancelled = True