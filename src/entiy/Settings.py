class Settings():
    # 存储《绿皮猪入侵》的所有设置类

    def __init__(self):
        #初始化游戏设置

        #游戏窗口大小
        self.screen_width = 800
        self.screen_height = 800
        # 背景颜色
        self.bg_color = (255, 255, 255)

        # 小鸟固定属性
        self.bird_limit = 3       # 小鸟数量上限

        # 子弹固定属性
        self.bullets_allowed = 3 #允许的最大子弹数

        # 超级子弹固定属性
        self.super_bullets_allowed = 1 # 每个关卡允许的超级子弹数

        # 猪固定属性
        self.fleet_drop_speed = 5      # 猪垂直移动的速度
        self.density = 0.5             # 猪生成密度，初始密度50%

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 猪点数的提高速度
        self.score_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        初始化随游戏进行而变化的设置
        """
        self.bird_speed_factor = 1   # 小鸟移动速度
        self.bullet_speed_factor = 1  # 子弹飞行速度
        self.super_bullet_speed_factor = 0.6 # 超级子弹飞行速度
        self.pig_speed_factor = 0.2  # 猪水平移动的速度

        # 猪群的移动方向，1表示向右，-1表示向左
        self.fleet_direction = 1

        # 计分
        self.pig_points = 50

    def increase_speed(self):
        """
        提高速度设置和猪点数
        """
        self.bird_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.density *= self.speedup_scale

        self.pig_points = int(self.pig_points * self.score_scale)