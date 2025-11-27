from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFormLayout, QMenuBar,
    QMenu, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,
    QPushButton, QProgressBar, QStatusBar, QApplication, QInputDialog,
    QDialog, QVBoxLayout, QFileDialog, QMessageBox
)
import sys

sys.path.append(sys.path[0][:-6])
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThread, Qt
from src.ui.canvas import Canvas
from src.core.worker import FractalWorker
from src.db.database import Database
from src.ui.gallery_dialog import GalleryDialog
from src.resources.themes import Themes
from src.ui.color_dialog import ColorSchemeDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Explorer")
        self.setGeometry(100, 100, 1200, 800)

        self.worker = None
        self.db = Database()
        self.current_theme = "light"

        self._setup_ui()
        self._setup_themes_menu()
        self._setup_color_menu()

        self.canvas.customContextMenuRequested.connect(self._on_canvas_resize)

    def _setup_ui(self):
        # Меню-бар
        menubar = QMenuBar(self)

        # Меню галереи
        gallery_menu = QMenu("Галерея", self)
        menubar.addMenu(gallery_menu)

        # Действия для меню галереи
        self.save_preset_action = QAction("Сохранить пресет...", self)
        self.load_preset_action = QAction("Загрузить пресет...", self)
        self.export_action = QAction("Экспорт изображения...", self)
        # self.gallery_action = QAction("Просмотр галереи...", self)

        gallery_menu.addAction(self.save_preset_action)
        gallery_menu.addAction(self.load_preset_action)
        gallery_menu.addAction(self.export_action)
        gallery_menu.addSeparator()
        # gallery_menu.addAction(self.gallery_action)

        self.setMenuBar(menubar)

        # Статус-бар
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # Центральный виджет
        central = QWidget(self)
        central_layout = QHBoxLayout()

        # Левая колонка параметров
        left_panel = QWidget(self)
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setObjectName("left_panel")

        # Заголовок
        left_layout.addWidget(QLabel("Параметры фрактала:"))

        # Форма параметров
        form = QFormLayout()

        # Выбор фрактала
        self.fractal_type = QComboBox()
        self.fractal_type.addItems(["Mandelbrot", "Julia"])
        form.addRow("Тип:", self.fractal_type)

        # Диапазон X
        self.xmin = QDoubleSpinBox()
        self.xmin.setRange(-10, 10)
        self.xmin.setValue(-1.0)
        form.addRow("X min:", self.xmin)

        self.xmax = QDoubleSpinBox()
        self.xmax.setRange(-10, 10)
        self.xmax.setValue(1.0)
        form.addRow("X max:", self.xmax)

        # Диапазон Y
        self.ymin = QDoubleSpinBox()
        self.ymin.setRange(-10, 10)
        self.ymin.setValue(-1.25)
        form.addRow("Y min:", self.ymin)

        self.ymax = QDoubleSpinBox()
        self.ymax.setRange(-10, 10)
        self.ymax.setValue(1.25)
        form.addRow("Y max:", self.ymax)

        # Итерации
        self.iterations = QSpinBox()
        self.iterations.setRange(10, 3000)
        self.iterations.setValue(256)
        form.addRow("Итерации:", self.iterations)

        # Параметры для Julia
        self.c_real = QDoubleSpinBox()
        self.c_real.setRange(-2, 2)
        self.c_real.setValue(-0.7)
        form.addRow("C real:", self.c_real)

        self.c_imag = QDoubleSpinBox()
        self.c_imag.setRange(-2, 2)
        self.c_imag.setValue(0.27015)
        form.addRow("C imag:", self.c_imag)

        left_layout.addLayout(form)

        # Кнопки управления
        self.btn_compute = QPushButton("Вычислить")
        self.btn_reset = QPushButton("Сброс вида")

        left_layout.addWidget(self.btn_compute)
        left_layout.addWidget(self.btn_reset)

        # Прогресс-бар
        self.progress = QProgressBar()
        left_layout.addWidget(self.progress)

        # Статус
        self.label_status = QLabel("Готово.")
        left_layout.addWidget(self.label_status)
        left_layout.addStretch()

        # Холст для фрактала
        self.canvas = Canvas(width=800, height=600)

        # Финальный layout
        central_layout.addWidget(left_panel, stretch=0)
        central_layout.addWidget(self.canvas, stretch=1)
        central.setLayout(central_layout)
        self.setCentralWidget(central)
        central.setObjectName("centralWidget")

        # Подключение сигналов
        self.export_action.triggered.connect(self._export)
        self.save_preset_action.triggered.connect(self._save_preset)
        self.load_preset_action.triggered.connect(self._load_preset)
        # self.gallery_action.triggered.connect(self._show_gallery)
        self.btn_compute.clicked.connect(self._button_compute)
        self.btn_reset.clicked.connect(self.canvas.reset_view)

        self.canvas.set_recalculation_callback(self._on_navigation_changed)

    def _setup_themes_menu(self):
        """Добавляем меню выбора темы"""
        theme_menu = QMenu("Темы", self)
        self.menuBar().addMenu(theme_menu)

        themes = {
            "Светлая": "light",
            "Тёмная": "dark",
            "Розовая с цветочками 🌸": "pink"
        }

        for theme_name, theme_key in themes.items():
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, key=theme_key: self._change_theme(key))
            theme_menu.addAction(action)

    def _setup_color_menu(self):
        """Добавляем меню выбора цветовой схемы"""
        color_menu = QMenu("Цвета", self)
        self.menuBar().addMenu(color_menu)

        color_schemes = {
            "Классическая": "classic",
            "Радуга": "rainbow",
            "Огонь": "fire",
            "Океан": "ocean",
            "Лес": "forest",
            "Розовая мечта 🌸": "pink_dream",
            "Неон": "neon",
            "Закат": "sunset"
        }

        for name, scheme in color_schemes.items():
            action = QAction(name, self)
            action.triggered.connect(lambda checked, s=scheme: self._change_color_scheme(s))
            color_menu.addAction(action)

        color_menu.addSeparator()

        custom_action = QAction("Настроить цвета...", self)
        custom_action.triggered.connect(self._show_color_dialog)
        color_menu.addAction(custom_action)

    def _get_fractal_params(self):
        """Преобразует диапазоны в center/zoom формат"""
        canvas_size = self.canvas.size()
        width = canvas_size.width()
        height = canvas_size.height()

        center_x = (self.xmin.value() + self.xmax.value()) / 2
        center_y = (self.ymin.value() + self.ymax.value()) / 2

        range_x = self.xmax.value() - self.xmin.value()
        range_y = self.ymax.value() - self.ymin.value()

        zoom_x = 2.0 / range_x
        zoom_y = 2.0 / range_y * (height / width)
        zoom = min(zoom_x, zoom_y)

        base_params = {
            'center_x': center_x,
            'center_y': center_y,
            'zoom': zoom,
            'width': width,
            'height': height,
            'max_iterations': self.iterations.value()
        }

        if self.fractal_type.currentText() == "Julia":
            base_params.update({
                'c_real': self.c_real.value(),
                'c_imag': self.c_imag.value()
            })

        return base_params

    def _export(self):
        """Экспорт текущего фрактала в PNG"""
        if not hasattr(self.canvas, 'image') or self.canvas.image.isNull():
            QMessageBox.warning(self, "Ошибка", "Нет изображения для экспорта")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт фрактала", "",
            "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg);;All Files (*)"
        )

        if filename:
            if self.canvas.export_image(filename):
                self.statusBar().showMessage(f"Изображение сохранено: {filename}")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изображение")

    def _button_compute(self):
        """Запуск вычислений в отдельном потоке"""
        if self.worker and self.worker.isRunning():
            self.statusBar().showMessage("Вычисления уже запущены...")
            return

        self.statusBar().showMessage("Подготовка вычислений...")
        self.progress.setValue(0)
        self.btn_compute.setEnabled(False)

        params = self._get_fractal_params()
        fractal_type = self.fractal_type.currentText()

        self.worker = FractalWorker(fractal_type, params)
        self.worker.progress_updated.connect(self._on_progress_updated)
        self.worker.calculation_finished.connect(self._on_calculation_finished)
        self.worker.error_occurred.connect(self._on_calculation_error)

        self.worker.start()
        self.statusBar().showMessage("Вычисления запущены...")

    def _on_progress_updated(self, progress):
        """Обновление прогресс-бара"""
        self.progress.setValue(progress)

    def _on_calculation_finished(self, result):
        """Вычисления завершены успешно"""
        self.canvas.set_fractal_data(result)
        self.progress.setValue(100)
        self.btn_compute.setEnabled(True)
        self.statusBar().showMessage("Готово!")

    def _on_calculation_error(self, error_msg):
        """Обработка ошибок"""
        self.progress.setValue(0)
        self.btn_compute.setEnabled(True)
        self.statusBar().showMessage(error_msg)

    def closeEvent(self, event):
        """При закрытии окна останавливаем worker если он запущен"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait(1000)
        event.accept()

    def _on_canvas_resize(self):
        """При изменении размера canvas можно пересчитать фрактал"""
        pass

    def _save_preset(self):
        """Сохранение текущих параметров как пресета"""
        name, ok = QInputDialog.getText(self, "Сохранение пресета", "Введите название пресета:")

        if ok and name:
            try:
                params = self._get_fractal_params()
                fractal_type = self.fractal_type.currentText()

                self.db.save_preset(
                    name=name,
                    fractal_type=fractal_type,
                    center_x=params['center_x'],
                    center_y=params['center_y'],
                    zoom=params['zoom'],
                    max_iterations=params['max_iterations'],
                    c_real=self.c_real.value() if fractal_type == "Julia" else None,
                    c_imag=self.c_imag.value() if fractal_type == "Julia" else None
                )

                self.statusBar().showMessage(f"Пресет '{name}' сохранен!")
            except Exception as e:
                self.statusBar().showMessage(f"Ошибка сохранения: {str(e)}")

    def _load_preset(self):
        """Загрузка пресета через табличный диалог"""
        dialog = GalleryDialog(self.db, self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_preset:
            self._apply_preset(dialog.selected_preset)

    def _apply_preset(self, preset):
        """Применяет параметры пресета к UI"""
        try:
            index = self.fractal_type.findText(preset['fractal_type'])
            if index >= 0:
                self.fractal_type.setCurrentIndex(index)

            range_x = 2.0 / preset['zoom']
            range_y = range_x * (self.canvas.height() / self.canvas.width())

            self.xmin.setValue(preset['center_x'] - range_x / 2)
            self.xmax.setValue(preset['center_x'] + range_x / 2)
            self.ymin.setValue(preset['center_y'] - range_y / 2)
            self.ymax.setValue(preset['center_y'] + range_y / 2)
            self.iterations.setValue(preset['max_iterations'])

            if preset['fractal_type'] == 'Julia':
                if preset['c_real'] is not None:
                    self.c_real.setValue(preset['c_real'])
                if preset['c_imag'] is not None:
                    self.c_imag.setValue(preset['c_imag'])

            self.statusBar().showMessage(f"Загружен пресет: {preset['name']}")
        except Exception as e:
            self.statusBar().showMessage(f"Ошибка загрузки пресета: {str(e)}")

    def _show_gallery(self):
        """Показ галереи через табличный диалог"""
        dialog = GalleryDialog(self.db, self)
        dialog.exec()

    def _on_navigation_changed(self, params):
        """Вызывается когда пользователь изменяет вид через canvas"""
        self.statusBar().showMessage("Пересчёт...")
        self._update_ui_from_canvas(params)

        fractal_type = self.fractal_type.currentText()
        if fractal_type == "Julia":
            params['c_real'] = self.c_real.value()
            params['c_imag'] = self.c_imag.value()

        self._start_calculation(fractal_type, params)

    def _update_ui_from_canvas(self, params):
        """Обновляет UI параметры из параметров canvas"""
        range_x = 2.0 / params['zoom']
        range_y = range_x * (params['height'] / params['width'])

        self.xmin.setValue(params['center_x'] - range_x / 2)
        self.xmax.setValue(params['center_x'] + range_x / 2)
        self.ymin.setValue(params['center_y'] - range_y / 2)
        self.ymax.setValue(params['center_y'] + range_y / 2)

    def _start_calculation(self, fractal_type, params):
        """Запускает вычисления с новыми параметрами"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()

        self.worker = FractalWorker(fractal_type, params)
        self.worker.progress_updated.connect(self._on_progress_updated)
        self.worker.calculation_finished.connect(self._on_calculation_finished)
        self.worker.error_occurred.connect(self._on_calculation_error)
        self.worker.start()

    def keyPressEvent(self, event):
        """Обработка горячих клавиш"""
        if event.key() == Qt.Key.Key_R:
            self.canvas.reset_view()
        elif event.key() == Qt.Key.Key_Equal:  # +
            self.canvas._zoom_at_center(1.5)
        elif event.key() == Qt.Key.Key_Minus:  # -
            self.canvas._zoom_at_center(0.67)
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def _change_theme(self, theme_name):
        """Меняет тему приложения"""
        self.current_theme = theme_name
        theme_css = Themes.get_theme(theme_name)
        self.setStyleSheet(theme_css)
        self.statusBar().showMessage(f"Тема изменена: {theme_name}")

    def _change_color_scheme(self, scheme_name):
        """Быстрая смена цветовой схемы"""
        self.canvas.set_color_scheme(scheme_name)
        self.statusBar().showMessage(f"Цветовая схема: {scheme_name}")

    def _show_color_dialog(self):
        """Показывает диалог выбора цветовой схемы"""
        dialog = ColorSchemeDialog(self.canvas.current_color_scheme, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.selected_scheme == "custom" and dialog.custom_colors:
                self.canvas.set_custom_colors(dialog.custom_colors)
                self.statusBar().showMessage("Применена кастомная цветовая схема")
            else:
                self._change_color_scheme(dialog.selected_scheme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())