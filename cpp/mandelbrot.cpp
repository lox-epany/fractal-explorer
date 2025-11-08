#include "mandelbrot.h"
#include <cmath>

extern "C" {

    EXPORT void compute_mandelbrot_stripe(
        double xmin, double xmax, double ymin, double ymax,
        int max_iter, int width,
        int y_start, int y_end,
        int* result
    ) {
        int stripe_height = y_end - y_start;
        int idx = 0;

        for (int y = y_start; y < y_end; y++) {
            for (int x = 0; x < width; x++) {
                // Преобразуем координаты пикселя в комплексные координаты
                double real = xmin + (xmax - xmin) * x / width;
                double imag = ymin + (ymax - ymin) * y / stripe_height; // высота полосы

                // Начинаем итерации для Мандельброта
                double zr = 0.0, zi = 0.0;
                int iter = 0;

                while (zr * zr + zi * zi < 4.0 && iter < max_iter) {
                    double temp = zr * zr - zi * zi + real;
                    zi = 2.0 * zr * zi + imag;
                    zr = temp;
                    iter++;
                }

                result[idx++] = iter;
            }
        }
    }

}
