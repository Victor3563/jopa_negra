import sys
import pygame

from settings import Settings
from parrot import Parrot
from column import ColumnPair, Column
from button import Button

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
        self.play_button = Button(self,"Play")

        # Список для хранения всех колонн
        self.columns = set()
        self.last_spawn_time = pygame.time.get_ticks()  # Время последнего спауна

        self.space_pressed = False

        
    def run_game(self) -> None:
        """Запуск игры"""
        while True:
            self.check_events()
            if self.settings.game_active:
                self.spawn_columns()
                self.check_collisions() 
                self.update_screen()
                    #кнопка play
            if not self.settings.game_active:
                self.play_button.draw_buttom()

            #Отображаем экран
            pygame.display.flip()


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

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.settings.game_active:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mous_pos):
        """Запускаем новую игру при нажатии кнопки"""
        if self.play_button.rect.collidepoint(mous_pos):
            self.settings._reset()
            for column_pair in self.columns:
                column_pair.empty()
            self.parrot.rect.center = self.parrot.screen_rect.center
            self.settings.game_active = True

    def check_collisions(self):
        """Проверка на столкновение попугая с колоннами"""
        # Проверяем пересечение rect попугая с rect каждой колонны в колоннах
        for column_pair in self.columns:
            if pygame.sprite.spritecollideany(self.parrot,column_pair):
                print("Столкновение!")
                self.settings.game_active = False


    def update_screen(self):
        """Перерисовываем экран и выводим его"""
        #Перерисовываем экран
        self.screen.fill(self.settings.bg_color)
        self.parrot.update()
        
        self.parrot.blitme()
        # Отображаем все колонны из группы колонн
        for column_pair in self.columns:
            column_pair.update()
            column_pair.blitme()



    def spawn_columns(self):
        """Спавнит новую пару колонн каждые n секунд"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.settings.spawn_time:  # Проверка интервала
            new_column_pair = ColumnPair(self)
            self.columns.add(new_column_pair)  # Добавляем новую колонну
            self.last_spawn_time = current_time  # Обновляем время последнего спауна


if __name__ == '__main__':
    game = FlappyParrot()
    game.run_game()