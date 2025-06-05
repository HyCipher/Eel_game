# env/wall.py

import pygame


class Wall:
    def __init__(self, width, height, line_width=40, gap_height=100, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.line_width = line_width
        self.gap_height = gap_height
        self.color = color

    def draw(self, screen):
        top_rect = pygame.Rect(
            self.width // 2 - self.line_width // 2,
            0,
            self.line_width,
            (self.height - self.gap_height) // 2
        )
        bottom_rect = pygame.Rect(
            self.width // 2 - self.line_width // 2,
            (self.height + self.gap_height) // 2,
            self.line_width,
            (self.height - self.gap_height) // 2
        )

        pygame.draw.rect(screen, self.color, top_rect)
        pygame.draw.rect(screen, self.color, bottom_rect)

    def get_gap_bounds(self):
        gap_top = (self.height - self.gap_height) // 2
        gap_bottom = (self.height + self.gap_height) // 2
        wall_x = self.width // 2
        return wall_x, gap_top, gap_bottom
