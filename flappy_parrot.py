import sys
import pygame

from settings import Settings
from parrot import Parrot
from column import ColumnPair
from button import Button

class FlappyParrot:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self) -> None:
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (0,0), pygame.FULLSCREEN
        )
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width

        pygame.display.set_caption("Flappy Parrot")

        self.parrot = Parrot(self)
        self.play_button = Button(self,"Play")

        # Список для хранения всех колонн
        self.columns = pygame.sprite.Group()
        self.last_spawn_time = pygame.time.get_ticks()  # Время последнего спауна

        self.space_pressed = False
        
        self.clock = pygame.time.Clock()
        
    def run_game(self) -> None:
        """Запуск игры"""
        while True:
            
            self.check_events()
            self.clock.tick(40)
            if self.settings.game_active:
                self.spawn_columns()
                self.check_collisions() 
                self.update_screen()
                    #кнопка play
            if not self.settings.game_active:
                pygame.mouse.set_visible(True)
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
            self.columns.empty()
            self.parrot.rect.center = self.parrot.screen_rect.center
            self.settings.game_active = True
            pygame.mouse.set_visible(False)

    def check_collisions(self):
        """Проверка на столкновение попугая с колоннами"""
        # Проверяем пересечение rect попугая с rect каждой колонны в колоннах  # Проверяем только колонны вблизи попугая
        parrot_collision_zone = self.parrot.rect  # Зона столкновения попугая
        for column_pair in self.columns:
            if column_pair.is_near_parrot(parrot_collision_zone):
                print("Столкновение!")
                self.settings.game_active = False
                break


    def update_screen(self):
        """Перерисовываем экран и выводим его"""
        #Перерисовываем экран
        self.screen.fill(self.settings.bg_color)
        self.parrot.update()
        
        self.parrot.blitme()
        # Отображаем все колонны из группы колонн
        self.columns.update()
        for column_pair in self.columns:
            column_pair.blitme()



    def spawn_columns(self):
        """Спавнит новую пару колонн каждые n секунд"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.settings.spawn_time:  # Проверка интервала
            new_column_pair = ColumnPair(self)
            self.columns.add(new_column_pair)  # Добавляем новую колонну
            self.last_spawn_time = current_time  # Обновляем время последнего спауна
            self.settings.column_hole *= 0.97
            self.settings.column_start_speed *= 1.03
            print((self.settings.column_hole))


if __name__ == '__main__':
    game = FlappyParrot()
    game.run_game()