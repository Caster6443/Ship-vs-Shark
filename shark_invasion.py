import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from shark import Shark
from utils import get_resource_path


class SharkInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 设置游戏全屏
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 绘制窗口
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.background = pygame.image.load(
            get_resource_path("images/bg.png")
        ).convert()
        # 给窗口起名
        pygame.display.set_caption("Shark Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.sharks = pygame.sprite.Group()
        self._create_fleet()
        # 游戏启动后处于活动状态
        self.game_active = False

        # 创建Play按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_sharks()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """响应鼠标和键盘事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            # 清空太空鲨鱼列表和子弹列表
            self.bullets.empty()
            self.sharks.empty()
            # 创建一个新的太空鲨舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组 bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_shark_collisions()

    def _check_bullet_shark_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.sharks, True, True)
        if collisions:
            for sharks in collisions.values():
                self.stats.score += self.settings.shark_points * len(sharks)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.sharks:
            # 删除现有的子弹并创建一个新的外型舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """响应飞船和太空鲨的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减1 并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空太空鲨列表和子弹列表
            self.bullets.empty()
            self.sharks.empty()
            # 创建一个新的太空鲨舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            # 游戏结束时显示光标
            pygame.mouse.set_visible(True)

    def _update_sharks(self):
        """检查是否有太空鲨位于屏幕边缘，并更新整个太空鲨舰队的位置"""
        self._check_fleet_edges()
        self.sharks.update()
        # 检测太空鲨和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.sharks):
            self._ship_hit()
        # 检查是否有太空鲨到达了屏幕的下边缘
        self._check_sharks_bottom()

    def _create_fleet(self):
        """创建一个太空鲨舰队"""
        # 创建一个太空鲨, 再不断添加，直到没有空间添加太空鲨为止
        # 太空鲨的间距为太空鲨的宽度
        shark = Shark(self)
        shark_width, shark_height = shark.rect.size
        current_x, current_y = shark_width, shark_height
        while current_y < (self.settings.screen_height - 3 * shark_height):
            while current_x < (self.settings.screen_width - 2 * shark_width):
                self._create_shark(current_x, current_y)
                current_x += 2 * shark_width
                # 添加一行鲨鱼后，重置x值并递增y值
            current_x = shark_width
            current_y += 2 * shark_height

    def _create_shark(self, x_position, y_position):
        """创建一个太空鲨鱼并将其放在当前行中"""
        new_shark = Shark(self)
        new_shark.x = x_position
        new_shark.rect.x = x_position
        new_shark.rect.y = y_position
        self.sharks.add(new_shark)

    def _check_fleet_edges(self):
        """在有太空鲨到达边缘时采取相应的措施"""
        for shark in self.sharks.sprites():
            if shark.check_edges():
                self._change_fleet_direction()
                break

    def _check_sharks_bottom(self):
        """检查是否有太空鲨到达了屏幕的下边缘"""
        for shark in self.sharks.sprites():
            if shark.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """将整个太空鲨舰队向下移动，并改变它们的方向"""
        for shark in self.sharks.sprites():
            shark.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.sharks.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = SharkInvasion()
    ai.run_game()
