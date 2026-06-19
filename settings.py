import pygame


class Settings:
    """存储游戏<<太空鲨入侵>> 中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        info = pygame.display.Info()
        monitor_height = info.current_h

        # 动态计算分辨率
        # 如果玩家屏幕高度大于 1440
        if monitor_height > 1440:
            self.screen_height = 1350
            self.screen_width = 1080
        else:
            # 否则自动降级为适合笔记本大屏幕的尺寸（比如高度占屏幕的 80%）
            # 保持 4:5 的比例：宽 = 高 * 0.8
            self.screen_height = int(monitor_height * 0.8)
            self.screen_width = int(self.screen_height * 0.8)
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 50

        # 太空鲨设置
        self.fleet_drop_speed = 20
        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        # 太空鲨分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 5.5
        self.bullet_speed = 5.0
        self.shark_speed = 5.0
        # fleet_direction 为 1 表示向右移动，为 -1 表示向左移动
        self.fleet_direction = 1
        # 记分设置
        self.shark_points = 50

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.shark_speed *= self.speedup_scale
        self.shark_points = int(self.shark_points * self.score_scale)
