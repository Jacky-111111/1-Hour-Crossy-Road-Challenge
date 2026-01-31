"""
UI: start screen, HUD (score, best, FPS), game over screen.
"""

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

import settings


class UIManager:
    """Start / HUD / Game over text overlays."""

    def __init__(self, base):
        self.base = base
        self._title = None
        self._subtitle = None
        self._score_text = None
        self._best_text = None
        self._fps_text = None
        self._game_over_title = None
        self._game_over_score = None
        self._game_over_restart = None
        self._nodes = []

    def _make_text(
        self,
        text: str,
        pos=(0, 0),
        scale=0.07,
        fg=(1, 1, 1, 1),
        align=TextNode.A_center,
        mayChange=False,
    ):
        node = OnscreenText(
            text=text,
            pos=pos,
            scale=scale,
            fg=fg,
            align=align,
            mayChange=mayChange,
        )
        self._nodes.append(node)
        return node

    def show_start_screen(self):
        """Press Enter to Start."""
        self.hide_all()
        self._title = self._make_text(
            "Crossy Road 3D",
            pos=(0, 0.1),
            scale=0.12,
        )
        self._subtitle = self._make_text(
            "Press ENTER to Start",
            pos=(0, -0.1),
            scale=0.06,
        )

    def show_hud(self, score: int, best: int):
        """Score and best; optionally FPS."""
        self._score_text = self._make_text(
            f"Score: {score}",
            pos=(-1.3, 0.9),
            scale=0.05,
            align=TextNode.A_left,
            mayChange=True,
        )
        self._best_text = self._make_text(
            f"Best: {best}",
            pos=(-1.3, 0.82),
            scale=0.05,
            align=TextNode.A_left,
            mayChange=True,
        )
        if settings.DEBUG_SHOW_FPS:
            self._fps_text = self._make_text(
                "FPS: 0",
                pos=(1.2, 0.9),
                scale=0.04,
                align=TextNode.A_right,
                mayChange=True,
            )

    def update_hud(self, score: int, best: int, fps: float = 0):
        if self._score_text:
            self._score_text.setText(f"Score: {score}")
        if self._best_text:
            self._best_text.setText(f"Best: {best}")
        if self._fps_text and settings.DEBUG_SHOW_FPS:
            self._fps_text.setText(f"FPS: {int(fps)}")

    def show_game_over(self, score: int, best: int):
        """Game over: score, best, R to Restart."""
        self.hide_all()
        self._game_over_title = self._make_text(
            "GAME OVER",
            pos=(0, 0.15),
            scale=0.1,
            fg=(1, 0.3, 0.3, 1),
        )
        self._game_over_score = self._make_text(
            f"Score: {score}  |  Best: {best}",
            pos=(0, 0),
            scale=0.06,
        )
        self._game_over_restart = self._make_text(
            "Press R to Restart",
            pos=(0, -0.15),
            scale=0.05,
        )

    def hide_all(self):
        """Remove all UI nodes."""
        for node in self._nodes:
            node.destroy()
        self._nodes = []
        self._title = None
        self._subtitle = None
        self._score_text = None
        self._best_text = None
        self._fps_text = None
        self._game_over_title = None
        self._game_over_score = None
        self._game_over_restart = None
