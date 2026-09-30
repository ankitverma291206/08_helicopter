"""Game state, collision detection, scoring and shield management."""
import random
import pygame
from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3
DISTANCE_PER_FRAME = SCROLL_SPEED / 60.0

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.distance = 0.0
        self.game_over = False
        self.shield_active = False
        self._spawn_obstacle()

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2,
                               HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(WIDTH, gap_y, GAP_HEIGHT,
                                        WALL_WIDTH, HEIGHT, SCROLL_SPEED))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return
        if key in (pygame.K_s, pygame.K_SPACE):
            self.shield_active = True

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

        self.distance += DISTANCE_PER_FRAME

        heli_rect = self.helicopter.get_rect()
        for obstacle in self.obstacles:
            if obstacle.collides_with(heli_rect):
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.game_over = True
                    break

        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles, font,
                            self.distance, self.shield_active, self.game_over)
