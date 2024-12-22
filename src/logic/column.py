import pygame
import random

from settings import Settings


class ColumnPair(pygame.sprite.Sprite):
    # Класс пары колонн с зазором
    def __init__(self, game):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.size_parot = self.settings.image_parot.get_width()

        # Загрузка изображений частей колонны
        self.image_bot = self.settings.image_bot
        self.image_top = self.settings.image_top
        self.image_mid = self.settings.image_mid

        # Список для хранения прямоугольников частей колонны
        self.parts = []

        # Прошёл ли попугай колонну
        self.passed = False

        # Задаем расположение колонн
        gap_y = random.randint(0, self.screen_rect.height -  int(self.settings.column_hole) - 100)

        # Строим верхнюю и нижнюю колонну
        top_column_height = gap_y
        self.create_column_part(self.image_top, self.screen_rect.width + 100, top_column_height, 'top')
        mid_y = top_column_height
        self.create_column_part(self.image_mid, self.screen_rect.width + 108, mid_y, 'top_mid')
        bot_column_y = gap_y + self.settings.column_hole
        self.create_column_part(self.image_bot, self.screen_rect.width + 100, bot_column_y, 'bottom')
        mid_y = bot_column_y + self.image_bot.get_height()
        self.create_column_part(self.image_mid, self.screen_rect.width + 108, mid_y, 'mid')

    def create_column_part(self, image, x, y, position):
        # Создает часть колонны и добавляет ее в список частей
        part_rect = image.get_rect()
        part_rect.x = x
        if position == 'top_mid':
            part_rect.bottom = y
        else:
            part_rect.y = y
        self.parts.append((image, part_rect))

    def is_near_parrot(self, parrot_collision_zone):
        # Проверяет, находится ли какая-либо часть колонн внутри зоны вокруг попугая
        if ((self.screen_rect.center[0] + self.size_parot < self.parts[0][1].x) or (self.parts[0][1].x < self.screen_rect.center[0] - self.size_parot)):
            return False
        for _, rect in self.parts:
            
            if rect.colliderect(parrot_collision_zone):
                return True
        return False

    def update(self, parrot):
        # Обновляет позиции всех частей колонны
        self.x = float(self.parts[0][1].x)
        speed = self.settings.column_start_speed
        self.x -= speed

        # Удаляем части колонны, если они вышли за экран
        if self.x < -20:
            self.kill()
        
        for _, rect in self.parts:
            rect.x = int(self.x)

        # Обновляем очки
        if not self.passed and rect.right < parrot.rect.left:
            self.passed = True
            self.settings.counter += 1

        
        

    def blitme(self):
        # Отображает все части колонн на экране
        for image, rect in self.parts:
            self.screen.blit(image, rect)
