import pygame
from env.wall import Wall
import sys
from generate import fish_generate
from generate import eel_generate


class Canvas:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Eel Game")

        self.background_color = (255, 255, 255)
        self.line_color = (0, 0, 0)
        self.line_width = 40
        self.gap_height = 100

        self.wall = Wall(self.width, self.height, self.line_width, self.gap_height, self.line_color)

        # 调用独立的生成鱼方法
        # 获取中间墙体和通道上下边界的坐标
        wall_x, gap_top, gap_bottom = self.wall.get_gap_bounds()

        self.left_fishes = fish_generate.generate_left_fishes(
            count=6,
            width=self.width,
            height=self.height,
            wall_x=wall_x,
            gap_top=gap_top,
            gap_bottom=gap_bottom,
            line_width=self.line_width,
            radius=10
        )

        self.right_fishes = fish_generate.generate_right_fishes(
            count=6,
            width=self.width,
            height=self.height,
            wall_x=wall_x,
            gap_top=gap_top,
            gap_bottom=gap_bottom,
            line_width=self.line_width,
            radius=10
        )

        # 初始化 eel
        self.left_eels = eel_generate.generate_left_eels(
            count=1,
            width=self.width,
            height=self.height,
            wall_x=wall_x,
            line_width=self.line_width,
            radius=15
        )

        self.right_eels = eel_generate.generate_right_eels(
            count=1,
            width=self.width,
            height=self.height,
            wall_x=wall_x,
            line_width=self.line_width,
            radius=15
        )

    def close(self):
        pygame.quit()
        sys.exit()
