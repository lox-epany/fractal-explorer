import sqlite3
import os


class Database:
    def __init__(self, db_path="fractals.db"):
        self.db_path = db_path
        self._init_db()
        self._add_default_presets()

    def _init_db(self):
        """Инициализация БД и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            # Читаем и выполняем schema.sql
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            conn.executescript(schema_sql)
            conn.commit()

    def save_preset(self, name, fractal_type, center_x, center_y, zoom,
                    max_iterations, c_real=None, c_imag=None):
        """Сохраняет пресет фрактала в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO fractal_presets 
                (name, fractal_type, center_x, center_y, zoom, max_iterations, c_real, c_imag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, fractal_type, center_x, center_y, zoom, max_iterations, c_real, c_imag))
            conn.commit()
            return cursor.lastrowid

    def load_presets(self, fractal_type=None):
        """Загружает все пресеты (или только определенного типа)"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Чтобы получать dict-like объекты
            cursor = conn.cursor()

            if fractal_type:
                cursor.execute('''
                    SELECT * FROM fractal_presets 
                    WHERE fractal_type = ? 
                    ORDER BY created_at DESC
                ''', (fractal_type,))
            else:
                cursor.execute('''
                    SELECT * FROM fractal_presets 
                    ORDER BY created_at DESC
                ''')

            return [dict(row) for row in cursor.fetchall()]

    def delete_preset(self, preset_id):
        """Удаляет пресет по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM fractal_presets WHERE id = ?', (preset_id,))
            conn.commit()

    def save_image(self, preset_id, image_data, width, height):
        """Сохраняет изображение фрактала в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO fractal_images (preset_id, image_data, width, height)
                VALUES (?, ?, ?, ?)
            ''', (preset_id, image_data, width, height))
            conn.commit()
            return cursor.lastrowid

    def load_images(self, preset_id):
        """Загружает изображения для пресета"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM fractal_images 
                WHERE preset_id = ? 
                ORDER BY created_at DESC
            ''', (preset_id,))
            return [dict(row) for row in cursor.fetchall()]

    def _add_default_presets(self):
        """Добавляет стандартные пресеты при инициализации БД"""
        presets = [
            # Мандельброт пресеты
            {
                'name': 'Классический Мандельброт',
                'fractal_type': 'Mandelbrot',
                'center_x': -0.5, 'center_y': 0.0,
                'zoom': 1.0, 'max_iterations': 256
            },
            {
                'name': 'Мандельброт - спирали',
                'fractal_type': 'Mandelbrot',
                'center_x': -0.743, 'center_y': 0.126,
                'zoom': 200.0, 'max_iterations': 512
            },
            {
                'name': 'Мандельброт - острова',
                'fractal_type': 'Mandelbrot',
                'center_x': -1.250, 'center_y': 0.020,
                'zoom': 80.0, 'max_iterations': 300
            },

            # Жюлиа пресеты (красивые!)
            {
                'name': 'Жюлиа - Дракон',
                'fractal_type': 'Julia',
                'center_x': 0.0, 'center_y': 0.0,
                'zoom': 1.2, 'max_iterations': 300,
                'c_real': -0.7269, 'c_imag': 0.1889
            },
            {
                'name': 'Жюлиа - Кружева',
                'fractal_type': 'Julia',
                'center_x': 0.0, 'center_y': 0.0,
                'zoom': 1.5, 'max_iterations': 400,
                'c_real': -0.4, 'c_imag': 0.6
            },
            {
                'name': 'Жюлиа - Снежинки',
                'fractal_type': 'Julia',
                'center_x': 0.0, 'center_y': 0.0,
                'zoom': 1.8, 'max_iterations': 350,
                'c_real': 0.285, 'c_imag': 0.01
            },
            {
                'name': 'Жюлиа - Огненный цветок',
                'fractal_type': 'Julia',
                'center_x': 0.0, 'center_y': 0.0,
                'zoom': 1.3, 'max_iterations': 280,
                'c_real': -0.8, 'c_imag': 0.156
            },
            {
                'name': 'Жюлиа - Космическая спираль',
                'fractal_type': 'Julia',
                'center_x': 0.0, 'center_y': 0.0,
                'zoom': 1.6, 'max_iterations': 320,
                'c_real': -0.70176, 'c_imag': -0.3842
            }
        ]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Проверяем, есть ли уже пресеты (чтобы не дублировать)
            cursor.execute("SELECT COUNT(*) FROM fractal_presets")
            count = cursor.fetchone()[0]

            if count == 0:
                for preset in presets:
                    cursor.execute('''
                        INSERT INTO fractal_presets 
                        (name, fractal_type, center_x, center_y, zoom, max_iterations, c_real, c_imag)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        preset['name'], preset['fractal_type'],
                        preset['center_x'], preset['center_y'],
                        preset['zoom'], preset['max_iterations'],
                        preset.get('c_real'), preset.get('c_imag')
                    ))

                conn.commit()
                print("✅ Добавлены стандартные пресеты фракталов")