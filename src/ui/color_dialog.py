from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QLabel, QListWidget, QColorDialog, QFrame, QScrollArea, QWidget,
    QGridLayout
)
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
from PyQt6.QtCore import Qt, QRectF
from src.core.color_schemes import ColorSchemes


class ColorSchemeDialog(QDialog):
    def __init__(self, current_scheme, parent=None):
        super().__init__(parent)
        self.current_scheme = current_scheme
        self.selected_scheme = current_scheme
        self.custom_colors = []
        self.setWindowTitle("Выбор цветовой схемы")
        self.resize(600, 500)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Выбор предустановленных схем
        layout.addWidget(QLabel("Предустановленные схемы:"))

        self.scheme_list = QListWidget()
        schemes = [
            "classic", "rainbow", "fire", "ocean",
            "forest", "pink_dream", "neon", "sunset"
        ]

        scheme_names = {
            "classic": "Классическая",
            "rainbow": "Радуга",
            "fire": "Огонь",
            "ocean": "Океан",
            "forest": "Лес",
            "pink_dream": "Розовая мечта 🌸",
            "neon": "Неон",
            "sunset": "Закат"
        }

        for scheme in schemes:
            self.scheme_list.addItem(scheme_names[scheme])

        # Превью выбранной схемы
        self.preview = ColorSchemePreview()
        self.scheme_list.currentRowChanged.connect(self._on_scheme_selected)

        # Кнопка создания кастомной схемы
        self.btn_custom = QPushButton("Создать свою схему")
        self.btn_custom.clicked.connect(self._create_custom_scheme)

        # Область для кастомных цветов
        self.custom_widget = QWidget()
        self.custom_layout = QHBoxLayout()
        self.custom_widget.setLayout(self.custom_layout)
        self.custom_widget.hide()

        self.btn_add_color = QPushButton("+ Добавить цвет")
        self.btn_add_color.clicked.connect(self._add_custom_color)

        # Кнопки диалога
        button_layout = QHBoxLayout()
        self.btn_apply = QPushButton("Применить")
        self.btn_cancel = QPushButton("Отмена")

        button_layout.addWidget(self.btn_apply)
        button_layout.addWidget(self.btn_cancel)

        # Компоновка
        schemes_layout = QHBoxLayout()
        schemes_layout.addWidget(self.scheme_list, 1)
        schemes_layout.addWidget(self.preview, 2)

        layout.addLayout(schemes_layout)
        layout.addWidget(self.btn_custom)
        layout.addWidget(self.custom_widget)
        layout.addWidget(self.btn_add_color)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Подключаем сигналы
        self.btn_apply.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        # Устанавливаем текущую схему
        if self.current_scheme in schemes:
            index = schemes.index(self.current_scheme)
            self.scheme_list.setCurrentRow(index)

    def _on_scheme_selected(self, row):
        schemes = ["classic", "rainbow", "fire", "ocean", "forest", "pink_dream", "neon", "sunset"]
        if 0 <= row < len(schemes):
            self.selected_scheme = schemes[row]
            self.preview.set_scheme(self.selected_scheme)

    def _create_custom_scheme(self):
        self.custom_widget.show()
        self.selected_scheme = "custom"

    def _add_custom_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color_frame = QFrame()
            color_frame.setFixedSize(30, 30)
            color_frame.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            self.custom_layout.addWidget(color_frame)
            self.custom_colors.append((color.red(), color.green(), color.blue()))


class ColorSchemePreview(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.setStyleSheet("border: 2px solid gray;")
        self.scheme_name = "classic"

    def set_scheme(self, scheme_name):
        self.scheme_name = scheme_name
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        colors = ColorSchemes.get_scheme(self.scheme_name)

        width = self.width()
        height = self.height()

        for i, color in enumerate(colors):
            x = (i / 256.0) * width
            rect_width = width / 256.0

            painter.fillRect(
                int(x), 0, int(rect_width) + 1, height,
                QColor(color[0], color[1], color[2])
            )