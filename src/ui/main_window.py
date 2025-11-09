from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QMenuBar,
    QMenu, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,
    QPushButton, QProgressBar, QStatusBar, QApplication
)
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from canvas import Canvas  # кастомный виджет для отображения фракталов
from src.core.worker import FractalWorker
# from ./worker import FractalWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Explorer")
        self.setGeometry(100, 100, 1200, 800)
        self._setup_ui()
        self.canvas.customContextMenuRequested.connect(self._on_canvas_resize)

    def _setup_ui(self):
        # Меню-бар
        menubar = QMenuBar(self)
        fractal_menu = QMenu("Fractal", self)
        file_menu = QMenu("File", self)

        # Действия меню
        mandelbrot_action = QAction("Mandelbrot", self)
        julia_action = QAction("Julia", self)
        fractal_menu.addAction(mandelbrot_action)
        fractal_menu.addAction(julia_action)

        self.export_action = QAction("Export...", self)
        self.import_action = QAction("Import...", self)
        self.save_action = QAction("Save", self)
        self.open_action = QAction("Open", self)
        file_menu.addAction(self.export_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.open_action)

        menubar.addMenu(fractal_menu)
        menubar.addMenu(file_menu)
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

        # Заголовок
        left_layout.addWidget(QLabel("Параметры фрактала:"))

        # Форма параметров
        form = QFormLayout()

        # Выбор фрактала (ComboBox)
        self.fractal_type = QComboBox()
        self.fractal_type.addItems(["Mandelbrot", "Julia"])
        form.addRow("Тип:", self.fractal_type)

        # Диапазон X
        self.xmin = QDoubleSpinBox()
        self.xmin.setRange(-10, 10)
        self.xmin.setValue(-1.5)
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

        # Кнопка вычисления
        self.btn_compute = QPushButton("Вычислить")
        left_layout.addWidget(self.btn_compute)

        # Прогресс-бар
        self.progress = QProgressBar()
        left_layout.addWidget(self.progress)

        # Лейбл для статуса (доп. помимо статус-бара)
        self.label_status = QLabel("Готово.")
        left_layout.addWidget(self.label_status)
        left_layout.addStretch()

        # Центральное место для фрактала
        self.canvas = Canvas(width=800, height=600)

        # Финальный layout
        central_layout.addWidget(left_panel, stretch=0)
        central_layout.addWidget(self.canvas, stretch=1)
        central.setLayout(central_layout)
        self.setCentralWidget(central)

        # подключение кнопок
        self.open_action.triggered.connect(self._open)
        self.save_action.triggered.connect(self._save)
        self.export_action.triggered.connect(self._export)
        self.import_action.triggered.connect(self._import)
        self.btn_compute.clicked.connect(self._button_compute)

        # # создаем поток для вычислений
        # self.thread = QThread()
        # self.worker = FractalWorker()
        # self.worker.moveToThread(self.thread)
        #
        # # Подключаем сигналы для управления UI и обработки результатов
        # self.thread.started.connect(self.worker.do_work)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        #
        # self.worker.progress.connect(self.on_progress)
        # self.worker.preview_ready.connect(self.on_result)
        # self.worker.error.connect(self.on_error)
        # self.worker.stripe_ready.connect(self.on_stripe_ready)

    def _get_fractal_params(self):
        """Преобразует диапазоны в center/zoom формат"""
        # Получаем текущий размер canvas (а не фиксированный)
        canvas_size = self.canvas.size()
        width = canvas_size.width()
        height = canvas_size.height()

        # Вычисляем центр и zoom с учётом соотношения сторон
        center_x = (self.xmin.value() + self.xmax.value()) / 2
        center_y = (self.ymin.value() + self.ymax.value()) / 2

        # Zoom рассчитываем правильно с учётом aspect ratio
        range_x = self.xmax.value() - self.xmin.value()
        range_y = self.ymax.value() - self.ymin.value()

        # Подбираем zoom чтобы вписать в текущие диапазоны
        zoom_x = 2.0 / range_x
        zoom_y = 2.0 / range_y * (height / width)  # Корректируем на aspect ratio

        zoom = min(zoom_x, zoom_y)

        return {
            'center_x': center_x,
            'center_y': center_y,
            'zoom': zoom,
            'width': width,  # Текущая ширина canvas
            'height': height,  # Текущая высота canvas
            'max_iterations': self.iterations.value()
        }

    def _import(self):
        print("imported")

    def _export(self):
        print("exported")

    def _open(self):
        print("opened")

    def _save(self):
        print("saved")

    def _button_compute(self):
        self.statusBar().showMessage("Начало расчёта...")
        self.progress.setValue(0)

        params = self._get_fractal_params()

        # Создаем и запускаем worker
        self.worker = FractalWorker("Mandelbrot", params)
        self.worker.finished.connect(self._on_calculation_finished)
        self.worker.error.connect(self._on_calculation_error)
        self.worker.start()

    def _on_calculation_finished(self, result):
        # Передаём данные в canvas (он сам создаст изображение нужного размера)
        self.canvas.set_fractal_data(result)
        self.statusBar().showMessage("Готово!")

    def _on_calculation_error(self, error_msg):
        print(error_msg)
        self.statusBar().showMessage(f"Ошибка: {error_msg}")

    def _on_canvas_resize(self):
        """При изменении размера canvas можно пересчитать фрактал"""
        # Позже добавим авто-пересчёт при ресайзе
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
