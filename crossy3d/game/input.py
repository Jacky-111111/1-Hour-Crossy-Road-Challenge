"""
Input handling: movement buffer, key mapping.
"""

from collections import deque

# Movement directions: (dx, dz) - no diagonals (X matches camera view: left = +dx, right = -dx)
DIRECTIONS = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (1, 0),
    "right": (-1, 0),
}

KEY_TO_DIR = {
    "w": "up",
    "arrow_up": "up",
    "space": "up",
    "s": "down",
    "arrow_down": "down",
    "a": "left",
    "arrow_left": "left",
    "d": "right",
    "arrow_right": "right",
}


class InputManager:
    """Buffers one move during hop; maps keys to directions."""

    def __init__(self, buffer_max: int = 1):
        self.buffer_max = buffer_max
        self.buffer: deque = deque(maxlen=buffer_max)
        self._key_map = KEY_TO_DIR

    def push_direction(self, direction: str):
        """Queue a direction (up/down/left/right)."""
        if direction in DIRECTIONS and len(self.buffer) < self.buffer_max:
            self.buffer.append(direction)

    def pop_direction(self):
        """Consume next buffered direction or None."""
        if self.buffer:
            return self.buffer.popleft()
        return None

    def key_to_direction(self, key: str):
        """Map key name to direction or None."""
        return self._key_map.get(key)

    def clear(self):
        self.buffer.clear()
