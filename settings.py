class Settings():
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализируем настройки игры"""
        #Параметры игры
        self.game_active = False
        self.counter = 0
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (200,200,230)

        #Параметры попугая
        self.defolt_speed = 4
        self.decrease_speed = 0.08

        #Параметры колонны
        self.column_start_speed = 1
        self.column_hole = 300
        self.spawn_time = 5000

    def _reset(self):
        """Выводим все к начальным настройкам"""
        #Параметры игры
        self.game_active = False
        self.counter = 0
         #Параметры попугая
        self.defolt_speed = 4
        self.decrease_speed = 0.08

        #Параметры колонны
        self.column_start_speed = 1
        self.column_hole = 300
        self.spawn_time = 5000
