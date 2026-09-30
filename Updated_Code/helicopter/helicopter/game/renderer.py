"""Pygame rendering for the helicopter game."""
import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)
COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)
COLOR_SHIELD = (40, 120, 230)
COLOR_GAME_OVER = (180, 40, 40)

def draw_scene(surface, helicopter, obstacles, font, distance=0.0,
               shield_active=False, game_over=False):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_top_rect())
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_bottom_rect())

    heli_rect = helicopter.get_rect()
    pygame.draw.rect(surface, COLOR_HELI, heli_rect, border_radius=4)
    if shield_active:
        pygame.draw.circle(surface, COLOR_SHIELD, heli_rect.center,
                           max(heli_rect.width, heli_rect.height)//2 + 8, 3)

    draw_text(surface, font, f"Distance: {int(distance)} m", (12, 10))
    shield_text = "Shield: ACTIVE (S/SPACE)" if shield_active else "Shield: OFF (S/SPACE)"
    draw_text(surface, font, shield_text, (12, 38),
              COLOR_SHIELD if shield_active else COLOR_TEXT)

    if game_over:
        draw_banner(surface, font,
                    f"GAME OVER | Distance: {int(distance)} m | Press R to restart")

def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)

def draw_banner(surface, font, text):
    surf = font.render(text, True, COLOR_GAME_OVER)
    rect = surf.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
    surface.blit(surf, rect)
