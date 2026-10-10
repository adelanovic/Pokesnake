"""Loading images, fonts and music."""

import os

import pygame

from pokesnake.settings import IMAGE_DIR, MUSIC_FILES, SPRITE_DIR


class Assets:
    """Loads every file once. Sprites are scaled on first use and cached per size."""

    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.sprite_names = sorted(f for f in os.listdir(SPRITE_DIR) if f.endswith('.png'))
        self.snake_head = self._load_scaled(os.path.join(IMAGE_DIR, 'poke-ball.png'), cell_size)
        self.score_font = pygame.font.SysFont('bahnschrift', max(cell_size * 3 // 10, 16), bold=True)
        self.message_font = pygame.font.SysFont('bahnschrift', max(cell_size * 35 // 100, 18), bold=True)
        self._sprite_cache = {}

    @staticmethod
    def _load_scaled(path, size):
        # Plain scale keeps the pixel art crisp; smoothscale would blur it
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (size, size))

    def sprite(self, name, size=None):
        size = size or self.cell_size
        key = (name, size)
        if key not in self._sprite_cache:
            self._sprite_cache[key] = self._load_scaled(os.path.join(SPRITE_DIR, name), size)
        return self._sprite_cache[key]

    @staticmethod
    def play_music():
        for music_file in MUSIC_FILES:
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)
                return
            except pygame.error as e:
                print(f'Could not play {music_file}: {e}')
