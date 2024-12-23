import os
import pygame


class Settings():
    # Класс для хранения всех настроек игры
    def __init__(self):
        # Инициализируем настройки игры

        # Параметры игры
        self.game_active = False
        self.counter = 0
        self.best_score = 0
        self.skin_number = 0
        self.best_score_file = 'src/logic/best_score.txt'
        self.load_best_score()

        # Параметры экрана
        self.screen_width = pygame.display.set_mode((0, 0), pygame.FULLSCREEN).get_width()
        self.screen_height = pygame.display.set_mode((0, 0), pygame.FULLSCREEN).get_height()
        self.bg_color = (204, 204, 255)

        # Параметры попугая
        self.skins = [{'up': pygame.image.load('resources/images/cropped_parrot_yellow1.png'),
                       'down': pygame.image.load('resources/images/cropped_parrot_yellow.png')},
                      {'up': pygame.image.load('resources/images/cropped_parrot_green1.png'),
                       'down': pygame.image.load('resources/images/cropped_parrot_green.png')},
                       {'up': pygame.image.load('resources/images/cropped_parrot_blue1.png'),
                        'down': pygame.image.load('resources/images/cropped_parrot_blue.png')}]
        self.image_parot =  pygame.image.load('resources/images/cropped_parrot_blue.png')
        self.defolt_speed = 17
        self.decrease_speed = 1

        # Параметры колонны
        self.column_start_speed = 8
        self.column_hole = 300
        self.spawn_time = 1500
        self.image_bot = pygame.image.load('resources/images/Top_column.png')
        self.image_top = pygame.transform.rotate(self.image_bot, 180)
        self.image_mid = pygame.image.load('resources/images/longlong_mid.png')

    def load_best_score(self):
        # Загрузка лучшего результата из файла
        if os.path.exists(self.best_score_file):
            try:
                with open(self.best_score_file, 'r') as file:
                    self.best_score = int(file.read().strip())
            except ValueError:
                self.best_score = 0
        else:
            self.best_score = 0

    def save_best_score(self):
        # Сохранение лучшего результата в файл
        try:
            with open(self.best_score_file, 'w') as file:
                file.write(str(self.best_score))
        except IOError:
            pass

    def _reset(self):
        # Выводим все к начальным настройкам

        # Параметры игры
        self.game_active = False
        self.counter = 0

        # Параметры попугая
        self.defolt_speed = 17
        self.decrease_speed = 1

        # Параметры колонны
        self.column_start_speed = 8
        self.column_hole = 300
        self.spawn_time = 1500
