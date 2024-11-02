import pygame.font

class Button():

    def __init__(self, game, msg):
        '''Инициализирует атрибуты кнопки'''
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Назначаем размер и свойства
        self.width, self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        #Строим кнопку
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)
    
    def _prep_msg(self,msg):
        """Выравниваем и создаем текст"""
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_buttom(self):
        #отображение кнопки и текста
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)