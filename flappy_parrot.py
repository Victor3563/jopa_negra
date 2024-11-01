import sys
import pygame

from settings import Settings
from parrot import Parrot

class FlappyParrot:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self) -> None:
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Flappy Parrot")

        self.parrot = Parrot(self)

        self.space_pressed = False

        
    def run_game(self) -> None:
        """Запуск игры"""
        while True:
            self.check_events()
            self.update_screen()

    def check_events(self):
        """Обрабатываем нажатия клавишь"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.space_pressed:
                    self.parrot.speed = self.settings.defolt_speed
                    self.space_pressed = True
                elif event.key == pygame.K_q:
                    sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = False


    def update_screen(self):
        """Перерисовываем экран и выводим его"""
        #Перерисовываем экран
        self.screen.fill(self.settings.bg_color)
        self.parrot.update()
        self.parrot.blitme()

        #Отображаем экран
        pygame.display.flip()


if __name__ == '__main__':
    game = FlappyParrot()
    game.run_game()