import numpy as np
from PyQt6.QtGui import QColor


class ColorSchemes:
    @staticmethod
    def get_scheme(scheme_name):
        schemes = {
            "classic": ColorSchemes.classic_scheme(),
            "rainbow": ColorSchemes.rainbow_scheme(),
            "fire": ColorSchemes.fire_scheme(),
            "ocean": ColorSchemes.ocean_scheme(),
            "forest": ColorSchemes.forest_scheme(),
            "pink_dream": ColorSchemes.pink_dream_scheme(),
            "neon": ColorSchemes.neon_scheme(),
            "sunset": ColorSchemes.sunset_scheme()
        }
        return schemes.get(scheme_name, ColorSchemes.classic_scheme())

    @staticmethod
    def classic_scheme():
        """Классическая сине-белая схема"""
        colors = []
        for i in range(256):
            if i < 64:
                r, g, b = 0, 0, i * 4
            elif i < 128:
                r, g, b = 0, (i - 64) * 4, 255
            elif i < 192:
                r, g, b = (i - 128) * 4, 255, 255
            else:
                r, g, b = 255, 255, 255
            colors.append((r, g, b))
        return colors

    @staticmethod
    def rainbow_scheme():
        """Радужная схема"""
        colors = []
        for i in range(256):
            # Плавный переход через все цвета радуги
            hue = (i / 256.0) * 360
            color = QColor.fromHsv(int(hue), 255, 255)
            colors.append((color.red(), color.green(), color.blue()))
        return colors

    @staticmethod
    def fire_scheme():
        """Огненная схема"""
        colors = []
        for i in range(256):
            if i < 85:
                r = i * 3
                g = 0
                b = 0
            elif i < 170:
                r = 255
                g = (i - 85) * 3
                b = 0
            else:
                r = 255
                g = 255
                b = (i - 170) * 3
            colors.append((r, g, b))
        return colors

    @staticmethod
    def ocean_scheme():
        """Океанская схема"""
        colors = []
        for i in range(256):
            # От темно-синего к бирюзовому и белому
            if i < 128:
                r = 0
                g = i * 2
                b = 128 + i
            else:
                r = (i - 128) * 2
                g = 255
                b = 255
            colors.append((r, g, b))
        return colors

    @staticmethod
    def forest_scheme():
        """Лесная схема"""
        colors = []
        for i in range(256):
            # От темно-зеленого к салатовому и белому
            if i < 100:
                r = 0
                g = 50 + i * 2
                b = 0
            elif i < 200:
                r = (i - 100) * 2
                g = 255
                b = (i - 100)
            else:
                r = 255
                g = 255
                b = 200 + (i - 200)
            colors.append((r, g, b))
        return colors

    @staticmethod
    def pink_dream_scheme():
        """Розовый шёлк - очень мягкий и элегантный 🌸
        надеюсь вам очень понравиться этот цвет, лично я ослеп"""
        colors = []
        for i in range(256):
            # Очень плавные переходы как у шёлка
            if i < 90:
                # От кремово-розового к нежно-розовому
                t = i / 90.0
                r = 245 + int(10 * t)  # 245 → 255
                g = 225 + int(15 * t)  # 225 → 240
                b = 235 + int(15 * t)  # 235 → 250
            elif i < 160:
                # Нежно-розовый → сиренево-розовый
                t = (i - 90) / 70.0
                r = 255
                g = 240 - int(25 * t)  # 240 → 215
                b = 250 - int(20 * t)  # 250 → 230
            elif i < 220:
                # Сиренево-розовый → лавандовый
                t = (i - 160) / 60.0
                r = 255 - int(20 * t)  # 255 → 235
                g = 215 - int(10 * t)  # 215 → 205
                b = 230 + int(25 * t)  # 230 → 255
            else:
                # К белому с лавандовым оттенком
                t = (i - 220) / 36.0
                r = 235 + int(20 * t)  # 235 → 255
                g = 205 + int(50 * t)  # 205 → 255
                b = 255

            colors.append((r, g, b))
        return colors

    @staticmethod
    def neon_scheme():
        """Неоновая схема"""
        colors = []
        for i in range(256):
            # Яркие неоновые цвета
            phase = (i / 256.0) * 3.14159 * 2
            r = int(128 + 127 * np.sin(phase))
            g = int(128 + 127 * np.sin(phase + 2.094))
            b = int(128 + 127 * np.sin(phase + 4.188))
            colors.append((r, g, b))
        return colors

    @staticmethod
    def sunset_scheme():
        """Схема заката"""
        colors = []
        for i in range(256):
            # От оранжевого к красному и фиолетовому
            if i < 100:
                r = 255
                g = 100 + i
                b = 0
            elif i < 180:
                r = 255
                g = 200 - (i - 100)
                b = (i - 100) * 3
            else:
                r = 255 - (i - 180)
                g = 50
                b = 255
            colors.append((r, g, b))
        return colors

    @staticmethod
    def custom_scheme(colors_list):
        """Кастомная схема из списка цветов"""
        if len(colors_list) < 2:
            return ColorSchemes.classic_scheme()

        # Интерполяция между цветами
        colors = []
        steps = 256
        segments = len(colors_list) - 1
        steps_per_segment = steps // segments

        for seg in range(segments):
            start_color = colors_list[seg]
            end_color = colors_list[seg + 1]

            for i in range(steps_per_segment):
                t = i / steps_per_segment
                r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
                colors.append((r, g, b))

        # Добавляем оставшиеся шаги
        while len(colors) < 256:
            colors.append(colors_list[-1])

        return colors[:256]