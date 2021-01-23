import pygame
import sys
from src.entiy.Bullet import Bullet
from src.entiy.Pig import  Pig
from time import sleep
import random

from src.entiy.Super_bullet import superBullet

def check_keydown_events(event,ai_settings, screen, bird, bullets, super_bullets):
    """
    键盘被按下
    :param event: 游戏事件对象
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param bird: 小鸟对象
    :param bullets: 子弹编组对象
    :param super_bullets: 导弹编组
    """
    if event.key == pygame.K_RIGHT:
        bird.moving_right = True
    elif event.key == pygame.K_LEFT:
        bird.moving_left = True
    elif event.key == pygame.K_UP:
        bird.moving_up = True
    elif event.key == pygame.K_DOWN:
        bird.moving_down = True
    elif event.key == pygame.K_SPACE:
        # 创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings, screen, bird, bullets)
    elif event.key == pygame.K_z:
        # 创建一颗导弹，并将其加入到编组bullets中
        fire_super_bullet(ai_settings, screen, bird, super_bullets)
    elif event.key == pygame.K_q:
        #当按下Q键后退出游戏
        sys.exit()

def check_keyup_events(event, bird):
    """
    当键盘被松开
    :param event: 游戏事件对象
    :param bird: 小鸟对象
    :return:
    """
    if event.key == pygame.K_RIGHT:
        # 小鸟停止向右移动
        bird.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 小鸟停止向左移动
        bird.moving_left = False
    elif event.key == pygame.K_UP:
        bird.moving_up = False
    elif event.key == pygame.K_DOWN:
        bird.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, bird, pigs,bullets, super_bullets):
    """
    监视键盘和鼠标事件
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏计分牌对象
    :param play_button: 开始游戏按钮对象
    :param bird: 小鸟对象
    :param pigs: 猪编组对象
    :param bullets: 子弹编组对象
    :param super_bullets: 导弹对象
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #当键盘被按下
           check_keydown_events(event, ai_settings, screen, bird, bullets, super_bullets)
        elif event.type == pygame.KEYUP:  #当键盘被松开
            check_keyup_events(event, bird)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, bird, pigs, bullets, super_bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, bird, pigs, bullets, super_bullets, mouse_x, mouse_y):
    """
    在玩家点击Play按钮时开始游戏
    :param ai_settings: 游戏设置信息
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param play_button: Play按钮对象
    :param bird: 小鸟对象
    :param pigs: 猪编组对象
    :param bullets: 子弹编组对象
    :param mouse_x: 鼠标位置的x坐标
    :param mouse_y: 鼠标位置的y坐标
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分牌图像
        sb.prep_score()       # 准备当前分数
        sb.prep_high_score()  # 准备最高分数
        sb.prep_level()       # 准备当前游戏等级
        sb.prep_birds()       # 准备剩余游戏机会

        # 清空猪列表和子弹列表
        pigs.empty()
        bullets.empty()
        super_bullets.empty()

        # 创建一群新的猪，并让小鸟居中
        create_fleet(ai_settings, screen, bird, pigs)
        bird.center_bird()

def update_screen(ai_settings, screen, stats, sb, bird, pigs,bullets, super_bullets, play_button):
    """
    更新屏幕上的图像，并切换到新屏幕
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪编组对象
    :param bullets: 子弹编组对象
    :param super_bullets: 导弹编组
    :param play_button: 游戏开始按钮对象
    """
    screen.fill(ai_settings.bg_color)  # 背景颜色

    # 绘制所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制所有导弹
    for super_bullet in super_bullets.sprites():
        super_bullet.draw_bullet()

    bird.blitme()  # 小鸟
    pigs.draw(screen) #猪

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, bird, pigs, bullets, super_bullets):
    """
    更新子弹的位置，并删除已消失的子弹
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪编组对象
    :param bullets: 子弹编组对象
    :param super_bullets: 导弹对象
    """

    # 更新子弹的状态
    bullets.update()
    super_bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.centerx >= screen.get_rect().right:
            bullets.remove(bullet)
    #print(len(bullets))

    # 删除已消失的导弹
    for super_bullet in super_bullets.copy():
        if super_bullet.rect.bottom <= 0:
            super_bullets.remove(super_bullet)

    # 检查是否有子弹击中了猪
    check_bullet_pig_collision(ai_settings, screen, stats, sb, bird, pigs, bullets, super_bullets)

