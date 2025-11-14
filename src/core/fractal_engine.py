import ctypes
import numpy as np
import os
import sys


class FractalEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Выбор библиотеки в зависимости от ОС
        if sys.platform == "win32":
            lib_names = ["mandelbrot.dll", "libmandelbrot.dll"]
        else:
            lib_names = ["libmandelbrot.so", "mandelbrot.so"]

        self.lib = None
        for lib_name in lib_names:
            lib_path = os.path.join(base_dir, '..', '..', 'lib', lib_name)
            try:
                if os.path.exists(lib_path):
                    self.lib = ctypes.CDLL(lib_path)
                    print(f"✅ Загружена библиотека: {lib_path}")
                    break
            except Exception as e:
                print(f"❌ Ошибка загрузки {lib_path}: {e}")

        if self.lib is None:
            raise FileNotFoundError(f"Не удалось загрузить библиотеку фракталов")

        self._setup_function_types()

    def _setup_function_types(self):
        # Mandelbrot
        self.lib.calculate_mandelbrot.argtypes = [
            ctypes.c_double, ctypes.c_double,  # center_x, center_y
            ctypes.c_double,  # zoom
            ctypes.c_int, ctypes.c_int,  # width, height
            ctypes.POINTER(ctypes.c_int),  # output
            ctypes.c_int  # max_iterations
        ]
        self.lib.calculate_mandelbrot.restype = None

        # Julia
        self.lib.calculate_julia.argtypes = [
            ctypes.c_double, ctypes.c_double,  # c_real, c_imag
            ctypes.c_double, ctypes.c_double,  # center_x, center_y
            ctypes.c_double,  # zoom
            ctypes.c_int, ctypes.c_int,  # width, height
            ctypes.POINTER(ctypes.c_int),  # output
            ctypes.c_int  # max_iterations
        ]
        self.lib.calculate_julia.restype = None

    def calculate_mandelbrot(self, center_x, center_y, zoom, width, height, max_iterations):
        """Вычисляет множество Мандельброта"""
        output_array = (ctypes.c_int * (width * height))()
        self.lib.calculate_mandelbrot(
            center_x, center_y, zoom,
            width, height, output_array, max_iterations
        )
        return np.ctypeslib.as_array(output_array).reshape(height, width)

    def calculate_julia(self, c_real, c_imag, center_x, center_y, zoom, width, height, max_iterations):
        """Вычисляет множество Жюлиа"""
        output_array = (ctypes.c_int * (width * height))()
        self.lib.calculate_julia(
            c_real, c_imag, center_x, center_y, zoom,
            width, height, output_array, max_iterations
        )
        return np.ctypeslib.as_array(output_array).reshape(height, width)