#include "mandelbrot.h"
#include <math.h>

/*
 * Вычисление множества Мандельброта
 *
 * Алгоритм:
 * Для каждого пикселя (x,y) мы преобразуем его в координату комплексной плоскости (cx,cy)
 * Затем итерируем формулу: z_{n+1} = z_n^2 + c, где z0 = 0, c = (cx, cy)
 * Пиксель принадлежит множеству Мандельброта, если последовательность не уходит в бесконечность
 */
void calculate_mandelbrot(double center_x, double center_y, double zoom,
                         int width, int height, int* output, int max_iterations) {

    /*
     * Параметры преобразования пикселей → комплексные координаты
     */
    double scale = 2.0 / zoom;  // Масштаб: 2.0 покрывает диапазон [-1, 1] при zoom=1
    double aspect_ratio = (double)height / width;  // Соотношение сторон

    /*
     * Вычисляем смещение для перевода пикселей в комплексные координаты
     * Мы хотим чтобы центр экрана (width/2, height/2) соответствовал (center_x, center_y)
     */
    double pixel_to_real = scale / width;     // Коэффициент для X координаты
    double pixel_to_imag = scale * aspect_ratio / height;  // Коэффициент для Y координаты

    /*
     * Основной цикл по всем пикселям
     * Пока БЕЗ многопоточности - добавим OpenMP позже
     */
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {

            /*
             * Преобразуем координаты пикселя в точку комплексной плоскости
             *
             * (x - width/2.0)  - смещение от центра экрана
             * * pixel_to_real   - масштабирование к мировым координатам
             * + center_x        - смещение к выбранному центру
             */
            double cx = (x - width / 2.0) * pixel_to_real + center_x;
            double cy = (y - height / 2.0) * pixel_to_imag + center_y;

            /*
             * Итерационный процесс для определения принадлежности точке множеству
             * z_real, z_imag - текущее значение z в итерации
             * Мы начинаем с z0 = 0
             */
            double z_real = 0.0;
            double z_imag = 0.0;

            int iteration = 0;

            /*
             * Условия остановки:
             * 1. |z| > 2.0 (точка гарантировано уходит в бесконечность)
             * 2. Достигнуто max_iterations (точка вероятно принадлежит множеству)
             *
             * Мы проверяем |z|^2 < 4 вместо |z| < 2 чтобы избежать квадратного корня
             */
            while (z_real * z_real + z_imag * z_imag < 4.0 && iteration < max_iterations) {
                /*
                 * Формула Мандельброта: z_{n+1} = z_n^2 + c
                 *
                 * Для комплексных чисел:
                 * z^2 = (real + imag*i)^2 = (real^2 - imag^2) + (2*real*imag)*i
                 */
                double temp = z_real * z_real - z_imag * z_imag + cx;  // real часть
                z_imag = 2.0 * z_real * z_imag + cy;                   // imag часть
                z_real = temp;

                iteration++;
            }

            /*
             * Записываем результат в выходной массив
             * iteration = 0..max_iterations
             * - iteration == max_iterations: точка в множестве (обычно чёрный)
             * - iteration < max_iterations: точка вне множества (цвет зависит от итерации)
             */
            output[y * width + x] = iteration;
        }
    }
}