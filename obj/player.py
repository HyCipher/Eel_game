import pygame

class Player:
    def __init__(self, x, y, color=(255, 0, 0), radius=10, speed=0.1):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        return dx, dy

    def update(self, width, height, wall_x=None, gap_top=None, gap_bottom=None, line_width=20):
        dx, dy = self.handle_input()
        next_x = self.x + dx
        next_y = self.y + dy

        # 屏幕边界限制
        if next_x - self.radius < 0 or next_x + self.radius > width:
            dx = 0
        if next_y - self.radius < 0 or next_y + self.radius > height:
            dy = 0

        # 墙体限制
        if wall_x is not None:
            wall_left = wall_x - line_width // 2
            wall_right = wall_x + line_width // 2
            gap_top_safe = gap_top
            gap_bottom_safe = gap_bottom

            next_x_wall = wall_left - self.radius < next_x < wall_right + self.radius
            next_y_gap = gap_top_safe < next_y < gap_bottom_safe

            # 如果下一帧的位置进入墙体但不在 gap 内，则禁止该方向的移动
            if next_x_wall and not next_y_gap:
                dx = 0
            if next_x_wall and not next_y_gap:
                dy = 0  # 关键补充：防止斜向进入墙体

        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
