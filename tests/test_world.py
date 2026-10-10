import random
import unittest

from pokesnake.snake import DOWN, LEFT, MAX_QUEUED_TURNS, RIGHT, UP, Snake
from pokesnake.world import Status, World


def make_world(columns=6, rows=4):
    return World(columns, rows, ['a.png', 'b.png'], rng=random.Random(0))


class SnakeTest(unittest.TestCase):
    def test_moves_and_keeps_length(self):
        snake = Snake((2, 2))
        snake.queue_turn(RIGHT)
        snake.apply_next_turn()
        snake.move(snake.next_head(), grow=False)
        self.assertEqual(list(snake.body), [(3, 2)])
        self.assertNotIn((2, 2), snake)

    def test_reverse_ignored_when_snake_has_a_tail(self):
        snake = Snake((2, 2))
        snake.queue_turn(RIGHT)
        snake.apply_next_turn()
        snake.move((3, 2), grow=True)
        snake.queue_turn(LEFT)
        snake.apply_next_turn()
        self.assertEqual(snake.direction, RIGHT)

    def test_one_turn_per_step(self):
        snake = Snake((2, 2))
        snake.queue_turn(UP)
        snake.queue_turn(RIGHT)
        snake.apply_next_turn()
        self.assertEqual(snake.direction, UP)
        snake.apply_next_turn()
        self.assertEqual(snake.direction, RIGHT)

    def test_turn_queue_is_capped(self):
        snake = Snake((2, 2))
        for _ in range(MAX_QUEUED_TURNS + 5):
            snake.queue_turn(UP)
        self.assertEqual(len(snake._turns), MAX_QUEUED_TURNS)

    def test_can_follow_own_tail(self):
        snake = Snake((1, 1))
        for cell in [(2, 1), (2, 2), (1, 2)]:
            snake.move(cell, grow=True)
        # Body is a 2x2 square; the tail at (1, 1) moves away this step
        self.assertFalse(snake.would_collide((1, 1), growing=False))
        self.assertTrue(snake.would_collide((1, 1), growing=True))
        self.assertTrue(snake.would_collide((2, 1), growing=False))


class WorldTest(unittest.TestCase):
    def test_waits_for_first_key(self):
        world = make_world()
        start = world.snake.head
        self.assertIs(world.step(), Status.PLAYING)
        self.assertEqual(world.snake.head, start)

    def test_eating_grows_snake_and_records_sprite(self):
        world = make_world()
        world.food_cell = (world.snake.head[0] + 1, world.snake.head[1])
        world.food_sprite = 'b.png'
        world.snake.queue_turn(RIGHT)
        world.step()
        self.assertEqual(world.captured, ['b.png'])
        self.assertEqual(len(world.snake), 2)
        self.assertNotIn(world.food_cell, world.snake)

    def test_hitting_wall_loses(self):
        world = make_world()
        world.food_cell = (0, 0)
        world.snake.queue_turn(DOWN)
        statuses = [world.step() for _ in range(world.rows)]
        self.assertEqual(statuses[-1], Status.LOST)

    def test_filling_board_wins(self):
        world = World(2, 1, ['a.png'], rng=random.Random(0))
        self.assertEqual(world.food_cell, (0, 0))
        world.snake.queue_turn(LEFT)
        self.assertIs(world.step(), Status.WON)


if __name__ == '__main__':
    unittest.main()
