"""Game settings: file locations, colors, board size, speeds and key bindings."""

import os
from typing import NamedTuple

import pygame

from pokesnake.snake import DOWN, LEFT, RIGHT, UP

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
SPRITE_DIR = os.path.join(BASE_DIR, 'pokemon')
MUSIC_FILES = [os.path.join(BASE_DIR, 'music', name) for name in ('freesound_trance.mp3', 'loop.wav')]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 153, 213)

GRID_COLUMNS = 16
GRID_ROWS = 10
MAX_CELL_SIZE = 100
MIN_CELL_SIZE = 40


class Speed(NamedTuple):
    name: str
    moves_per_second: int


# Picked with the number keys on the start and game over screens
SPEEDS = {
    pygame.K_1: Speed('Slow', 3),
    pygame.K_2: Speed('Normal', 5),
    pygame.K_3: Speed('Fast', 7),
}
SPEED_KEYS = {pygame.K_KP1: pygame.K_1, pygame.K_KP2: pygame.K_2, pygame.K_KP3: pygame.K_3}
SPEED_MENU = 'Pick a speed:   1 = Slow    2 = Normal    3 = Fast'

KEY_DIRECTIONS = {
    pygame.K_UP: UP, pygame.K_w: UP,
    pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
}
QUIT_KEYS = (pygame.K_q, pygame.K_ESCAPE)
REPLAY_KEY = pygame.K_c
