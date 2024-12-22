import pygame

from settings import Settings


class Parrot():
    # Класс попугая
    def __init__(self, game):
        # Инициализируем попугая
        self.settings = Settings()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Загружаем изображение попугая и получаем границы
        self.image = self.settings.image_parot
        # Создаем маску изображения попугая для точных границ
        self.bird_mask = pygame.mask.from_surface(self.image)
        self.rect = self.bird_mask.get_bounding_rects()[0]

        # Задаем позицию по горизонтали в которой всегда будет находиться попугай
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)

        # Задаем начальную скорость
        self.speed = 0

    def update(self) -> None:
        # Управляем полетом птицы
        # Обновляем скорость (гравитация или любое другое изменение скорости)
        self.y = float(self.rect.y)
        self.speed -= self.settings.decrease_speed
        self.y -= self.speed

        self.check_rect()

        # Обновляем позицию `rect` на основе `y`
        self.rect.y = int(self.y)

    def check_rect(self) -> None:
        # Проверка верхней границы экрана
        if self.y <= 0:
            self.y = 0
            # Останавливаем движение вверх при достижении верхней границы
            self.speed = 0

        # Проверка нижней границы экрана
        elif self.y + self.rect.height >= self.screen_rect.height:
            self.y = self.screen_rect.height - self.rect.height
            # Останавливаем падение при достижении нижней границы
            self.speed = 0

    def blitme(self) -> None:
        # Рисует птицу
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
        self.screen.blit(self.image, self.rect)