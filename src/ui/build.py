#!/usr/bin/env python3
"""
Скрипт для сборки Fractal Explorer в исполняемый файл
Поддерживает Windows, Linux и macOS
"""

import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path


def get_platform_specifics():
    """Определяет параметры для текущей платформы"""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if system == "windows":
        ext = ".exe"
        icon = "icon.ico"
        add_data_sep = ";"
    else:
        ext = ""
        icon = "icon.ico" if system == "darwin" else "icon.png"
        add_data_sep = ":"

    return {
        "system": system,
        "arch": arch,
        "ext": ext,
        "icon": icon,
        "add_data_sep": add_data_sep,
        "spec_name": f"fractal_explorer_{system}_{arch}"
    }


def create_icon():
    """Создает иконку если её нет"""
    icon_path = Path("icon.ico")
    if not icon_path.exists():
        print("⚠️  Иконка не найдена. Будет использована стандартная иконка PyQt.")
        return None
    return str(icon_path)


def clean_build_dirs():
    """Очищает предыдущие сборки"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Очищена папка: {dir_name}")


def create_spec_file(platform_info):
    """Создает .spec файл для PyInstaller"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Добавляем пути к модулям
sys.path.append(str(Path(__name__).parent))

a = Analysis(
    ['src/ui/main_window.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/resources/themes.py', 'src/resources'),
        ('src/ui/canvas.py', 'src/ui'),
        ('src/ui/gallery_dialog.py', 'src/ui'),
        ('src/ui/color_dialog.py', 'src/ui'),
        ('src/core/worker.py', 'src/core'),
        ('src/db/database.py', 'src/db'),
    ],
    hiddenimports=[
        'numpy',
        'numpy.core._dtype_ctypes',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Исключаем ненужные модули для уменьшения размера
excludes = ['tkinter', 'email', 'http', 'urllib', 'xml', 'pydoc']
for exclude in excludes:
    if exclude in a.dependencies:
        a.dependencies.remove(exclude)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='fractal_explorer{platform_info["ext"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip={platform_info["system"] != "windows"},
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={f"'{platform_info['icon']}'" if platform_info['icon'] and os.path.exists(platform_info['icon']) else None},
)
'''

    spec_filename = f"{platform_info['spec_name']}.spec"
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)

    return spec_filename


def build_application(spec_file):
    """Собирает приложение используя PyInstaller"""
    try:
        result = subprocess.run([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            spec_file
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Сборка завершена успешно!")
            return True
        else:
            print(f"❌ Ошибка сборки: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Ошибка при запуске PyInstaller: {e}")
        return False


def optimize_build():
    """Оптимизирует собранное приложение"""
    dist_dir = Path("../../dist")
    if not dist_dir.exists():
        return

    # Удаляем ненужные файлы
    unnecessary_files = [
        "qt.conf",
        "PyQt6/Qt6/bin",
        "PyQt6/Qt6/translations",
        "PyQt6/Qt6/qml",
    ]

    for file_pattern in unnecessary_files:
        file_path = dist_dir / "fractal_explorer" / file_pattern
        if file_path.exists():
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()


def create_launch_scripts():
    """Создает скрипты для запуска на разных платформах"""
    system = platform.system().lower()

    if system == "windows":
        # BAT файл для Windows
        bat_content = '''@echo off
chcp 65001 > nul
echo Запуск Fractal Explorer...
dist\\fractal_explorer.exe
pause
'''
        with open("run_fractal_explorer.bat", "w", encoding="utf-8") as f:
            f.write(bat_content)
        print("📝 Создан BAT файл для запуска: run_fractal_explorer.bat")

    elif system in ["linux", "darwin"]:
        # Shell скрипт для Linux/macOS
        script_content = '''#!/bin/bash
echo "Запуск Fractal Explorer..."
cd "$(dirname "$0")"
./dist/fractal_explorer
'''
        script_name = "run_fractal_explorer.sh"
        with open(script_name, "w", encoding="utf-8") as f:
            f.write(script_content)

        # Делаем скрипт исполняемым
        os.chmod(script_name, 0o755)
        print(f"📝 Создан shell скрипт для запуска: {script_name}")


def main():
    """Основная функция сборки"""
    print("🚀 Запуск сборки Fractal Explorer...")
    print(f"📋 Платформа: {platform.system()} {platform.machine()}")

    # Проверяем зависимости
    try:
        import PyQt6
        import numpy
        print("✅ Все зависимости найдены")
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости: {e}")
        sys.exit(1)

    # Получаем информацию о платформе
    platform_info = get_platform_specifics()
    print(f"🔧 Целевая платформа: {platform_info['system']}/{platform_info['arch']}")

    # Очищаем предыдущие сборки
    clean_build_dirs()

    # Создаем spec файл
    print("📄 Создание конфигурации сборки...")
    spec_file = create_spec_file(platform_info)

    # Запускаем сборку
    print("🔨 Запуск PyInstaller...")
    if build_application(spec_file):
        # Оптимизируем сборку
        optimize_build()

        # Создаем скрипты запуска
        create_launch_scripts()

        print(f"🎉 Сборка завершена!")
        print(f"📁 Исполняемый файл: dist/fractal_explorer{platform_info['ext']}")
        print(f"💾 Размер приложения: {get_folder_size('../../dist')} МБ")
    else:
        print("💥 Сборка не удалась!")
        sys.exit(1)


def get_folder_size(folder_path):
    """Возвращает размер папки в МБ"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return round(total_size / (1024 * 1024), 2)


if __name__ == "__main__":
    main()