import sqlite3
import os
from datetime import datetime
from PyQt6.QtGui import QImage
import json


class Database:
    def __init__(self, db_path="fractals.db"):
        self.db_path = db_path
        self._init_db()

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