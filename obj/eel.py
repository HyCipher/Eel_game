import pygame
import random
import math


class Eel:
    def __init__(self, x, y, color=(0, 200, 100), radius=20, speed=0.02):
        """
        Eel's property
        :param x: position
        :param y: position
        :param color:
        :param radius: size
        :param speed:
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed

        # A random initial movement direction
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

        self.electric_field_radius = 80  # Electric field radius
        self.electric_field_color = (0, 255, 255, 80)  # RGBA with transparency

    # movement
    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    # The small changes in direction make the electric eel look like it is "swimming randomly."
    def small_random_turn(self, max_angle_deg=20):
        current_angle = math.atan2(self.dy, self.dx)
        delta_angle = math.radians(random.uniform(-max_angle_deg, max_angle_deg))
        new_angle = current_angle + delta_angle
        self.dx = math.cos(new_angle)
        self.dy = math.sin(new_angle)

    # After hitting the left and right boundaries, it bounces back (in the opposite direction of x) and performs a slight steering perturbation.
    def bounce_horizontal(self):
        self.dx *= -1
        self.small_random_turn()

    # After hitting the left and right boundaries, it bounces back (in the opposite direction of y) and performs a slight steering perturbation.
    def bounce_vertical(self):
        self.dy *= -1
        self.small_random_turn()

    # Make sure the eel doesn't swim off the screen.
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

    # Determine whether the electric eel has entered the wall and channel area, and bounce back as long as it enters the horizontal range of the wall.
    def check_wall_collision(self, wall_x, gap_top, gap_bottom, line_width):
        wall_left = wall_x - line_width / 2
        wall_right = wall_x + line_width / 2

        wall_left_bound = wall_left - self.radius
        wall_right_bound = wall_right + self.radius

        # 不管在不在通道范围，只要进入墙体区域就反弹
        if wall_left_bound < self.x < wall_right_bound:
            if self.x < wall_x:
                self.x = wall_left_bound
            else:
                self.x = wall_right_bound
            self.bounce_horizontal()

    def update(self, width, height, wall_x=None, gap_top=None, gap_bottom=None, line_width=None):
        self.move()
        self.check_screen_bounds(width, height)
        if wall_x is not None and gap_top is not None and gap_bottom is not None and line_width is not None:
            self.check_wall_collision(wall_x, gap_top, gap_bottom, line_width)
        if random.random() < 0.01:
            self.small_random_turn()

    def affects(self, fish, wall_x):
        # 计算两者距离
        distance = math.hypot(self.x - fish.x, self.y - fish.y)

        # 只影响电场半径范围内的鱼
        if distance > self.electric_field_radius:
            return False

        # 限制电场作用只影响同一边的鱼
        same_side = (self.x < wall_x and fish.x < wall_x) or (self.x > wall_x and fish.x > wall_x)
        return same_side

    def draw(self, screen):
        # draw electric field
        electric_surface = pygame.Surface((self.electric_field_radius * 2, self.electric_field_radius * 2),
                                          pygame.SRCALPHA)
        pygame.draw.circle(
            electric_surface,
            self.electric_field_color,
            (self.electric_field_radius, self.electric_field_radius),
            self.electric_field_radius
        )
        screen.blit(electric_surface, (self.x - self.electric_field_radius, self.y - self.electric_field_radius))

        # Draw eel object
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