def check_bullet_pig_collision(ai_settings, screen, stats, sb, bird, pigs,bullets, super_bullets):
    """
    检测猪与子弹相撞
    :param ai_settings: 游戏设置对象
    :param screen: 屏幕对象
    :param stats: 游戏统计信息对象
    :param sb: 游戏记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪对象
    :param bullets: 子弹编组对象
    :param super_bullets: 导弹对象
    """
    # 如果子弹击中了猪，就删除相应的子弹和猪
    # 两个布尔类型的实参分别表示是否要删除第一个编组的个体和第二个编组的个体
    collisions = pygame.sprite.groupcollide(bullets, pigs, True, True)
    super_collisions = pygame.sprite.groupcollide(super_bullets, pigs, False, True)

    if collisions:
        # 当子弹击中猪，得分加pig_points
        for pigs in collisions.values():
            stats.score += ai_settings.pig_points * len(pigs)
            sb.prep_score()
        # 每次击中猪后检查最高分是否发送变化
        check_high_score(stats, sb)

    if super_collisions:
        # 当子弹击中猪，得分加pig_points
        for pigs in super_collisions.values():
            stats.score += ai_settings.pig_points * len(pigs)
            sb.prep_score()
        # 每次击中猪后检查最高分是否发送变化
        check_high_score(stats, sb)

    if len(pigs) == 0:
        # 删除所有子弹，加快游戏节奏，并创建一群新的猪
        bullets.empty()
        super_bullets.empty()
        ai_settings.increase_speed()

        # 如果整群猪都被消灭，就提高一个等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, bird, pigs)

def fire_bullet(ai_settings, screen, bird, bullets):
    """
    发射新的子弹
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param bird: 小鸟对象
    :param bullets: 子弹编组
    """
    if len(bullets) < ai_settings.bullets_allowed:
        # 当子弹数小于允许最大子弹数时才创建新子弹
        new_bullet = Bullet(ai_settings, screen, bird)
        bullets.add(new_bullet)

def fire_super_bullet(ai_settings, screen, bird, super_bullets):
    """
    发射新的子弹
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param bird: 小鸟对象
    :param super_bullets: 子弹编组
    :return:
    """
    if len(super_bullets) < ai_settings.super_bullets_allowed:
        # 当子弹数小于允许最大子弹数时才创建新子弹
        new_bullet = superBullet(ai_settings, screen, bird)
        super_bullets.add(new_bullet)

def get_number_pigs_y(ai_settings, pig_height):
    """
    计算每列可容纳多少个猪
    :param ai_settings: 游戏设置
    :param pig_width: 猪图像的宽度
    :return: 每行可容纳的猪数量
    """
    available_space_y = ai_settings.screen_height - 2 * pig_height
    number_pigs_y = int(available_space_y / (2 * pig_height))
    return number_pigs_y

def get_number_lines(ai_settings, bird_width, pig_width):
    """
    计算屏幕可以容纳多少列猪
    :param ai_settings: 游戏设置
    :param bird_height: 小鸟图像长度
    :param pig_height: 猪图像的长度
    :return: 每次产生多少行猪
    """
    available_space_x = ai_settings.screen_width - 2 * bird_width
    number_rows = int(available_space_x / (2 * pig_width))         #每隔一行放置一行猪
    return number_rows

