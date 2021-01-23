import pygame
from pygame.sprite import Sprite


class Bird(Sprite):

    def __init__(self, ai_settings, screen):
        """
        初始化小鸟并设置其初始位置
        :param ai_settings: 游戏设置
        :param screen: 屏幕对象
        """
        super().__init__() # 调用父类Sprite的构造函数
        self.screen = screen
        self.ai_settings = ai_settings

        #加载小鸟图像并获取外接矩形
        self.image = pygame.image.load('static/images/brid.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #每艘小鸟初始放在屏幕底部中央
        self.center_bird()

        #在小鸟的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整小鸟的位置"""
        # 更新小鸟的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.bird_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.bird_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.bird_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.bird_speed_factor
        # 根据self.center更新rect对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        #在指定位置绘制小鸟
        self.screen.blit(self.image, self.rect)

    def center_bird(self):
        # 让小鸟在屏幕上居中
        self.center = self.screen_rect.left
        self.bottom = int(self.screen_rect.bottom/2)