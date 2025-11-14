-- Таблица для сохранения пресетов фракталов
CREATE TABLE IF NOT EXISTS fractal_presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    fractal_type TEXT NOT NULL CHECK(fractal_type IN ('Mandelbrot', 'Julia')),
    center_x REAL NOT NULL,
    center_y REAL NOT NULL,
    zoom REAL NOT NULL,
    max_iterations INTEGER NOT NULL,
    c_real REAL DEFAULT NULL,  -- Только для Julia
    c_imag REAL DEFAULT NULL,  -- Только для Julia
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для сохранения изображений фракталов
CREATE TABLE IF NOT EXISTS fractal_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preset_id INTEGER,
    image_data BLOB NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (preset_id) REFERENCES fractal_presets (id) ON DELETE CASCADE
);