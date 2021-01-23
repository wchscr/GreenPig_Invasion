import pygame
from pygame.sprite import Sprite


class Pig(Sprite):
    # 表示单个猪的类

    def __init__(self, ai_settings, screen):
        """
        初始化猪并设置其起始位置
        :param ai_settings: 游戏设置
        :param screen: 屏幕对象
        """
        super(Pig, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载猪的图像，并设置其rect属性
        self.image = pygame.image.load('static/images/pig.bmp')
        self.rect = self.image.get_rect()

        #每个猪最初都在屏幕的右上角出现
        self.rect.x = ai_settings.screen_width - self.rect.width
        self.rect.y = ai_settings.screen_height - self.rect.height

        #存储猪的准确位置
        self.y = float(self.rect.y)

    def blitme(self):
        #在指定位置绘制猪
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        #如果猪位于屏幕边缘，就返回True
        screen_rect = self.screen.get_rect()
        if self.rect.top <=0 :
            return True
        elif self.rect.bottom >= screen_rect.bottom:
            return True

    def update(self):
        #水平向左或者向右移动猪
        self.y += (self.ai_settings.pig_speed_factor * self.ai_settings.fleet_direction)
        self.rect.y = self.y