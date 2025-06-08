import pygame


class Wall:
    def __init__(self, width, height, line_width=40, gap_height=100, color=(0, 0, 0)):
        self.width = width
        self.height = height

        # 配置参数统一放入 config
        self.config = {
            "line_width": line_width,
            "gap_height": gap_height,
            "color": color
        }

    def draw(self, screen):
        lw = self.config["line_width"]
        gh = self.config["gap_height"]
        color = self.config["color"]

        top_rect = pygame.Rect(
            self.width // 2 - lw // 2,
            0,
            lw,
            (self.height - gh) // 2
        )
        bottom_rect = pygame.Rect(
            self.width // 2 - lw // 2,
            (self.height + gh) // 2,
            lw,
            (self.height - gh) // 2
        )

        pygame.draw.rect(screen, color, top_rect)
        pygame.draw.rect(screen, color, bottom_rect)

    def get_gap_bounds(self):
        gh = self.config["gap_height"]
        gap_top = (self.height - gh) // 2
        gap_bottom = (self.height + gh) // 2
        wall_x = self.width // 2
        return wall_x, gap_top, gap_bottom

    # 可选添加：动态修改配置的方法
    def update_config(self, **kwargs):
        for key in kwargs:
            if key in self.config:
                self.config[key] = kwargs[key]
