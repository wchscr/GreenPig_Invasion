import pygame
from src.entiy.Settings import Settings
from src.entiy.Bird import Bird
from src.function import game_functions as gf
from pygame.sprite import Group
from src.entiy.game_stats import GameStats
from src.entiy.scoreboard import Scoreboard
from src.entiy.button import Button

def game_init():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_height, ai_settings.screen_height))  # 设置游戏窗口大小
    pygame.display.set_caption("绿皮猪入侵")  # 游戏名

    # 初始化背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('static/bgm/bgm.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一艘小鸟
    brid = Bird(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    super_bullets = Group()  # 超级子弹
    # 创建一个猪编组
    pigs = Group()
    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建猪人群
    gf.create_fleet(ai_settings, screen, brid, pigs)

    return ai_settings, screen, stats, sb, play_button, brid, pigs, bullets, super_bullets

def run_game():

    # 游戏初始化
    ai_settings, screen, stats, sb, play_button, brid, pigs, bullets, super_bullets = game_init()

    # 游戏主循环
    while True:
        #检查事件的发生
        gf.check_events(ai_settings, screen, stats, sb, play_button, brid, pigs, bullets, super_bullets)
        if stats.game_active:
            # 如果小鸟还活着才更新实体状态
            brid.update() # 更新小鸟状态
            gf.update_bullets(ai_settings, screen, stats, sb, brid, pigs, bullets, super_bullets) # 更新子弹状态
            gf.update_pigs(ai_settings, stats, screen, sb, brid, pigs, bullets, super_bullets) # 更新猪状态
        # 每次循环都重绘屏幕
        gf.update_screen(ai_settings, screen, stats, sb, brid, pigs, bullets, super_bullets, play_button)

if __name__ == '__main__':
    run_game() #启动游戏