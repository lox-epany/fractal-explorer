from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np
from .fractal_engine import FractalEngine


class FractalWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray)
    error = pyqtSignal(str)

    def __init__(self, fractal_type, params):
        super().__init__()
        self.fractal_type = fractal_type
        self.params = params
        self.engine = FractalEngine()

    def run(self):
        try:
            if self.fractal_type == "Mandelbrot":
                result = self.engine.calculate_mandelbrot(**self.params)
                print(result)
                self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))