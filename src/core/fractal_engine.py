import ctypes
import numpy as np
from pathlib import Path

class FractalEngine:
    def __init__(self):
        # Путь к DLL
        lib_path = Path(__file__).parent.parent.parent / "cpp" / "mandelbrot.dll"
        self.lib = ctypes.CDLL(str(lib_path))

        # Определяем сигнатуру функции compute_mandelbrot_stripe
        self.lib.compute_mandelbrot_stripe.argtypes = [
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]

        # Аналогично для жюлиа
        self.lib.compute_julia_stripe.argtypes = [
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_double, ctypes.c_double,
            ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]

    def compute_mandelbrot_stripe(self, xmin, xmax, ymin, ymax, iterations, width=800, y_start=0, y_end=600):
        stripe_height = y_end - y_start
        buffer = (ctypes.c_int * (width * stripe_height))()
        self.lib.compute_mandelbrot_stripe(
            ctypes.c_double(xmin),
            ctypes.c_double(xmax),
            ctypes.c_double(ymin),
            ctypes.c_double(ymax),
            ctypes.c_int(iterations),
            ctypes.c_int(width),
            ctypes.c_int(y_start),
            ctypes.c_int(y_end),
            buffer
        )
        # Превращаем ctypes массив в numpy
        return np.ctypeslib.as_array(buffer).reshape((stripe_height, width))

    def compute_julia_stripe(self, xmin, xmax, ymin, ymax, c_real, c_imag, iterations, width=800, y_start=0, y_end=600):
        stripe_height = y_end - y_start
        buffer = (ctypes.c_int * (width * stripe_height))()
        self.lib.compute_julia_stripe(
            ctypes.c_double(xmin),
            ctypes.c_double(xmax),
            ctypes.c_double(ymin),
            ctypes.c_double(ymax),
            ctypes.c_double(c_real),
            ctypes.c_double(c_imag),
            ctypes.c_int(iterations),
            ctypes.c_int(width),
            ctypes.c_int(y_start),
            ctypes.c_int(y_end),
            buffer
        )
        return np.ctypeslib.as_array(buffer).reshape((stripe_height, width))
