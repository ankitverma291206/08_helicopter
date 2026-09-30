"""Player-controlled helicopter with bounded vertical movement."""
import pygame

THRUST = 0.4
MAX_VERTICAL_SPEED = 5.0

class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        up = keys_pressed[pygame.K_UP]
        down = keys_pressed[pygame.K_DOWN]
        if up and not down:
            self.vy = max(self.vy - THRUST, -MAX_VERTICAL_SPEED)
        elif down and not up:
            self.vy = min(self.vy + THRUST, MAX_VERTICAL_SPEED)
        elif up and down:
            self.vy = 0.0

    def update(self, height_bound):
        self.y += self.vy
        half_h = self.height / 2
        min_y, max_y = half_h, height_bound - half_h
        if self.y < min_y:
            self.y, self.vy = min_y, 0.0
        elif self.y > max_y:
            self.y, self.vy = max_y, 0.0

    def get_rect(self):
        return pygame.Rect(int(self.x - self.width / 2),
                           int(self.y - self.height / 2),
                           self.width, self.height)
