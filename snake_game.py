"""Pokesnake - a snake game where every Pokemon you catch joins your tail."""

import os
import random
import sys

import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
FOOD_IMAGE_DIR = os.path.join(BASE_DIR, 'pokemon')
MUSIC_FILES = [os.path.join(BASE_DIR, 'music', name) for name in ('freesound_trance.mp3', 'loop.wav')]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 153, 213)

GRID_COLUMNS = 16
GRID_ROWS = 10
MAX_CELL_SIZE = 100
MIN_CELL_SIZE = 40

# Snake moves per second for each speed, picked with the number keys
SPEEDS = {
    pygame.K_1: ('Slow', 3),
    pygame.K_2: ('Normal', 5),
    pygame.K_3: ('Fast', 7),
}
SPEED_KEYS = {pygame.K_KP1: pygame.K_1, pygame.K_KP2: pygame.K_2, pygame.K_KP3: pygame.K_3}
SPEED_MENU = 'Pick a speed:   1 = Slow    2 = Normal    3 = Fast'

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
KEY_DIRECTIONS = {
    pygame.K_UP: UP, pygame.K_w: UP,
    pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
}

pygame.init()

# Shrink the grid cells on small monitors so the whole board stays visible
display_info = pygame.display.Info()
CELL_SIZE = max(MIN_CELL_SIZE, min(MAX_CELL_SIZE,
                                   (display_info.current_w - 40) // GRID_COLUMNS,
                                   (display_info.current_h - 100) // GRID_ROWS))
SCREEN_WIDTH = GRID_COLUMNS * CELL_SIZE
SCREEN_HEIGHT = GRID_ROWS * CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pokesnake')
pygame.display.set_icon(pygame.image.load(os.path.join(IMAGE_DIR, 'pikachu.png')))
clock = pygame.time.Clock()

score_font = pygame.font.SysFont('bahnschrift', max(CELL_SIZE * 3 // 10, 16), bold=True)
message_font = pygame.font.SysFont('bahnschrift', max(CELL_SIZE * 35 // 100, 18), bold=True)

food_images = sorted(f for f in os.listdir(FOOD_IMAGE_DIR) if f.endswith('.png'))
snake_head_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMAGE_DIR, 'poke-ball.png')).convert_alpha(), (CELL_SIZE, CELL_SIZE))

_image_cache = {}


def play_music():
    for music_file in MUSIC_FILES:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            return
        except pygame.error as e:
            print(f'Could not play {music_file}: {e}')


def load_food_image(image_name, size=None):
    """Load a Pokemon sprite scaled to `size`, caching it so each file is only read once."""
    size = size or CELL_SIZE
    key = (image_name, size)
    if key not in _image_cache:
        image = pygame.image.load(os.path.join(FOOD_IMAGE_DIR, image_name)).convert_alpha()
        _image_cache[key] = pygame.transform.scale(image, (size, size))
    return _image_cache[key]


def draw_snake(snake_body, captured_images):
    screen.blit(snake_head_image, snake_body[0])
    for block, image_name in zip(snake_body[1:], captured_images):
        screen.blit(load_food_image(image_name), block)


def create_food(snake_body):
    free_cells = [[col * CELL_SIZE, row * CELL_SIZE]
                  for col in range(GRID_COLUMNS) for row in range(GRID_ROWS)
                  if [col * CELL_SIZE, row * CELL_SIZE] not in snake_body]
    return random.choice(free_cells), random.choice(food_images)


def display_images(images):
    """Draw the captured Pokemon in a grid that fills the screen."""
    if not images:
        return
    margin = 10
    columns = 1
    while True:
        image_size = (SCREEN_WIDTH - margin * (columns + 1)) // columns
        rows = -(-len(images) // columns)
        if rows * (image_size + margin) + margin <= SCREEN_HEIGHT:
            break
        columns += 1
    image_size = min(image_size, CELL_SIZE * 3)

    for index, image_name in enumerate(images):
        x = margin + (index % columns) * (image_size + margin)
        y = margin + (index // columns) * (image_size + margin)
        screen.blit(load_food_image(image_name, image_size), (x, y))


def draw_centered_text(lines):
    rendered = [message_font.render(line, True, BLACK) for line in lines]
    line_height = message_font.get_linesize()
    panel_width = max(text.get_width() for text in rendered) + 60
    panel_height = line_height * len(rendered) + 40
    panel = pygame.Rect(0, 0, panel_width, panel_height)
    panel.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, WHITE, panel, border_radius=20)

    y = panel.top + 20
    for text in rendered:
        screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, y))
        y += line_height


def wait_for_speed(current_speed=None):
    """Wait for a speed key (or C to replay at `current_speed`). Returns the speed, or None to quit."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                key = SPEED_KEYS.get(event.key, event.key)
                if key in (pygame.K_q, pygame.K_ESCAPE):
                    return None
                if key in SPEEDS:
                    return SPEEDS[key]
                if key == pygame.K_c and current_speed:
                    return current_speed
        clock.tick(30)


def start_screen():
    screen.fill(BLUE)
    display_images(food_images[:24])
    draw_centered_text([
        'Pokesnake!',
        SPEED_MENU,
        'Use the arrow keys to catch Pokemon.',
    ])
    pygame.display.update()
    return wait_for_speed()


def game_over_screen(captured_images, speed):
    """Show the captured Pokemon. Returns the speed for the next game, or None to quit."""
    screen.fill(BLUE)
    display_images(captured_images)
    draw_centered_text([
        f'You captured {len(captured_images)} Pokemon Mayla or Aydin!',
        f'Press C to Play Again ({speed[0]}) or Q to Quit.',
        SPEED_MENU,
        'You can do it! I love you!',
    ])
    pygame.display.update()
    return wait_for_speed(speed)


# Main game loop. Returns the list of Pokemon captured, or None if the window was closed.
def game_loop(speed):
    speed_name, moves_per_second = speed
    x = (GRID_COLUMNS // 2) * CELL_SIZE
    y = (GRID_ROWS // 2) * CELL_SIZE
    direction = None
    pending_directions = []

    snake_body = [[x, y]]
    captured_images = []
    food_pos, food_image_name = create_food(snake_body)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key in KEY_DIRECTIONS:
                pending_directions.append(KEY_DIRECTIONS[event.key])

        # Apply at most one turn per tick and ignore turns straight back into the snake's own body
        while pending_directions:
            new_direction = pending_directions.pop(0)
            is_reverse = direction and new_direction == (-direction[0], -direction[1])
            if new_direction != direction and not (is_reverse and len(snake_body) > 1):
                direction = new_direction
                break

        if direction:
            x += direction[0] * CELL_SIZE
            y += direction[1] * CELL_SIZE

        # Game over if the snake hits the wall
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            return captured_images

        ate_food = [x, y] == food_pos
        snake_body.insert(0, [x, y])
        if not ate_food:
            del snake_body[-1]

        # Game over if the snake hits itself
        if direction and [x, y] in snake_body[1:]:
            return captured_images

        if ate_food:
            captured_images.append(food_image_name)
            if len(snake_body) == GRID_COLUMNS * GRID_ROWS:
                return captured_images
            food_pos, food_image_name = create_food(snake_body)

        screen.fill(BLACK)
        screen.blit(load_food_image(food_image_name), food_pos)
        draw_snake(snake_body, captured_images)
        score_text = score_font.render(f'Captured: {len(captured_images)}   Speed: {speed_name}', True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.update()

        clock.tick(moves_per_second)


def main():
    play_music()
    speed = start_screen()
    while speed:
        captured_images = game_loop(speed)
        if captured_images is None:
            break
        speed = game_over_screen(captured_images, speed)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
