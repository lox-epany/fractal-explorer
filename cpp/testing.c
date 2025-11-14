#include <pthread.h>

void calculate_mandelbrot(double center_x, double center_y, double zoom,
                         int width, int height, int* output, int max_iterations) {

    double scale = 2.0 / zoom;  // Масштаб: 2.0 покрывает диапазон [-1, 1] при zoom=1

    double pixel_to_real = scale / width;     // Коэффициент для X координаты
    double pixel_to_imag = scale / height;  // Коэффициент для Y координаты

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {

            double cx = (x - width / 2.0) * pixel_to_real + center_x;
            double cy = (y - height / 2.0) * pixel_to_imag + center_y;

            double z_real = 0.0;
            double z_imag = 0.0;

            int iteration = 0;

            while (z_real * z_real + z_imag * z_imag < 4.0 && iteration < max_iterations) {

                double temp = z_real * z_real - z_imag * z_imag + cx;  // real часть
                z_imag = 2.0 * z_real * z_imag + cy;                   // imag часть
                z_real = temp;

                iteration++;
            }

            output[y * width + x] = iteration;
        }
    }
}

int main() {

}