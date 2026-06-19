import pygame
from pygame.sprite import Sprite
from utils import get_resource_path


class Shark(Sprite):
    """表示单个太空鲨的类"""

    def __init__(self, ai_game):
        """初始化太空鲨鱼并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载太空鲨图像并设置其rect属性
        self.image = pygame.image.load(get_resource_path("images/shark.png"))
        self.image = pygame.transform.scale(self.image, (66, 106))
        self.rect = self.image.get_rect()
        # 每个太空鲨最初都在屏幕左上角生成
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 储存太空鲨的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """向左或向右移动外星人"""
        self.x += self.settings.shark_speed * self.settings.fleet_direction
        self.rect.x = self.x
