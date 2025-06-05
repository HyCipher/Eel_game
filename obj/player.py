import pygame


class Player:
    def __init__(self, x, y, color=(255, 0, 0), radius=12, speed=2):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

    def check_screen_bounds(self, width, height):
        r = self.radius
        self.x = max(r, min(width - r, self.x))
        self.y = max(r, min(height - r, self.y))

    def update(self, width, height):
        self.handle_keys()
        self.check_screen_bounds(width, height)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
