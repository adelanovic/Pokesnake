"""The snake itself. Pure game logic in grid coordinates, no pygame needed."""

from collections import deque

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Extra key presses beyond this are dropped so mashing keys can't queue up turns for seconds
MAX_QUEUED_TURNS = 3


class Snake:
    """A snake on the grid. `body[0]` is the head (the poke ball), the rest is the tail of Pokemon."""

    def __init__(self, start):
        self.body = deque([start])
        self._cells = {start}
        self.direction = None
        self._turns = deque()

    def __len__(self):
        return len(self.body)

    def __contains__(self, cell):
        return cell in self._cells

    @property
    def head(self):
        return self.body[0]

    def queue_turn(self, direction):
        if len(self._turns) < MAX_QUEUED_TURNS:
            self._turns.append(direction)

    def apply_next_turn(self):
        """Apply at most one queued turn, skipping turns straight back into the snake's own body."""
        while self._turns:
            new_direction = self._turns.popleft()
            is_reverse = self.direction and new_direction == (-self.direction[0], -self.direction[1])
            if new_direction != self.direction and not (is_reverse and len(self.body) > 1):
                self.direction = new_direction
                return

    def next_head(self):
        return self.head[0] + self.direction[0], self.head[1] + self.direction[1]

    def would_collide(self, cell, growing):
        if cell not in self._cells:
            return False
        # The tail moves out of the way this step unless the snake is growing
        return growing or cell != self.body[-1]

    def move(self, new_head, grow):
        if not grow:
            self._cells.discard(self.body.pop())
        self.body.appendleft(new_head)
        self._cells.add(new_head)
