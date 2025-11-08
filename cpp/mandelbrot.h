#ifndef MANDELBROT_H
#define MANDELBROT_H

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

extern "C" {
    /*
    Вычислить полосу множества Мандельброта

    xmin, xmax, ymin, ymax — диапазон координат фрактала
    max_iter — макс. итераций
    width — ширина изображения (пикселей)
    y_start, y_end — строка вычисляемой полосы (в пикселях по высоте)
    result — указатель на память для вывода результата (int массив размером width*(y_end-y_start))
    */
    EXPORT void compute_mandelbrot_stripe(
        double xmin, double xmax, double ymin, double ymax,
        int max_iter, int width,
        int y_start, int y_end,
        int* result
    );
}

#endif
