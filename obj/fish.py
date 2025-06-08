import pygame
import random
import math


class Fish:
    # 🧠 类属性用于默认值统一管理
    default_color = (0, 0, 255)
    default_radius = 10
    default_speed = 0.10
    default_slow_timer = 60
    default_slow_factor = 0.3
    default_avoid_distance = 80

    def __init__(
        self,
        x,
        y,
        color=None,
        radius=None,
        speed=None
    ):
        self.x = x
        self.y = y

        self.color = color or self.default_color
        self.radius = radius or self.default_radius
        self.base_speed = speed or self.default_speed
        self.speed = self.base_speed

        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.slow_timer = 0

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def small_random_turn(self, max_angle_deg=30):
        angle = math.atan2(self.dy, self.dx)
        angle += math.radians(random.uniform(-max_angle_deg, max_angle_deg))
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

    def bounce_horizontal(self):
        self.dx *= -1
        self.small_random_turn()

    def bounce_vertical(self):
        self.dy *= -1
        self.small_random_turn()

    def check_screen_bounds(self, width, height):
        r = self.radius
        if self.x - r < 0:
            self.x = r
            self.bounce_horizontal()
        elif self.x + r > width:
            self.x = width - r
            self.bounce_horizontal()

        if self.y - r < 0:
            self.y = r
            self.bounce_vertical()
        elif self.y + r > height:
            self.y = height - r
            self.bounce_vertical()

    def check_wall_collision(self, wall_x, gap_top, gap_bottom, line_width=20):
        if wall_x is None or gap_top is None or gap_bottom is None:
            return

        r = self.radius
        wall_left = wall_x - line_width // 2
        wall_right = wall_x + line_width // 2
        gap_top_safe = gap_top - r
        gap_bottom_safe = gap_bottom + r

        in_wall_x = wall_left - r < self.x < wall_right + r
        in_gap_y = gap_top_safe < self.y < gap_bottom_safe

        if in_wall_x:
            if not in_gap_y or True:  # 墙体区域不允许进入
                if self.x < wall_x:
                    self.x = wall_left - r
                else:
                    self.x = wall_right + r
                self.bounce_horizontal()

    def avoid_player(self, player, min_distance=None):
        if min_distance is None:
            min_distance = self.default_avoid_distance

        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.hypot(dx, dy)

        if min_distance > distance > 0:
            angle = math.atan2(dy, dx)
            self.dx = math.cos(angle)
            self.dy = math.sin(angle)
            self.small_random_turn(max_angle_deg=10)

    def update(self, width, height, wall_x=None, gap_top=None, gap_bottom=None, player=None):
        if random.random() < 0.01:
            self.small_random_turn()

        self.move()
        self.check_screen_bounds(width, height)
        self.check_wall_collision(wall_x, gap_top, gap_bottom)

        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer == 0:
                self.speed = self.base_speed

    def react_to_electric_field(self, slow_factor=None):
        if slow_factor is None:
            slow_factor = self.default_slow_factor
        self.speed = self.base_speed * slow_factor
        self.slow_timer = self.default_slow_timer

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    @staticmethod
    def is_valid_position(x, y, wall_x, gap_top, gap_bottom, line_width, radius):
        wall_left = wall_x - line_width // 2 - radius
        wall_right = wall_x + line_width // 2 + radius
        gap_top_safe = gap_top - radius
        gap_bottom_safe = gap_bottom + radius
        return not (wall_left < x < wall_right and gap_top_safe < y < gap_bottom_safe)
