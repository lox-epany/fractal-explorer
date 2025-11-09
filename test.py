from src.core.fractal_engine import FractalEngine

engine = FractalEngine()
result = engine.calculate_mandelbrot(0, 0, 1.0, 100, 100, 100)
print(result)