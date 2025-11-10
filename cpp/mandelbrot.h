#ifndef MANDELBROT_H
#define MANDELBROT_H

// Защита от повторного включения файла

#ifdef __cplusplus
extern "C" {
#endif
    // Если компилятор C++, то оборачиваем в extern "C"
    // для совместимости с ctypes Python
    // УНИВЕРСАЛЬНЫЕ ДИРЕКТИВЫ ЭКСПОРТА
#ifdef _WIN32
#ifdef MANDELBROT_EXPORTS
#define MANDELBROT_API __declspec(dllexport)
#else
#define MANDELBROT_API __declspec(dllimport)
#endif
#else
#define MANDELBROT_API __attribute__((visibility("default")))
#endif
    /*
     * Вычисление множества Мандельброта
     *
     * Параметры:
     *   center_x, center_y - координаты центра видимой области
     *   zoom               - уровень масштабирования (1.0 = стандартный вид)
     *   width, height      - размеры выходного изображения в пикселях
     *   output             - указатель на массив для результатов (width * height)
     *   max_iterations     - максимальное количество итераций на пиксель
     *
     * Возвращает:
     *   void - результат записывается в output массив
     */
    MANDELBROT_API void calculate_mandelbrot(double center_x, double center_y, double zoom,
                             int width, int height, int* output, int max_iterations);

#ifdef __cplusplus
}
#endif

#endif // MANDELBROT_H