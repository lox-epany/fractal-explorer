from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QMenuBar,
    QMenu, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,
    QPushButton, QProgressBar, QStatusBar, QApplication
)
import sys
sys.path.append(sys.path[0][:-6])
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt
from src.ui.canvas import Canvas  # кастомный виджет для отображения фракталов
from src.core.worker import FractalWorker
from src.db.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Explorer")
        self.setGeometry(100, 100, 1200, 800)
        self._setup_ui()
        self.canvas.customContextMenuRequested.connect(self._on_canvas_resize)
        self.worker = None  # Добавляем ссылку на worker
        self.db = Database()

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

        # Меню для галереи
        gallery_menu = QMenu("Галерея", self)
        self.menuBar().addMenu(gallery_menu)

        # Действия
        self.save_preset_action = QAction("Сохранить пресет...", self)
        self.load_preset_action = QAction("Загрузить пресет...", self)
        self.gallery_action = QAction("Галерея...", self)

        gallery_menu.addAction(self.save_preset_action)
        gallery_menu.addAction(self.load_preset_action)
        gallery_menu.addAction(self.gallery_action)

        # Подключаем сигналы
        self.save_preset_action.triggered.connect(self._save_preset)
        self.load_preset_action.triggered.connect(self._load_preset)
        self.gallery_action.triggered.connect(self._show_gallery)

        # Настраиваем callback для canvas
        self.canvas.set_recalculation_callback(self._on_navigation_changed)

        # Добавляем кнопку сброса
        self.btn_reset = QPushButton("Сброс вида")
        # Добавь эту кнопку в layout где-то после btn_compute
        self.btn_reset.clicked.connect(self.canvas.reset_view)

    def _get_fractal_params(self):
        """Преобразует диапазоны в center/zoom формат"""
        # Получаем текущий размер canvas (а не фиксированный)
        canvas_size = self.canvas.size()
        width = canvas_size.width()
        height = canvas_size.height()

        c_real = self.c_real.value()
        c_imag = self.c_imag.value()

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
        print(self.fractal_type.currentText())

        if self.fractal_type.currentText() == "Mandelbrot":
            return {
            'center_x': center_x,
            'center_y': center_y,
            'zoom': zoom,
            'width': width,  # Текущая ширина canvas
            'height': height,  # Текущая высота canvas
            'max_iterations': self.iterations.value()
        }
        else: return {
            'c_real': c_real,
            'c_imag': c_imag,
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
        """Запуск вычислений в отдельном потоке"""
        if self.worker and self.worker.isRunning():
            self.statusBar().showMessage("Вычисления уже запущены...")
            return

        self.statusBar().showMessage("Подготовка вычислений...")
        self.progress.setValue(0)
        self.btn_compute.setEnabled(False)  # Блокируем кнопку

        # Получаем параметры
        params = self._get_fractal_params()
        fractal_type = self.fractal_type.currentText()

        # Создаем и настраиваем worker
        self.worker = FractalWorker(fractal_type, params)
        self.worker.progress_updated.connect(self._on_progress_updated)
        self.worker.calculation_finished.connect(self._on_calculation_finished)
        self.worker.error_occurred.connect(self._on_calculation_error)

        # Запускаем
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
        print(f"Ошибка: {error_msg}")

    def closeEvent(self, event):
        """При закрытии окна останавливаем worker если он запущен"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait(1000)  # Ждем 1 секунду для завершения
        event.accept()

    def _on_canvas_resize(self):
        """При изменении размера canvas можно пересчитать фрактал"""
        # Позже добавим авто-пересчёт при ресайзе
        pass

    def _save_preset(self):
        """Сохранение текущих параметров как пресета"""
        from PyQt6.QtWidgets import QInputDialog

        name, ok = QInputDialog.getText(
            self, "Сохранение пресета", "Введите название пресета:"
        )

        if ok and name:
            try:
                params = self._get_fractal_params()
                fractal_type = self.fractal_type.currentText()

                # Сохраняем в БД
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
        """Загрузка пресета из БД"""
        from PyQt6.QtWidgets import QInputDialog, QListWidget, QDialog, QVBoxLayout, QDialogButtonBox

        # Получаем пресеты из БД
        presets = self.db.load_presets()

        if not presets:
            self.statusBar().showMessage("Нет сохраненных пресетов")
            return

        # Диалог выбора пресета
        dialog = QDialog(self)
        dialog.setWindowTitle("Выберите пресет")
        layout = QVBoxLayout()

        list_widget = QListWidget()
        for preset in presets:
            list_widget.addItem(f"{preset['name']} ({preset['fractal_type']})")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addWidget(list_widget)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted and list_widget.currentItem():
            selected_preset = presets[list_widget.currentRow()]
            self._apply_preset(selected_preset)

    def _apply_preset(self, preset):
        """Применяет параметры пресета к UI"""
        try:
            # Устанавливаем тип фрактала
            index = self.fractal_type.findText(preset['fractal_type'])
            if index >= 0:
                self.fractal_type.setCurrentIndex(index)

            # Вычисляем диапазоны из center/zoom
            range_x = 2.0 / preset['zoom']
            range_y = range_x * (self.canvas.height() / self.canvas.width())

            self.xmin.setValue(preset['center_x'] - range_x / 2)
            self.xmax.setValue(preset['center_x'] + range_x / 2)
            self.ymin.setValue(preset['center_y'] - range_y / 2)
            self.ymax.setValue(preset['center_y'] + range_y / 2)
            self.iterations.setValue(preset['max_iterations'])

            # Параметры Julia
            if preset['fractal_type'] == 'Julia':
                if preset['c_real'] is not None:
                    self.c_real.setValue(preset['c_real'])
                if preset['c_imag'] is not None:
                    self.c_imag.setValue(preset['c_imag'])

            self.statusBar().showMessage(f"Загружен пресет: {preset['name']}")

        except Exception as e:
            self.statusBar().showMessage(f"Ошибка загрузки пресета: {str(e)}")

    def _show_gallery(self):
        """Показывает галерею сохраненных фракталов"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel, QHBoxLayout
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import Qt

        presets = self.db.load_presets()

        if not presets:
            self.statusBar().showMessage("Галерея пуста")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Галерея фракталов")
        dialog.resize(600, 400)

        layout = QHBoxLayout()

        # Список пресетов
        preset_list = QListWidget()
        for preset in presets:
            preset_list.addItem(f"{preset['name']} ({preset['fractal_type']})")

        # Информация о выбранном пресете
        info_label = QLabel("Выберите пресет из списка")
        info_label.setWordWrap(True)

        preset_list.currentRowChanged.connect(
            lambda row: info_label.setText(self._format_preset_info(presets[row]))
        )

        layout.addWidget(preset_list, 1)
        layout.addWidget(info_label, 2)

        dialog.setLayout(layout)
        dialog.exec()

    def _format_preset_info(self, preset):
        """Форматирует информацию о пресете для отображения"""
        return f"""
        <b>{preset['name']}</b><br>
        Тип: {preset['fractal_type']}<br>
        Центр: ({preset['center_x']:.4f}, {preset['center_y']:.4f})<br>
        Масштаб: {preset['zoom']:.2f}<br>
        Итерации: {preset['max_iterations']}<br>
        {f"Параметр C: ({preset['c_real']:.4f} + {preset['c_imag']:.4f}i)" if preset['fractal_type'] == 'Julia' else ''}
        """

    def _on_navigation_changed(self, params):
        """Вызывается когда пользователь изменяет вид через canvas"""
        self.statusBar().showMessage("Пересчёт...")

        # Обновляем UI параметры чтобы они соответствовали навигации
        self._update_ui_from_canvas(params)

        # Запускаем вычисления
        fractal_type = self.fractal_type.currentText()
        if fractal_type == "Julia":
            params['c_real'] = self.c_real.value()
            params['c_imag'] = self.c_imag.value()

        self._start_calculation(fractal_type, params)

    def _update_ui_from_canvas(self, params):
        """Обновляет UI параметры из параметров canvas"""
        # Вычисляем диапазоны для отображения в UI
        range_x = 2.0 / params['zoom']
        range_y = range_x * (params['height'] / params['width'])

        self.xmin.setValue(params['center_x'] - range_x / 2)
        self.xmax.setValue(params['center_x'] + range_x / 2)
        self.ymin.setValue(params['center_y'] - range_y / 2)
        self.ymax.setValue(params['center_y'] + range_y / 2)

    def _start_calculation(self, fractal_type, params):
        """Запускает вычисления с новыми параметрами"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()  # Отменяем предыдущие вычисления

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
