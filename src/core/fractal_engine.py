import ctypes
import numpy as np
import os


class FractalEngine:
    def __init__(self):
        self.lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), '..', '..', 'lib', 'libmandelbrot.dll'))
        self._setup_function_types()

    def _setup_function_types(self):
        self.lib.calculate_mandelbrot.argtypes = [
            ctypes.c_double, ctypes.c_double,  # center_x, center_y
            ctypes.c_double,                   # zoom
            ctypes.c_int, ctypes.c_int,        # width, height
            ctypes.POINTER(ctypes.c_int),      # output
            ctypes.c_int                       # max_iterations
        ]
        self.lib.calculate_mandelbrot.restype = None

    def calculate_mandelbrot(self, center_x, center_y, zoom, width, height, max_iterations):
        output_array = (ctypes.c_int * (width * height))()
        self.lib.calculate_mandelbrot(center_x, center_y, zoom, width, height, output_array, max_iterations)
        return np.ctypeslib.as_array(output_array).reshape(width, height)