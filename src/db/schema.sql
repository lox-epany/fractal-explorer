CREATE TABLE IF NOT EXISTS gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    fractal_type TEXT NOT NULL,
    xmin REAL NOT NULL,
    xmax REAL NOT NULL,
    ymin REAL NOT NULL,
    ymax REAL NOT NULL,
    iterations INTEGER NOT NULL,
    c_real REAL,
    c_imag REAL,
    thumbnail BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    render_time REAL
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fractal_type TEXT NOT NULL,
    xmin REAL,
    xmax REAL,
    ymin REAL,
    ymax REAL,
    iterations INTEGER,
    render_time REAL,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    fractal_type TEXT NOT NULL,
    xmin REAL,
    xmax REAL,
    ymin REAL,
    ymax REAL,
    iterations INTEGER,
    c_real REAL,
    c_imag REAL
);

INSERT INTO presets (name, fractal_type, xmin, xmax, ymin, ymax, iterations, c_real, c_imag) VALUES
('Full Mandelbrot', 'mandelbrot', -2.5, 1.0, -1.25, 1.25, 256, NULL, NULL),
('Mandelbrot Zoom 1', 'mandelbrot', -0.8, -0.4, -0.2, 0.2, 256, NULL, NULL),
('Julia Set 1', 'julia', -2.0, 2.0, -1.5, 1.5, 256, -0.7, 0.27015);
