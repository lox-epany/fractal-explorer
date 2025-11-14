from src.db.database import Database


def test_database():
    db = Database("test.db")

    # Тест сохранения пресета
    preset_id = db.save_preset(
        name="Тестовый Мандельброт",
        fractal_type="Mandelbrot",
        center_x=-0.5,
        center_y=0,
        zoom=1.0,
        max_iterations=100
    )
    print(f"Сохранен пресет с ID: {preset_id}")

    # Тест загрузки пресетов
    presets = db.load_presets()
    print("Сохраненные пресеты:")
    for preset in presets:
        print(f"- {preset['name']} ({preset['fractal_type']})")

    # Тест удаления
    db.delete_preset(preset_id)
    print("Пресет удален")


if __name__ == "__main__":
    test_database()