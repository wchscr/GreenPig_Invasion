import pygame
#“精灵”类
from pygame.sprite import Sprite

class Bullet(Sprite):   #Bullet作为子类继承父类Sprite
    #对小鸟发射的子弹进行群组式的管理

    def __init__(self, ai_settings, screen, brid):
        """
        在小鸟所在的位置创建一个子弹对象
        :param ai_settings: 游戏设置对象
        :param screen: 屏幕对象
        :param brid: 小鸟对象
        """
        super().__init__() # 调用父类Sprite的构造函数
        self.screen = screen

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.image = pygame.image.load('static/images/heart.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = brid.rect.centerx   #将子弹移动到小鸟处
        self.rect.top = brid.rect.top           #将子弹移动到小鸟头部

        #存储用小数表示的子弹纵轴位置
        self.x = float(self.rect.x)

        #设置子弹的颜色和飞行速度
        # self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # 超级子弹


    def update(self):
        #向右移动子弹
        self.x += self.speed_factor
        self.rect.x = self.x

    def draw_bullet(self):
        #在屏幕上绘制子弹
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
