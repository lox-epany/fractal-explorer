class Themes:
    @staticmethod
    def get_theme(theme_name):
        themes = {
            "light": Themes.light_theme(),
            "dark": Themes.dark_theme(),
            "pink": Themes.pink_flower_theme_with_pattern()
        }
        return themes.get(theme_name, Themes.light_theme())

    @staticmethod
    def light_theme():
        return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        QWidget {
            background-color: #f0f0f0;
            color: #333333;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 4px;
            border: 1px solid #ccc;
            border-radius: 3px;
            background-color: white;
        }
        QProgressBar {
            border: 1px solid #ccc;
            border-radius: 3px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
        }
        """

    @staticmethod
    def dark_theme():
        return """
        QMainWindow {
            background-color: #2b2b2b;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #666666;
        }
        QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 4px;
            border: 1px solid #555;
            border-radius: 3px;
            background-color: #404040;
            color: white;
        }
        QProgressBar {
            border: 1px solid #555;
            border-radius: 3px;
            text-align: center;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #bb86fc;
        }
        """

    @staticmethod
    def pink_flower_theme():
        return """
        /* 🌸 Розовая тема с цветочками - УЛУЧШЕННАЯ ВЕРСИЯ */
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #fff0f5, stop:0.3 #ffe4ec, stop:1 #fadadd);
            border: 2px solid #f8bbd9;
        }

        /* Центральный виджет с полупрозрачностью */
        QWidget#centralWidget {
            background: rgba(255, 240, 245, 0.7);
            border-radius: 15px;
            margin: 10px;
        }

        /* Панель параметров с узором */
        QWidget[objectName^="left_panel"] {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 245, 248, 0.9), 
                stop:1 rgba(252, 228, 236, 0.9));
            border: 2px solid #f8bbd9;
            border-radius: 15px;
            padding: 15px;
            margin: 5px;
        }

        /* Стили для кнопок - как лепестки цветов */
        QPushButton {
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                stop:0 #ffcdd2, stop:0.7 #f48fb1, stop:1 #ad1457);
            color: white;
            border: 2px solid #f06292;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            min-width: 80px;
        }

        QPushButton:hover {
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.9,
                stop:0 #f8bbd9, stop:0.7 #f06292, stop:1 #880e4f);
            border: 2px solid #ec407a;
        }

        QPushButton:pressed {
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.7,
                stop:0 #f48fb1, stop:0.9 #ad1457);
        }

        /* Поля ввода - как бутоны */
        QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 8px 12px;
            border: 2px solid #f48fb1;
            border-radius: 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #fff0f5);
            color: #880e4f;
            font-weight: bold;
            selection-background-color: #f8bbd9;
        }

        QComboBox::drop-down {
            border: none;
            background: #f48fb1;
            border-radius: 10px;
            width: 20px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #880e4f;
            width: 0px;
            height: 0px;
        }

        /* Прогресс-бар - как стебель цветка */
        QProgressBar {
            border: 2px solid #f48fb1;
            border-radius: 10px;
            text-align: center;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fff0f5, stop:1 #fadadd);
            color: #880e4f;
            font-weight: bold;
        }

        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f48fb1, stop:0.5 #ec407a, stop:1 #ad1457);
            border-radius: 8px;
        }

        /* Метки - красивые надписи */
        QLabel {
            color: #880e4f;
            font-weight: bold;
            background: transparent;
            padding: 2px 5px;
        }

        QLabel[text="Параметры фрактала:"] {
            font-size: 14px;
            color: #ad1457;
            font-weight: bold;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent, stop:0.5 #f8bbd9, stop:1 transparent);
            padding: 8px;
            border-radius: 10px;
        }

        /* Меню-бар - как цветущая ветка */
        QMenuBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fce4ec, stop:0.5 #f8bbd9, stop:1 #fce4ec);
            color: #880e4f;
            font-weight: bold;
            border-bottom: 2px solid #f48fb1;
            padding: 5px;
        }

        QMenuBar::item {
            background: transparent;
            padding: 5px 15px;
            border-radius: 10px;
            margin: 0 2px;
        }

        QMenuBar::item:selected {
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                stop:0 #f8bbd9, stop:1 #f06292);
            color: white;
        }

        /* Выпадающие меню */
        QMenu {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fff0f5, stop:1 #fadadd);
            border: 2px solid #f48fb1;
            border-radius: 10px;
            padding: 5px;
        }

        QMenu::item {
            padding: 8px 25px 8px 20px;
            border-radius: 5px;
            color: #880e4f;
        }

        QMenu::item:selected {
            background: #f48fb1;
            color: white;
        }

        /* Статус-бар */
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fce4ec, stop:1 #f8bbd9);
            color: #880e4f;
            border-top: 2px solid #f48fb1;
        }

        /* Таблицы в галерее */
        QTableWidget {
            background: #fff0f5;
            alternate-background-color: #fce4ec;
            gridline-color: #f8bbd9;
            border: 2px solid #f48fb1;
            border-radius: 10px;
        }

        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f8bbd9;
            color: #880e4f;
        }

        QTableWidget::item:selected {
            background: #f48fb1;
            color: white;
        }

        QHeaderView::section {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8bbd9, stop:1 #f48fb1);
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }

        /* Полосы прокрутки */
        QScrollBar:vertical {
            background: #fce4ec;
            width: 15px;
            border-radius: 7px;
        }

        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f48fb1, stop:1 #ad1457);
            border-radius: 7px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ec407a, stop:1 #880e4f);
        }
        """

    @staticmethod
    def pink_flower_theme_with_pattern():
        theme = Themes.pink_flower_theme()
        # Добавляем фоновый узор через base64 (простой точечный узор)
        pattern = """
        QMainWindow {
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' 
            xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 30 Q60 20 70 30 Q80 40 70 50 Q60 60 50 50 Q40 60 30 50 
            Q20 40 30 30 Q40 20 50 30' fill='%23f8bbd9' opacity='0.1'/%3E%3C/svg%3E");
            background-repeat: repeat;
        }
        """
        return theme + pattern