
class GameStats():
    # 跟踪游戏的统计信息

    def __init__(self, ai_settings):
        """
        初始化统计信息
        :param ai_settings: 游戏设置
        """
        self.ai_settings = ai_settings
        self.reset_stats() # 初始化游戏运行期间可能发生变化的统计信息
        # 游戏刚启动时处于非活动状态
        self.game_active = False

        # 在任何情况下都不应重置最高分
        self.high_score = 0

    def reset_stats(self):
        # 初始化在游戏运行期间可能发生变化的统计信息
        self.bird_left = self.ai_settings.bird_limit   #玩家拥有的小鸟数量
        self.score = 0
        self.level = 1
