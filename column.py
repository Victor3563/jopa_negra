import pygame
import random

from settings import Settings

class Column(pygame.sprite.Sprite):
    """Класс колон"""
    def __init__(self,game,image, x, y):
        super().__init__() 
        """Инициализируем колонну"""
        self.settings = Settings()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Перемещаем колонну влево"""
        self.rect.x -= self.settings.column_start_speed

        # Удаляем колонну, если она вышла за экран
        if self.rect.right < 0:
            self.settings.column_hole *= 0.99
            self.settings.column_start_speed *= 1.01
            self.settings.counter += 1
            self.kill()


class ColumnPair(pygame.sprite.Group):
    """Класс пары колонн с зазором"""
    def __init__(self, game):
        super().__init__()
        self.settings = Settings()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Загрузка изображений частей колонны
        self.image_bot = pygame.image.load('images/Top_column.png')
        self.image_top = pygame.transform.rotate(self.image_bot, 180)
        self.image_mid = pygame.image.load('images/mid_column.png')

        #Задаем расположение колон
        gap_y = random.randint(0, self.screen_rect.height - self.settings.column_hole)

        #Строим верхнюю колонну
        top_column_height = gap_y
        self.create_column_part(game, self.image_top, self.screen_rect.width+100, top_column_height, None, 'top')

        # Средние части верхней колонны + подгон положения по х так как столб не однороден по ширине
        mid_y = top_column_height - self.image_top.get_height()+4
        while mid_y > -self.image_top.get_height():
            self.create_column_part(game, self.image_mid, self.screen_rect.width+108, mid_y)
            mid_y -= self.image_mid.get_height()

        # Нижняя колонна
        bot_column_y = gap_y + self.settings.column_hole
        self.create_column_part(game, self.image_bot, self.screen_rect.width+100, bot_column_y, None, 'bottom')

        # Средние части нижней колонны + подгон положения по х так как столб не однороден по ширине
        mid_y = bot_column_y + self.image_bot.get_height()
        while mid_y < self.screen_rect.height + self.image_top.get_height():
            self.create_column_part(game, self.image_mid, self.screen_rect.width + 108, mid_y)
            mid_y += self.image_mid.get_height()

    def create_column_part(self, game, image, x, start_y, height=None, position=None):
        """Создает часть колонны и добавляет ее в группу"""
        # Создаем объект на основе части колонны (top, bot или mid)
        if position == 'top':
            self.add(Column(game, image, x, start_y))
        elif position == 'bottom':
            self.add(Column(game, image, x, start_y))
        else:
            # Создаем центральные части колонн
            mid_column = Column(game, image, x, start_y)
            self.add(mid_column)

    def update(self):
        """Обновляет позиции всех колонн"""
        for sprite in self.sprites():
            sprite.update()

    def blitme(self):
        """Отображает все колонны группы на экране"""
        for sprite in self.sprites():
            self.screen.blit(sprite.image, sprite.rect)
