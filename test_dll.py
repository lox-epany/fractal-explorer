import ctypes
import os
import numpy as np

# Загружаем нашу DLL
lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'libmandelbrot.dll')
fractal_lib = ctypes.CDLL(lib_path)

# Определяем типы аргументов для функции
fractal_lib.calculate_mandelbrot.argtypes = [
    ctypes.c_double,  # center_x
    ctypes.c_double,  # center_y
    ctypes.c_double,  # zoom
    ctypes.c_int,     # width
    ctypes.c_int,     # height
    ctypes.POINTER(ctypes.c_int),  # output array
    ctypes.c_int      # max_iterations
]
fractal_lib.calculate_mandelbrot.restype = None

# Тестируем на маленьком размере
width, height = 10, 10
max_iterations = 100

# Создаём массив для результатов
output_array = (ctypes.c_int * (width * height))()

# Вызываем нашу C функцию
fractal_lib.calculate_mandelbrot(
    0.0, 0.0, 1.0,  # center_x, center_y, zoom
    width, height,   # размеры
    output_array,    # массив результатов
    max_iterations   # качество
)

# Преобразуем в numpy для удобства
result = np.ctypeslib.as_array(output_array).reshape(height, width)
print("Результат вычислений:")
print(result)