from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter, QImageWriter
from PyQt6.QtCore import Qt, QTimer, QPointF
import os
from src.core.color_schemes import ColorSchemes


class Canvas(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.image = None
        self.colormap = self._create_colormap()
        self.pending_update = False
        self.draw_timer = QTimer()
        self.draw_timer.timeout.connect(self._deferred_update)
        self.draw_timer.setSingleShot(True)

        # Параметры навигации
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        self.max_iterations = 256

        # Для панорамирования
        self.is_panning = False
        self.last_mouse_pos = QPointF()

        # Для автоматического пересчёта
        self.recalculation_callback = None

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Чтобы получать события клавиатуры
        self.setMouseTracking(True)  # Отслеживание движения мыши

        # настройка градиентов для фракталов
        self.current_color_scheme = "classic"
        self.colormap = ColorSchemes.get_scheme(self.current_color_scheme)

    def set_recalculation_callback(self, callback):
        """Устанавливает функцию для пересчёта фрактала"""
        self.recalculation_callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Зум в точку клика
            self._zoom_to_point(event.position())
        elif event.button() == Qt.MouseButton.RightButton:
            # Начало панорамирования
            self.is_panning = True
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.is_panning:
            # Панорамирование
            delta = event.position() - self.last_mouse_pos
            self._pan(delta.x(), delta.y())
            self.last_mouse_pos = event.position()

    def wheelEvent(self, event):
        """Зум колесом мыши"""
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self._zoom_at_center(zoom_factor)

    def _zoom_to_point(self, point):
        """Приближение к точке клика"""
        # Преобразуем координаты мыши в мировые координаты
        width = self.width()
        height = self.height()

        scale = 2.0 / self.zoom
        aspect_ratio = width / height
        world_width = scale
        world_height = scale / aspect_ratio

        mouse_x = (point.x() - width / 2.0) * world_width / width + self.center_x
        mouse_y = (point.y() - height / 2.0) * world_height / height + self.center_y

        # Увеличиваем зум
        self.zoom *= 1.5

        # Новый центр - точка клика
        self.center_x = mouse_x
        self.center_y = mouse_y

        self._recalculate_fractal()

    def _zoom_at_center(self, zoom_factor):
        """Зум относительно центра"""
        self.zoom *= zoom_factor
        self._recalculate_fractal()

    def _pan(self, dx, dy):
        """Панорамирование"""
        width = self.width()
        height = self.height()

        scale = 2.0 / self.zoom
        aspect_ratio = width / height
        world_width = scale
        world_height = scale / aspect_ratio

        # Смещение в мировых координатах
        delta_x = -dx * world_width / width
        delta_y = -dy * world_height / height

        self.center_x += delta_x
        self.center_y += delta_y

        self._recalculate_fractal()

    def _recalculate_fractal(self):
        """Запускает пересчёт фрактала"""
        if self.recalculation_callback:
            params = {
                'center_x': self.center_x,
                'center_y': self.center_y,
                'zoom': self.zoom,
                'width': self.width(),
                'height': self.height(),
                'max_iterations': self.max_iterations
            }
            self.recalculation_callback(params)

    def reset_view(self):
        """Сброс к начальному виду"""
        self.center_x = 0.0
        self.center_y = 0.0
        self.zoom = 1.0
        self._recalculate_fractal()

    def get_current_params(self):
        """Возвращает текущие параметры вида"""
        return {
            'center_x': self.center_x,
            'center_y': self.center_y,
            'zoom': self.zoom
        }

    def set_params(self, center_x, center_y, zoom):
        """Устанавливает параметры вида"""
        self.center_x = center_x
        self.center_y = center_y
        self.zoom = zoom

    def set_fractal_data(self, fractal_data):
        """Устанавливает данные фрактала и планирует отрисовку"""
        self.fractal_data = fractal_data
        self._schedule_update()

    def _schedule_update(self):
        """Планирует отрисовку (дебаунсинг)"""
        if not self.draw_timer.isActive():
            self.draw_timer.start(10)  # 10ms дебаунсинг

    def _deferred_update(self):
        """Отрисовка в основном цикле UI (не блокирует)"""
        if hasattr(self, 'fractal_data'):
            self._create_image_from_data()
            self.update()

    def _create_image_from_data(self):
        """Создаёт QImage из данных фрактала (может быть медленным)"""
        height, width = self.fractal_data.shape
        self.image = QImage(width, height, QImage.Format.Format_RGB32)

        # ОПТИМИЗАЦИЯ: используем bits() для прямого доступа к памяти
        self.image.fill(0)  # Быстрая очистка

        # Преобразуем данные в цвета
        for y in range(height):
            for x in range(width):
                color = self._iterations_to_color(self.fractal_data[y, x])
                self.image.setPixel(x, y, self._qRgb(*color))

    @staticmethod
    def _create_colormap():
        """Создаёт цветовую палитру с плавным градиентом"""
        colors = []
        for i in range(256):
            if i < 64:
                r, g, b = 0, 0, i * 4
            elif i < 128:
                r, g, b = 0, (i - 64) * 4, 255
            elif i < 192:
                r, g, b = (i - 128) * 4, 255, 255
            else:
                r, g, b = 255, 255, 255
            colors.append((r, g, b))
        return colors

    def _iterations_to_color(self, iterations):
        """Преобразует количество итераций в RGB цвет по палитре"""
        # print("iter")
        if iterations < 0:
            return 0, 0, 0  # Чёрный, если вне множества
        return self.colormap[iterations % 256]


    def paintEvent(self, event):
        """Только быстрая отрисовка готового изображения"""
        if self.image:
            painter = QPainter(self)
            painter.drawImage(self.rect(), self.image)

    def _qRgb(self, r, g, b):
        """Вспомогательный метод для создания QRgb"""
        return (r << 16) | (g << 8) | b

    def export_image(self, filename, quality=100):
        """Экспортирует текущее изображение в файл"""
        if self.image:
            writer = QImageWriter(filename)

            # Определяем формат по расширению
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                writer.setFormat(ext[1:].encode())

            writer.setQuality(quality)

            if writer.write(self.image):
                return True
            else:
                print(f"Ошибка экспорта: {writer.errorString()}")
                return False
        return False

    def set_color_scheme(self, scheme_name):
        """Устанавливает цветовую схему"""
        self.current_color_scheme = scheme_name
        self.colormap = ColorSchemes.get_scheme(scheme_name)
        if hasattr(self, 'fractal_data'):
            self._create_image_from_data()
            self.update()

    def set_custom_colors(self, colors_list):
        """Устанавливает кастомную цветовую схему"""
        self.current_color_scheme = "custom"
        self.colormap = ColorSchemes.custom_scheme(colors_list)
        if hasattr(self, 'fractal_data'):
            self._create_image_from_data()
            self.update()