"""Entry point for the browser build (pygbag looks for main.py). On the desktop use snake_game.py."""

import asyncio

# pygbag only loads the packages it sees imported here, so pygame must be imported directly
import pygame  # noqa: F401

from pokesnake.game import Game

asyncio.run(Game().run())
