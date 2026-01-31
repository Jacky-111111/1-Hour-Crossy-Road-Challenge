"""
UI: start screen, HUD (score, best, FPS, controls), game over screen with Restart button.
"""

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode

import settings


# One-line control reminders for HUD; full list for start/game over
CONTROLS_HUD = "WASD / Arrows - Move  |  R - Restart  |  Esc - Quit"
CONTROLS_FULL = [
    "W / ↑ / Space - Forward    S / ↓ - Back    A / ← - Left    D / → - Right",
    "Enter - Start / Confirm    R - Restart    Esc - Quit    F1 - Debug",
]


class UIManager:
    """Start / HUD / Game over text overlays + Restart button."""

    def __init__(self, base):
        self.base = base
        self._title = None
        self._subtitle = None
        self._score_text = None
        self._best_text = None
        self._fps_text = None
        self._controls_hud_text = None
        self._game_over_title = None
        self._game_over_score = None
        self._game_over_restart = None
        self._restart_button = None
        self._game_over_controls = []
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
        """SpongeBob theme title + Press Enter to Start + all controls reminder."""
        self.hide_all()
        self._title = self._make_text(
            "SpongeBob Crossy Road",
            pos=(0, 0.2),
            scale=0.11,
            fg=(1.0, 0.95, 0.3, 1),
        )
        self._subtitle = self._make_text(
            "Bikini Bottom 3D",
            pos=(0, 0.08),
            scale=0.055,
            fg=(0.3, 0.7, 0.9, 1),
        )
        self._make_text(
            "Press ENTER to Start",
            pos=(0, -0.02),
            scale=0.06,
        )
        for i, line in enumerate(CONTROLS_FULL):
            self._make_text(
                line,
                pos=(0, -0.22 - i * 0.06),
                scale=0.035,
                fg=(0.9, 0.9, 0.9, 1),
            )

    def show_hud(self, score: int, best: int):
        """Score, best, FPS, and controls reminder."""
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
        self._controls_hud_text = self._make_text(
            CONTROLS_HUD,
            pos=(0, -0.92),
            scale=0.032,
            fg=(0.85, 0.85, 0.85, 1),
        )

    def update_hud(self, score: int, best: int, fps: float = 0):
        if self._score_text:
            self._score_text.setText(f"Score: {score}")
        if self._best_text:
            self._best_text.setText(f"Best: {best}")
        if self._fps_text and settings.DEBUG_SHOW_FPS:
            self._fps_text.setText(f"FPS: {int(fps)}")

    def show_game_over(self, score: int, best: int, on_restart=None):
        """Game over: score, best, Restart button, and all controls reminder."""
        self.hide_all()
        self._game_over_title = self._make_text(
            "GAME OVER",
            pos=(0, 0.22),
            scale=0.1,
            fg=(1, 0.3, 0.3, 1),
        )
        self._game_over_score = self._make_text(
            f"Score: {score}  |  Best: {best}",
            pos=(0, 0.08),
            scale=0.06,
        )
        self._game_over_restart = self._make_text(
            "Press R or click Restart",
            pos=(0, -0.02),
            scale=0.045,
        )
        if on_restart is not None:
            self._restart_button = DirectButton(
                text="Restart",
                scale=0.06,
                command=on_restart,
                pos=(0, 0, -0.12),
            )
            self._nodes.append(self._restart_button)
        for i, line in enumerate(CONTROLS_FULL):
            self._make_text(
                line,
                pos=(0, -0.32 - i * 0.055),
                scale=0.032,
                fg=(0.85, 0.85, 0.85, 1),
            )

    def hide_all(self):
        """Remove all UI nodes and the Restart button."""
        for node in self._nodes:
            if hasattr(node, "destroy"):
                node.destroy()
        self._nodes = []
        self._title = None
        self._subtitle = None
        self._score_text = None
        self._best_text = None
        self._fps_text = None
        self._controls_hud_text = None
        self._game_over_title = None
        self._game_over_score = None
        self._game_over_restart = None
        self._restart_button = None
