"""The window and the flow between the start screen, playing and the game over screen.

The loops are async so the same code runs on the desktop and in the browser (via pygbag), where
every frame must `await asyncio.sleep(0)` to hand control back to the page.
"""

import asyncio
import os
import sys

import pygame

from pokesnake.assets import Assets
from pokesnake.renderer import Renderer
from pokesnake.settings import (BLUE, GRID_COLUMNS, GRID_ROWS, IMAGE_DIR, KEY_DIRECTIONS, MAX_CELL_SIZE,
                                MIN_CELL_SIZE, QUIT_KEYS, REPLAY_KEY, SPEED_KEYS, SPEED_MENU, SPEEDS)
from pokesnake.world import Status, World

IS_WEB = sys.platform == 'emscripten'
# The loop always runs this fast, even when the snake moves only a few times a second. In the browser the
# music is fed between frames, so a slow loop starves the audio and it crackles.
FPS = 60
AUDIO_BUFFER_SIZE = 2048


def fit_cell_size():
    """Shrink the grid cells on small monitors so the whole board stays visible."""
    if IS_WEB:
        return MAX_CELL_SIZE  # The browser scales the canvas to fit the page
    info = pygame.display.Info()
    return max(MIN_CELL_SIZE, min(MAX_CELL_SIZE,
                                  (info.current_w - 40) // GRID_COLUMNS,
                                  (info.current_h - 100) // GRID_ROWS))


class Game:
    def __init__(self):
        # A bigger buffer than pygame's default avoids crackling when the computer is busy
        pygame.mixer.pre_init(44100, -16, 2, AUDIO_BUFFER_SIZE)
        pygame.init()
        cell_size = fit_cell_size()
        pygame.display.set_caption('Pokesnake')
        pygame.display.set_icon(pygame.image.load(os.path.join(IMAGE_DIR, 'pikachu.png')))
        self.screen = pygame.display.set_mode((GRID_COLUMNS * cell_size, GRID_ROWS * cell_size))
        self.clock = pygame.time.Clock()
        self.assets = Assets(cell_size)
        self.renderer = Renderer(self.screen, self.assets, cell_size)

    async def run(self):
        self.assets.play_music()
        speed = await self.start_screen()
        while speed:
            world = await self.play(speed)
            if world is None:
                break
            speed = await self.game_over_screen(world, speed)
        pygame.quit()

    async def play(self, speed):
        """Play one round. Returns the finished World, or None if the window was closed."""
        world = World(GRID_COLUMNS, GRID_ROWS, self.assets.sprite_names)
        step_ms = 1000 / speed.moves_per_second
        elapsed_ms = 0
        self.renderer.draw_world(world, speed)
        pygame.display.update()
        self.clock.tick()  # Don't count time spent on the menu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key in KEY_DIRECTIONS:
                    world.snake.queue_turn(KEY_DIRECTIONS[event.key])

            # Move the snake only when its next step is due; cap the backlog so a hiccup can't skip moves
            elapsed_ms += self.clock.tick(FPS)
            if elapsed_ms >= step_ms:
                elapsed_ms = min(elapsed_ms - step_ms, step_ms)
                if world.step() is not Status.PLAYING:
                    return world
                self.renderer.draw_world(world, speed)
                pygame.display.update()

            await asyncio.sleep(0)

    async def start_screen(self):
        self.renderer.draw_gallery(self.assets.sprite_names[:24], BLUE)
        self.renderer.draw_message([
            'Pokesnake!',
            SPEED_MENU,
            'Use the arrow keys to catch Pokemon.',
        ])
        pygame.display.update()
        return await self._wait_for_speed()

    async def game_over_screen(self, world, speed):
        """Show the captured Pokemon. Returns the speed for the next game, or None to quit."""
        self.renderer.draw_gallery(world.captured, BLUE)
        self.renderer.draw_message([
            f'You captured {len(world.captured)} Pokemon Mayla or Aydin!',
            f'Press C to Play Again ({speed.name}) or Q to Quit.',
            SPEED_MENU,
            'You can do it! I love you!',
        ])
        pygame.display.update()
        return await self._wait_for_speed(speed)

    async def _wait_for_speed(self, current_speed=None):
        """Wait for a speed key (or C to replay at `current_speed`). Returns the speed, or None to quit."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    key = SPEED_KEYS.get(event.key, event.key)
                    if key in QUIT_KEYS:
                        return None
                    if key in SPEEDS:
                        return SPEEDS[key]
                    if key == REPLAY_KEY and current_speed:
                        return current_speed
            self.clock.tick(FPS)
            await asyncio.sleep(0)


def main():
    asyncio.run(Game().run())
    sys.exit()
