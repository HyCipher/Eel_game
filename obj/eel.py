import pygame
import random
import math


class Eel:
    # 🧠 默认参数抽成类属性，方便统一管理
    default_color = (0, 200, 100)
    default_radius = 20
    default_speed = 0.02
    default_slow_factor = 0.3
    default_electric_field_radius = 160
    default_electric_field_color = (0, 255, 255, 80)

    def __init__(
        self, x, y,
        color=None,
        radius=None,
        speed=None,
        slow_factor=None,
        electric_field_radius=None,
        electric_field_color=None
    ):
        self.x = x
        self.y = y

        # 使用类属性作为默认值
        self.color = color or self.default_color
        self.radius = radius or self.default_radius
        self.speed = speed or self.default_speed
        self.slow_factor = slow_factor or self.default_slow_factor
        self.electric_field_radius = electric_field_radius or self.default_electric_field_radius
        self.electric_field_color = electric_field_color or self.default_electric_field_color

        # 随机初始方向
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def small_random_turn(self, max_angle_deg=20):
        current_angle = math.atan2(self.dy, self.dx)
        delta_angle = math.radians(random.uniform(-max_angle_deg, max_angle_deg))
        new_angle = current_angle + delta_angle
        self.dx = math.cos(new_angle)
        self.dy = math.sin(new_angle)

    def bounce_horizontal(self):
        self.dx *= -1
        self.small_random_turn()

    def bounce_vertical(self):
        self.dy *= -1
        self.small_random_turn()

    def check_screen_bounds(self, width, height):
        if self.x - self.radius < 0:
            self.x = self.radius
            self.bounce_horizontal()
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.bounce_horizontal()

        if self.y - self.radius < 0:
            self.y = self.radius
            self.bounce_vertical()
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.bounce_vertical()

    def check_wall_collision(self, wall_x, gap_top, gap_bottom, line_width):
        wall_left = wall_x - line_width / 2
        wall_right = wall_x + line_width / 2

        wall_left_bound = wall_left - self.radius
        wall_right_bound = wall_right + self.radius

        if wall_left_bound < self.x < wall_right_bound:
            if self.x < wall_x:
                self.x = wall_left_bound
            else:
                self.x = wall_right_bound
            self.bounce_horizontal()

    def update(self, width, height, wall_x=None, gap_top=None, gap_bottom=None, line_width=None):
        # 如果你想让鳗鱼游动，把下面取消注释
        # self.move()
        # self.check_screen_bounds(width, height)
        # if wall_x is not None and gap_top is not None and gap_bottom is not None and line_width is not None:
        #     self.check_wall_collision(wall_x, gap_top, gap_bottom, line_width)
        # if random.random() < 0.01:
        #     self.small_random_turn()
        pass

    def affects(self, fish, wall_x):
        distance = math.hypot(self.x - fish.x, self.y - fish.y)
        if distance > self.electric_field_radius:
            return False
        same_side = (self.x < wall_x and fish.x < wall_x) or (self.x > wall_x and fish.x > wall_x)
        return same_side

    def draw(self, screen):
        surface = pygame.Surface(
            (self.electric_field_radius * 2, self.electric_field_radius * 2),
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            surface,
            self.electric_field_color,
            (self.electric_field_radius, self.electric_field_radius),
            self.electric_field_radius
        )
        screen.blit(surface, (self.x - self.electric_field_radius, self.y - self.electric_field_radius))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
