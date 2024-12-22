import sys
import pygame.font


class Button():
    def __init__(self, game, msg, cnt, not_one_str=False, cnt_text=0):
        # Инициализирует атрибуты кнопки
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначаем размер и свойства
        self.button_colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
        self.text_colors = [(255, 255, 255), (0, 0, 0)]
        if "Play" in msg:
            self.width, self.height = 200, 90
        else:
            self.width, self.height = 200, 60
        self.button_color = self.button_colors[cnt % len(self.button_colors)]
        self.text_color_base = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Строим кнопку
        if cnt != 1:
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.spacing = -20
            self.rect.center = (
                self.screen_rect.centerx,
                self.screen_rect.centery + cnt * (self.height - self.spacing)
            )
            self._prep_msg(msg, not_one_str)
        else:
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.spacing = -27.5
            self.rect.center = (
                self.screen_rect.centerx,
                self.screen_rect.centery + cnt * (self.height - self.spacing)
            )
            self._prep_msg(msg, not_one_str)

    def _prep_msg(self, msg, not_one_str):
        # Выравниваем и создаем текст
        if not_one_str:
            lines = msg.split("\n")
            spacer = 0
            self.msg_image_rects = []
            for line in lines:
                msg_image = self.font.render(line, True, self.text_color_base, self.button_color)
                msg_image_rect = msg_image.get_rect()
                msg_image_rect.center = (self.rect.centerx, self.rect.centery - 20 + spacer)
                self.msg_image_rects.append(msg_image_rect)
                spacer += 30
            self.msg_images = [self.font.render(lines[i], True, self.text_colors[i], self.button_color) for i in range(len(lines))]
        else:
            self.msg_image = self.font.render(msg, True, self.text_color_base, self.button_color)
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center

    def draw_button(self, not_one_str=False):
        # Отображение кнопки и текста
        self.screen.fill(self.button_color, self.rect)
        if not_one_str:
            for i, msg_image in enumerate(self.msg_images):
                self.screen.blit(msg_image, self.msg_image_rects[i])
        else:
            self.screen.blit(self.msg_image, self.msg_image_rect)
