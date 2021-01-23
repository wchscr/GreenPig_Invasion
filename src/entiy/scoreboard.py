import pygame.font
from pygame.sprite import Group

from src.entiy.Bird import Bird


class Scoreboard():
    # 显示得分信息的类

    def __init__(self, ai_settings, screen, stats):
        """
        初始化显示得分涉及的属性
        :param ai_settings: 游戏设置
        :param screen: 屏幕对象
        :param stats: 游戏统计信息对象
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('arial', 48)

        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_birds()

    def prep_score(self):
        # 将得分转换为一副渲染的图像
        rounded_score = int(round(self.stats.score - 1))
        score_str = "{:,}".format(rounded_score) # 字符格式转换指令，在数字转换为字符串时在其中插入逗号(千位符)，例如1,000,000
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        # 在屏幕上显示得分
        self.screen.blit(self.score_image, self.score_rect)   # 显示当前得分信息
        self.screen.blit(self.high_score_image, self.high_score_rect) # 显示最高分信息
        self.screen.blit(self.level_image, self.level_rect) # 显示游戏等级信息
        self.birds.draw(self.screen) # 绘制剩余的飞船命数

    def prep_high_score(self):
        """
        将最高得分转换为渲染的图像
        """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """
        将等级转换为渲染的图像
        """
        # render函数用于渲染图像
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right # 将等级信息与得分信息对齐
        self.level_rect.top = self.score_rect.bottom + 10 # 将等级信息放在得分下方10个单位处

    def prep_birds(self):
        """
        显示还余下多少游戏机会
        """
        self.birds = Group()
        for bird_number in range(self.stats.bird_left):
            # 根据玩家还剩余多少飞船来打印左上角的飞船
            bird = Bird(self.ai_settings, self.screen)
            bird.rect.x = 10 + bird_number * bird.rect.width
            bird.rect.y = 10
            self.birds.add(bird)