def create_pig(ai_settings, screen, pigs, pig_number, line_number):
    """
    创建一个猪并加入当前行
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param pigs: 猪编组
    :param pig_number: 当前行猪的编号
    :param row_number: 当前行的编号
    """
    pig = Pig(ai_settings, screen)
    # 每空一个位置创建一个猪
    pig_height = pig.rect.height
    pig.y = pig_height + 2 * pig_height * pig_number
    pig.rect.y = pig.y
    pig.rect.x = ai_settings.screen_width - pig.rect.width * 2 - 2 * pig.rect.width * line_number
    pigs.add(pig)

def create_fleet(ai_settings, screen, bird, pigs):
    """
    创建猪人群
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param bird: 小鸟对象
    :param pigs: 猪编组
    """
    #猪间距为猪宽度和高度
    pig = Pig(ai_settings, screen)
    number_pigs_y = get_number_pigs_y(ai_settings, pig.rect.height) # 计算一列可容纳多少个猪
    number_lines = get_number_lines(ai_settings, bird.rect.width, pig.rect.width) - 2 # 计算一共可以容纳多少列猪

    # 创建猪人群
    for line_number in range(number_lines):
        for pig_number in range(number_pigs_y):
            if random.randint(1, 100) /100 < ai_settings.density:
                create_pig(ai_settings, screen, pigs, pig_number, line_number)

def check_fleet_edges(ai_settings, pigs):
    """
    有猪到达边缘时采取相应的措施
    :param ai_settings: 游戏设置
    :param pigs: 猪编组
    """
    for pig in pigs.sprites():
        if pig.check_edges():
            change_fleet_direction(ai_settings, pigs)   #改变猪的移动方向
            break

def change_fleet_direction(ai_settings, pigs):
    """
    将猪整体左移，并改变水平移动方向
    :param ai_settings: 游戏设置
    :param pigs: 猪编组
    """
    for pig in pigs.sprites():
        pig.rect.x -= ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def bird_hit(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets):
    """
    响应被猪撞到的小鸟
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪编组
    :param bullets: 子弹编组
    :param super_bullets: 导弹编组
    """
    # 将bird_left(剩余命数)减1
    if stats.bird_left > 0:
        stats.bird_left -= 1
        sb.prep_birds() #更新记分牌中，剩余游戏机会
        sleep(0.5)   # 暂停
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # 游戏结束时让鼠标可见

    # 清空猪列表和子弹列表
    pigs.empty()
    bullets.empty()
    super_bullets.empty()

    # 创建一群新的猪，并将小鸟放到屏幕底端中央
    create_fleet(ai_settings, screen, bird, pigs)
    bird.center_bird()

def check_pigs_bottom(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets):
    """
    检查是否有猪到达屏幕底端
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪编组
    :param bullets: 子弹编组
    :param super_bullets: 导弹编组
    """
    screen_rect = screen.get_rect()
    for pig in pigs.sprites():
        if pig.rect.left <= screen_rect.left:
            # 像小鸟被撞到一样进行处理
            bird_hit(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets)
            break

def update_pigs(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets):
    """
    检查是否有猪位于屏幕边缘位置，并更新所有猪的位置
    :param ai_settings: 游戏设置
    :param stats: 游戏统计信息对象
    :param screen: 屏幕对象
    :param sb: 记分牌对象
    :param bird: 小鸟对象
    :param pigs: 猪编组
    :param bullets: 子弹编组
    :param super_bullets: 导弹编组
    """
    check_fleet_edges(ai_settings, pigs)
    pigs.update()

    # 检测猪和小鸟之间的碰撞
    # 方法spritecollideany()接受两个实参：一个“精灵”和一个编组。
    # 它检查编组是否有成员与精灵发生了碰撞，并在找到了与精灵发送碰撞的成员后停止遍历
    if pygame.sprite.spritecollideany(bird, pigs):
        bird_hit(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets)
        # print("小鸟没了!")
    # 检查是否有猪到达屏幕最左端 
    check_pigs_bottom(ai_settings, stats, screen, sb, bird, pigs, bullets, super_bullets)

def check_high_score(stats, sb):
    """
    检查是否诞生了新的最高分
    :param stats: 游戏统计信息对象
    :param sb: 计分板对象
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()