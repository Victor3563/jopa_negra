import sys
import pygame

from src.logic.settings import Settings
from src.logic.parrot import Parrot
from src.logic.column import ColumnPair
from src.logic.button import Button


class FlappyParrot:
    # Класс для управления ресурсами и поведением игры
    def __init__(self) -> None:
        # Инициализирует игру и создает игровые ресурсы
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Flappy Parrot")
        self.parrot = Parrot(self)
        self.play_button = Button(self, "Play\nPress Enter", 0, not_one_str=True)
        self.customize_button = Button(self, "Customize", 1)
        self.quit_button = Button(self, "Quit", 2)

        # Список для хранения всех колонн
        self.columns = pygame.sprite.Group()

        # Время последнего спауна
        self.last_spawn_time = pygame.time.get_ticks()
        self.space_pressed = False
        self.clock = pygame.time.Clock()

    def run_game(self) -> None:
        # Запуск игры
        while True:
            self.check_events()
            self.clock.tick(40)
            if self.settings.game_active:
                self.spawn_columns()
                self.check_collisions()
                self.update_screen()

            # кнопки
            if not self.settings.game_active:
                pygame.mouse.set_visible(True)
                self.play_button.draw_button(not_one_str=True)
                self.customize_button.draw_button()
                self.quit_button.draw_button()
            # Отображаем экран

            pygame.display.flip()

    def check_events(self):
        # Обрабатываем нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.space_pressed:
                    self.parrot.speed = self.settings.defolt_speed
                    self.settings.decrease_speed = 1
                    self.parrot.image = self.settings.image_parot2
                    self.space_pressed = True
                elif event.key == pygame.K_RETURN and not self.settings.game_active:
                    self.settings._reset()
                    self.columns.empty()
                    self.parrot.rect.center = self.parrot.screen_rect.center
                    self.settings.game_active = True
                    pygame.mouse.set_visible(False)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.parrot.image = self.settings.image_parot
                    self.space_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.settings.game_active:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_customize_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_play_button(self, mous_pos):
        # Запускаем новую игру при нажатии кнопки
        if self.play_button.rect.collidepoint(mous_pos):
            self.settings._reset()
            self.columns.empty()
            self.parrot.rect.center = self.parrot.screen_rect.center
            self.settings.game_active = True
            pygame.mouse.set_visible(False)

    def _check_customize_button(self, mous_pos):
        # Выходим из игры при нажатии кнопки
        if self.customize_button.rect.collidepoint(mous_pos):
            pass

    def _check_quit_button(self, mous_pos):
        # Выходим из игры при нажатии кнопки
        if self.quit_button.rect.collidepoint(mous_pos):
            sys.exit()

    def check_collisions(self):
        # Проверка на столкновение попугая с колоннами
        # Проверяем пересечение rect попугая с rect каждой колонны в колоннах
        # Проверяем только колонны вблизи попугая
        parrot_collision_zone = self.parrot.rect  # Зона столкновения попугая
        for column_pair in self.columns:
            if column_pair.is_near_parrot(parrot_collision_zone):
                self.settings.game_active = False
                break

    def display_score(self):
        # Выводим кол-во очков
        font = pygame.font.SysFont(None, 48)
        score_image = font.render(f'Score: {self.settings.counter}', True, (0, 0, 0))
        score_rect = score_image.get_rect()
        score_rect.centerx = self.screen.get_rect().centerx
        # Отступ от верхней границы экрана
        score_rect.top = 20
        self.screen.blit(score_image, score_rect)

    def update_screen(self):
        # Перерисовываем экран и выводим его
        # Перерисовываем экран
        self.screen.fill(self.settings.bg_color)
        self.parrot.update()
        self.parrot.blitme()

        # Отображаем все колонны из группы колонн
        self.columns.update(self.parrot)
        for column_pair in self.columns:
            column_pair.update(self.parrot)
            column_pair.blitme()

        # Отображение очков
        self.display_score()

    def spawn_columns(self):
        # Спавнит новую пару колонн каждые n секунд
        current_time = pygame.time.get_ticks()
        # Проверка интервала
        if current_time - self.last_spawn_time >= self.settings.spawn_time:
            new_column_pair = ColumnPair(self)

            # Добавляем новую колонну
            self.columns.add(new_column_pair)
            self.last_spawn_time = current_time

            # Обновляем время последнего спауна
            if (self.settings.column_hole >= 280):
                self.settings.column_hole *= 0.97
            self.settings.column_start_speed *= 1.03
            if (self.settings.spawn_time >= 1150):
                self.settings.spawn_time /= 1.03

if __name__ == '__main__':
    game = FlappyParrot()
    game.run_game()
