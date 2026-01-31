#!/usr/bin/env python3
"""
Crossy Road 3D - Entry point.
Run from project root: python crossy3d/main.py
Or from crossy3d/: python main.py
"""

import sys
import os

# Ensure crossy3d is on path when run from project root
_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

from game.game_app import GameApp

if __name__ == "__main__":
    app = GameApp()
    app.run()
