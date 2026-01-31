"""
Audio feedback: hop, death, splash, train horn, score.
Uses Panda3D AudioSound; gracefully no-op if files missing.
"""

import os
from pathlib import Path

import settings


class AudioManager:
    """Play sound effects; optional (no crash if files missing)."""

    def __init__(self, base):
        self.base = base
        self.enabled = settings.AUDIO_ENABLED
        self._sounds = {}
        self._base_path = Path(__file__).resolve().parent.parent

    def _path(self, rel: str) -> Path:
        return self._base_path.parent / rel

    def load_sound(self, key: str, path: str):
        """Load a sound by path (relative to project root)."""
        if not self.enabled:
            return
        full = self._path(path)
        if not full.exists():
            return
        try:
            sound = self.base.loader.loadSfx(str(full))
            if sound:
                self._sounds[key] = sound
        except Exception:
            pass

    def load_all(self):
        """Load all configured sounds."""
        self.load_sound("hop", settings.SOUND_HOP)
        self.load_sound("death", settings.SOUND_DEATH)
        self.load_sound("splash", settings.SOUND_SPLASH)
        self.load_sound("train_horn", settings.SOUND_TRAIN_HORN)
        self.load_sound("score", settings.SOUND_SCORE)
        self.load_sound("doom", settings.SOUND_DOOM)

    def play(self, key: str):
        """Play sound by key (if loaded)."""
        if not self.enabled:
            return
        s = self._sounds.get(key)
        if s:
            try:
                s.play()
            except Exception:
                pass

    def play_hop(self):
        self.play("hop")

    def play_death(self):
        self.play("death")

    def play_splash(self):
        self.play("splash")

    def play_train_horn(self):
        self.play("train_horn")

    def play_score(self):
        self.play("score")

    def play_doom(self):
        self.play("doom")
