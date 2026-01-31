"""
Game state machine: START, PLAYING, GAME_OVER.
"""

from enum import Enum


class GameState(Enum):
    START = "start"
    PLAYING = "playing"
    GAME_OVER = "game_over"
