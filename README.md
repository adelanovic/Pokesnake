# pokesnake
A game I made for my kids that is like the game "snake" but utilizes Pokemon sprites.

The head of the snake is a pokeball. Every Pokemon you catch joins the end of your tail, and when
the game ends you get to see everyone you captured.

![Pokesnake](images/pokesnake.png)

## Running the game

Requires Python 3.8+.

```sh
pip install -r requirements.txt
python snake_game.py        # or: python -m pokesnake
```

## Playing in the browser

The game also runs in the browser using [pygbag](https://pygame-web.github.io/), which compiles Python and
pygame to WebAssembly. `main.py` is the browser entry point and `pygbag.ini` lists the files left out of
the web build.

To try the browser version locally:

```sh
pip install pygbag
pygbag .                    # then open http://localhost:8000
```

### Deploying to GitHub Pages

`.github/workflows/pages.yml` runs the tests, builds the web version and publishes it on every push to
`main`. One-time setup: on GitHub go to **Settings → Pages** and set **Source** to **GitHub Actions**.
The game is then live at `https://<your-username>.github.io/<repo-name>/`.

## Project layout

| File                     | What it does                                                    |
|--------------------------|-----------------------------------------------------------------|
| `snake_game.py`          | Launcher                                                        |
| `pokesnake/game.py`      | `Game`: the window and the start / play / game over flow        |
| `pokesnake/world.py`     | `World`: one round's rules - moving, catching, winning, losing  |
| `pokesnake/snake.py`     | `Snake`: the snake's body and turning                           |
| `pokesnake/renderer.py`  | `Renderer`: all drawing                                         |
| `pokesnake/assets.py`    | `Assets`: loads and caches images, fonts and music              |
| `pokesnake/settings.py`  | Colors, board size, speeds and key bindings                     |

`world.py` and `snake.py` don't use pygame, so the game rules can be tested on their own:

```sh
python -m unittest
```

## Controls

| Key                   | Action           |
|-----------------------|------------------|
| 1 / 2 / 3             | Pick speed: Slow, Normal or Fast (start and game over screens) |
| Arrow keys / W A S D  | Move             |
| C                     | Play again at the same speed |
| Q / Esc               | Quit (start and game over screens) |

The board is a 16 x 10 grid. On smaller screens the window shrinks automatically so the whole board fits.

## License

The source code is released under the [MIT License](LICENSE). Pokemon names and sprites belong to
Nintendo, Game Freak and Creatures Inc. They are not covered by that license and are included for
personal, non-commercial use only.
