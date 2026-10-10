"""Everything that draws to the screen."""

from itertools import islice

import pygame

from pokesnake.settings import BLACK, WHITE


class Renderer:
    def __init__(self, screen, assets, cell_size):
        self.screen = screen
        self.assets = assets
        self.cell_size = cell_size
        self._score_key = None
        self._score_surface = None

    def _to_pixels(self, cell):
        return cell[0] * self.cell_size, cell[1] * self.cell_size

    def draw_world(self, world, speed):
        self.screen.fill(BLACK)
        self.screen.blit(self.assets.sprite(world.food_sprite), self._to_pixels(world.food_cell))

        body = world.snake.body
        self.screen.blit(self.assets.snake_head, self._to_pixels(body[0]))
        for cell, sprite_name in zip(islice(body, 1, None), world.captured):
            self.screen.blit(self.assets.sprite(sprite_name), self._to_pixels(cell))

        # Only re-render the score text when it changes
        score_key = (len(world.captured), speed.name)
        if score_key != self._score_key:
            self._score_key = score_key
            self._score_surface = self.assets.score_font.render(
                f'Captured: {score_key[0]}   Speed: {score_key[1]}', True, WHITE)
        self.screen.blit(self._score_surface, (10, 10))

    def draw_gallery(self, sprite_names, background):
        """Fill the screen with `sprite_names` laid out in the largest grid that fits."""
        self.screen.fill(background)
        if not sprite_names:
            return
        width, height = self.screen.get_size()
        margin = 10
        columns = 1
        while True:
            image_size = (width - margin * (columns + 1)) // columns
            rows = -(-len(sprite_names) // columns)
            if rows * (image_size + margin) + margin <= height:
                break
            columns += 1
        image_size = min(image_size, self.cell_size * 3)

        for index, name in enumerate(sprite_names):
            x = margin + (index % columns) * (image_size + margin)
            y = margin + (index // columns) * (image_size + margin)
            self.screen.blit(self.assets.sprite(name, image_size), (x, y))

    def draw_message(self, lines):
        """Draw `lines` centered on a white panel in the middle of the screen."""
        font = self.assets.message_font
        rendered = [font.render(line, True, BLACK) for line in lines]
        line_height = font.get_linesize()
        panel = pygame.Rect(0, 0, max(text.get_width() for text in rendered) + 60,
                            line_height * len(rendered) + 40)
        panel.center = self.screen.get_rect().center
        pygame.draw.rect(self.screen, WHITE, panel, border_radius=20)

        y = panel.top + 20
        for text in rendered:
            self.screen.blit(text, (panel.centerx - text.get_width() // 2, y))
            y += line_height
