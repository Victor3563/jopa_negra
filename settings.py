class Settings():
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализируем настройки игры"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (200,200,230)

        #Параметры попугая
        self.defolt_speed = 4
        self.decrease_speed = 0.08