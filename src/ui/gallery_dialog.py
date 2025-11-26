from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QMessageBox
)


class GalleryDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.selected_preset = None
        self.setWindowTitle("Галерея фракталов")
        self.resize(700, 400)
        self._setup_ui()
        self._load_presets()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Таблица пресетов
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Название", "Тип", "Центр X", "Центр Y", "Зум", "Итерации"
        ])

        # Настройка таблицы
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        # Кнопки
        button_layout = QHBoxLayout()
        self.btn_load = QPushButton("Загрузить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_close = QPushButton("Закрыть")

        button_layout.addWidget(self.btn_load)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_close)

        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Подключаем сигналы
        self.btn_load.clicked.connect(self._load_selected)
        self.btn_delete.clicked.connect(self._delete_selected)
        self.btn_close.clicked.connect(self.reject)
        self.table.doubleClicked.connect(self._load_selected)

    def _load_presets(self):
        presets = self.db.load_presets()
        self.table.setRowCount(len(presets))

        for row, preset in enumerate(presets):
            self.table.setItem(row, 0, QTableWidgetItem(preset['name']))
            self.table.setItem(row, 1, QTableWidgetItem(preset['fractal_type']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{preset['center_x']:.4f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{preset['center_y']:.4f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{preset['zoom']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(str(preset['max_iterations'])))

    def _load_selected(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            presets = self.db.load_presets()
            if current_row < len(presets):
                self.selected_preset = presets[current_row]
                self.accept()
        else:
            QMessageBox.warning(self, "Внимание", "Выберите пресет для загрузки")

    def _delete_selected(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            presets = self.db.load_presets()
            if current_row < len(presets):
                preset = presets[current_row]
                reply = QMessageBox.question(
                    self, "Подтверждение",
                    f"Удалить пресет '{preset['name']}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.db.delete_preset(preset['id'])
                    self._load_presets()