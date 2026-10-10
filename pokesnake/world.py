"""One round of the game: the board, the snake, and the Pokemon. Pure logic, no pygame needed."""

import random
from enum import Enum

from pokesnake.snake import Snake


class Status(Enum):
    PLAYING = 'playing'
    LOST = 'lost'
    WON = 'won'


class World:
    """Advances the game one step at a time and keeps track of the Pokemon caught so far."""

    def __init__(self, columns, rows, sprite_names, rng=None):
        self.columns = columns
        self.rows = rows
        self.sprite_names = sprite_names
        self.rng = rng or random.Random()
        self.snake = Snake((columns // 2, rows // 2))
        self.captured = []
        self.status = Status.PLAYING
        self._all_cells = [(col, row) for col in range(columns) for row in range(rows)]
        self.food_cell, self.food_sprite = self._spawn_food()

    def _spawn_food(self):
        free_cells = [cell for cell in self._all_cells if cell not in self.snake]
        return self.rng.choice(free_cells), self.rng.choice(self.sprite_names)

    def in_bounds(self, cell):
        return 0 <= cell[0] < self.columns and 0 <= cell[1] < self.rows

    def step(self):
        if self.status is not Status.PLAYING:
            return self.status

        self.snake.apply_next_turn()
        if not self.snake.direction:
            return self.status  # Waiting for the first key press

        new_head = self.snake.next_head()
        ate_food = new_head == self.food_cell
        if not self.in_bounds(new_head) or self.snake.would_collide(new_head, growing=ate_food):
            self.status = Status.LOST
            return self.status

        self.snake.move(new_head, grow=ate_food)
        if ate_food:
            self.captured.append(self.food_sprite)
            if len(self.snake) == len(self._all_cells):
                self.status = Status.WON
            else:
                self.food_cell, self.food_sprite = self._spawn_food()
        return self.status
