import sqlite3
import os
from pathlib import Path
import io


class Database:
    def __init__(self, db_path="fractal_explorer.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def init_db(self):
        """Инициализировать БД"""
        if not os.path.exists(self.db_path):
            self.create_tables()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        """Создать таблицы из schema.sql"""
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r') as f:
            sql = f.read()

        conn = sqlite3.connect(self.db_path)
        conn.executescript(sql)
        conn.commit()
        conn.close()

    def save_to_gallery(self, name, fractal_type, params, thumbnail=None):
        """Сохранить фрактал в галерею"""
        cursor = self.conn.cursor()

        thumbnail_blob = None
        if thumbnail:
            img_bytes = io.BytesIO()
            thumbnail.save(img_bytes, format='PNG')
            thumbnail_blob = img_bytes.getvalue()

        cursor.execute("""
            INSERT INTO gallery 
            (name, description, fractal_type, xmin, xmax, ymin, ymax, 
             iterations, c_real, c_imag, thumbnail, render_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, "", fractal_type,
            params['xmin'], params['xmax'], params['ymin'], params['ymax'],
            params['iterations'], params.get('c_real'), params.get('c_imag'),
            thumbnail_blob, params.get('render_time', 0)
        ))

        self.conn.commit()

    def load_gallery(self):
        """Загрузить все фракталы из галереи"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM gallery ORDER BY created_at DESC")
        return cursor.fetchall()

    def load_presets(self):
        """Загрузить предустановки"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM presets")
        return cursor.fetchall()

    def add_to_history(self, fractal_type, params, render_time):
        """Добавить в историю"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO history 
            (fractal_type, xmin, xmax, ymin, ymax, iterations, render_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fractal_type,
            params['xmin'], params['xmax'], params['ymin'], params['ymax'],
            params['iterations'], render_time
        ))
        self.conn.commit()

    def close(self):
        """Закрыть соединение"""
        if self.conn:
            self.conn.close()
