# pokesnake
A game I made for my kids that is like the game "snake" but utilizes Pokemon sprites.

The head of the snake is a pokeball. Every Pokemon you catch joins the end of your tail, and when
the game ends you get to see everyone you captured.

![Pokesnake](images/pokesnake.png)

## Running the game

Requires Python 3.8+.

```sh
pip install -r requirements.txt
python snake_game.py
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
